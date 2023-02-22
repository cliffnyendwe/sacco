<?php

// disabling WSDL cache
ini_set("soap.wsdl_cache_enabled", "0");

$delivery_receipt = array();
define("LOG_FILE", "/tmp/mpesa_confirmation.log");

function C2BPaymentConfirmationResult($obj) 
{
    return "C2B Payment Transaction %s result received.";
}

function ConfirmC2BPayment($obj) 
{
    global $delivery_receipt; 						
    $delivery_receipt["TransType"] = $obj->TransType;
    $delivery_receipt["TransID"] = $obj->TransID;
    $delivery_receipt["TransTime"] = $obj->TransTime;
    $delivery_receipt["TransAmount"] = $obj->TransAmount;
    $delivery_receipt["BusinessShortCode"] = $obj->BusinessShortCode;
    $delivery_receipt["BillRefNumber"] = $obj->BillRefNumber;
    $delivery_receipt["InvoiceNumber"] = $obj->InvoiceNumber;
    $delivery_receipt["OrgAccountBalance"] = $obj->OrgAccountBalance;
    $delivery_receipt["ThirdPartyTransID"] = $obj->ThirdPartyTransID;
    $delivery_receipt["MSISDN"] = $obj->MSISDN;
    $delivery_receipt["FirstName"] = $obj->KYCInfo[0]->KYCValue;
    $delivery_receipt["MiddleName"] = $obj->KYCInfo[1]->KYCValue;
    $delivery_receipt["LastName"] = $obj->KYCInfo[2]->KYCValue;
    
    return "C2B Payment Transaction $obj->TransID result received.";
}

//error_log(date("Y-m-d H:i:s").": $HTTP_RAW_POST_DATA\n", 3, LOG_FILE);
error_log(date("Y-m-d H:i:s").": " . file_get_contents("php://input"). "\n\n", 3, LOG_FILE);

function save_payment($delivery_receipt)
{
    $sql = "INSERT INTO core_manager_incomingpayments(transaction_type, transaction_id, tstamp, mpesa_amt, business_number, mpesa_acc, mpesa_msisdn, mpesa_sender, source)  VALUES (:transaction_type, :transaction_id, :tstamp, :mpesa_amt, :business_number, :mpesa_acc, :mpesa_msisdn, :mpesa_sender, :source)";

    $params = array
        (
        ':transaction_type' => $delivery_receipt["TransType"], 
        ':transaction_id' => $delivery_receipt["TransID"], 
        ':tstamp' => $delivery_receipt["TransTime"], 
        ':mpesa_amt' => $delivery_receipt["TransAmount"], 
        ':business_number' => $delivery_receipt["BusinessShortCode"], 
        ':mpesa_acc' => $delivery_receipt["BillRefNumber"], 
        ':mpesa_msisdn' => $delivery_receipt["MSISDN"], 
        ':mpesa_sender' => "{$delivery_receipt['FirstName']} {$delivery_receipt['MiddleName']} {$delivery_receipt['LastName']}",
        ':source' => 'MPESA',
        );
    $result = _execute($sql, $params);
}

function init_soap($soapServer) 
{
    try
    {
    
        $soapServer->addFunction("C2BPaymentConfirmationResult");        
        $soapServer->addFunction("ConfirmC2BPayment");
        $soapServer->handle();

    } 
    
    catch (SoapFault $sf)
    {
        throw new SoapFault($sf->faultcode, $sf->faultstring);
    }
}

function _execute($sql, $params) 
{
    $host = "localhost";
    $username = "root";
    $password = "r00t";
    $database = "circle";


    try
    {
        $pdo = new PDO("mysql:host=$host;dbname=$database", $username, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        $pdo = null;
        $stmt = null;
    } 
    
    catch (PDOException $pe) 
    {
        throw new SoapFault(strval($pe->getCode()), $pe->getMessage());
    }
}

try
{ 
    $soapServer = new SoapServer("CBPInterface_C2BPaymentValidationAndConfirmation.wsdl");
    init_soap($soapServer);
    if ($delivery_receipt["TransID"])
    {
        save_payment($delivery_receipt);
    }
}

catch(SoapFault $sf)
{
    error_log(date("Y/m/d H:i:s") ."ERROR". $sf->__toString(), 3, LOG_FILE);
    $fault = $soapServer->fault('SVC0001', 'Service Error');
}

catch(Exception $e)
{
    error_log(date("Y/m/d H:i:s") . "ERROR".$e->__toString(), 3, LOG_FILE);
    $fault = $soapServer->fault('SVC0001', 'Service Error');
}

?>
