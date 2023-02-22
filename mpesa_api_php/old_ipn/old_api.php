<?php

    date_default_timezone_set("Africa/Nairobi");
    
    require_once('MySQL.php');
   
    define('DEBUG', TRUE);
    define("SYS_ERR_MESSAGE", "Internal Server Error");
    
    define("LOG_FILE", "/var/log/nginx/circle/mpesa_access.log");
    $hostname = "localhost";
    $username = "root";
    $password = "r00t";
    $database = "circle";


    ini_set('display_errors',1); 
    error_reporting(E_ALL & ~E_NOTICE);
    
    set_error_handler("exception_error_handler");
    
    /**
     * 404 Exception
     */
    class HTTP404Exception extends Exception{ }

    /**
     * 503 Exception
     */
    class HTTP503Exception extends Exception{ }

    /**
     * 400 Exception
     */
    class HTTP400Exception extends Exception{ }

    /**
     * 500 Exception
     */
    class HTTP500Exception extends Exception{ }

    /**
     * 403 Exception
     */
    class HTTP403Exception extends Exception{ }

    function status($msg, $text, $description="", $notification="") {            
        //Header('Content-Type: application/json');
        $response[] = array('status'=>$msg, 'message'=>$text,
            'description'=>$description, 'notification'=>$notification);
        http_response_code($msg);
        echo json_encode($response);
    }

    /**
     * Convert errors into exceptions.
     * NOTE: If an exception is not caught, a PHP _Fatal Error_ will be issued with
     * an "Uncaught Exception ...". This means that your program will be
     * terminated.
     */

    function exception_error_handler($errno, $errstr, $errfile, $errline )
    {
        throw new ErrorException($errstr, 0, $errno, $errfile, $errline);
    }
   
    function save_payment($mysqli, $id, $orig, $dest, $tstamp, $text, $customer_id, $mpesa_code, $mpesa_acc, $mpesa_msisdn, $mpesa_trx_date, $mpesa_trx_time, $mpesa_amt, $mpesa_sender, $business_number  ) {
    
        $stmt = $mysqli->prepare("INSERT INTO core_manager_incomingpayments(transaction_id, orig, dest, tstamp, text, customer_id, mpesa_code, mpesa_acc, mpesa_msisdn, mpesa_trx_date, mpesa_trx_time, mpesa_amt, mpesa_sender, business_number, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
                    
        $source = 'MPESA';
        if ($stmt === FALSE)
                throw new HTTP400Exception($mysqli->error);

        if ( ! $stmt->bind_param('sssssssssssssss', $id, $orig, $dest, $tstamp, $text, $customer_id, $mpesa_code, $mpesa_acc, $mpesa_msisdn, $mpesa_trx_date, $mpesa_trx_time, $mpesa_amt, $mpesa_sender, $business_number, $source))
            throw new HTTP503Exception($stmt->error);

        if ( ! $stmt->execute()) {
            if($stmt->errno == '1062') {
                error_log("\nDEBUG: " . date("Y-m-d H:i:s") . ", " . "duplicate request", 3, LOG_FILE); 
            } else {
                throw new HTTP400Exception($stmt->error);
            }
        }

        if ( ! $stmt->close())
            throw new HTTP503Exception($stmt->error);
    }
    
    try {
    
        /*$_SERVER["QUERY_STRING"] = "id=240460945&orig=MPESA&dest=254717069348&tstamp=2016-01-06 22:13:08&text=KA65SPBDKD Confirmed. on 6/1/16 at 10:12 PM Ksh10.00 received from MICHAEL MUKIMA 254716223118.  Account Number MTSE New Utility balance is Ksh80.00&customer_id=8075&user=default&pass=default&routemethod_id=2&routemethod_name=HTTP&mpesa_code=KA65SPBDKD&mpesa_acc=MTSE&mpesa_msisdn=254716223118&mpesa_trx_date=6/1/16&mpesa_trx_time=10:12 PM&mpesa_amt=10.0&mpesa_sender=MICHAEL MUKIMA&business_number=179126";*/
        
        /*
            GET DATA : array (
              'id' => '240460945',
              'orig' => 'MPESA',
              'dest' => '254717069348',
              'tstamp' => '2016-01-06 22:13:08',
              'text' => 'KA65SPBDKD Confirmed. on 6/1/16 at 10:12 PM Ksh10.00 received from MICHAEL MUKIMA 254716223118.  Account Number MTSE New Utility balance is Ksh80.00',
              'customer_id' => '8075',
              'user' => 'default',
              'pass' => 'default',
              'routemethod_id' => '2',
              'routemethod_name' => 'HTTP',
              'mpesa_code' => 'KA65SPBDKD',
              'mpesa_acc' => 'MTSE',
              'mpesa_msisdn' => '254716223118',
              'mpesa_trx_date' => '6/1/16',
              'mpesa_trx_time' => '10:12 PM',
              'mpesa_amt' => '10.0',
              'mpesa_sender' => 'MICHAEL MUKIMA',
              'business_number' => '179126',
            )
            */
        //parse_str(file_get_contents('php://input'), $postdata);
        parse_str($_SERVER["QUERY_STRING"], $postdata);
        print "<pre >";
        
        print_r($postdata);

        if (DEBUG) {
            error_log("\nDEBUG: " . date("Y-m-d H:i:s") . ", " . 
                var_export($postdata, TRUE), 3, LOG_FILE); 
        }       
    
        if(!isset($postdata['id']) || !isset($postdata['orig']) || 
            !isset($postdata['dest']) || !isset($postdata['tstamp']) || 
            !isset($postdata['text']) || !isset($postdata['customer_id']) ||
            !isset($postdata['mpesa_code']) || !isset($postdata['mpesa_acc']) || 
            !isset($postdata['mpesa_msisdn']) || !isset($postdata['mpesa_trx_date']) || 
            !isset($postdata['mpesa_trx_time']) || !isset($postdata['mpesa_amt']) || 
            !isset($postdata['mpesa_sender']) || !isset($postdata['business_number'])
            ) {
            throw new HTTP400Exception("Missing POST data");
        }
              
        $mysql = new MySQL($hostname, $username, $password, $database);
        
        if($mysql->mysqli->connect_errno){
            throw new Exception("Failed to connect to MySQL: (" . $mysql->mysqli->connect_errno . ") " . $mysql->mysqli->connect_error);
        }
        
        
        save_payment(
            $mysql->mysqli, 
            trim($postdata['id']), 
            trim($postdata['orig']), 
            trim($postdata['dest']), 
            trim($postdata['tstamp']), 
            trim($postdata['text']),
            trim($postdata['customer_id']),
            trim($postdata['mpesa_code']),
            trim($postdata['mpesa_acc']),
            trim($postdata['mpesa_msisdn']),
            trim($postdata['mpesa_trx_date']),
            trim($postdata['mpesa_trx_time']),
            trim($postdata['mpesa_amt']),
            trim($postdata['mpesa_sender']),
            trim($postdata['business_number'])
        );
        status('200', 'Request Successful', "", '');
        
    } catch (HTTP400Exception $e) {
        status('400', 'Bad Request', $e->getMessage(), 'error');
        error_log(date("y-m-d H:i:s")." ".$e->__toString()."\n", 3, LOG_FILE);
    } catch (HTTP404Exception $e) {
        status('404', 'Not Found', $e->getMessage(), 'info');
        error_log(date("y-m-d H:i:s")." ".$e->__toString()."\n", 3, LOG_FILE);
    } catch (HTTP503Exception $e) {
        status('503', 'Service Unavailable', $e->getMessage(), 'info');
        error_log(date("y-m-d H:i:s")." ".$e->__toString()."\n", 3, LOG_FILE);
    } catch (HTTP500Exception $e) {
        status('500', "Internal Server Error", $e->getMessage(), 'error');
        error_log(date("y-m-d H:i:s")." ".$e->__toString()."\n", 3, LOG_FILE);
    } catch (HTTP403Exception $e) {
        status('403', "Forbidden", $e->getMessage(), 'info');
        error_log(date("y-m-d H:i:s")." ".$e->__toString()."\n", 3, LOG_FILE);
    } catch (Exception $e) {
        status('503', SYS_ERR_MESSAGE, $e->getMessage(), 'info');
        error_log(date("y-m-d H:i:s")." ".$e->__toString()."\n", 3, LOG_FILE);
    }
    

    
    
    
