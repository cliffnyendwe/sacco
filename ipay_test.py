#!/usr/bin/env python

def credit_card_transaction_request(sid):
    print "----- credit card transaction request --------"
    import requests
    ipay_url = "https://apis.ipayafrica.com/payments/v2/transact/cc"
    #ipay_url = "http://localhost/test.php"
    #key = "demo"
    key = "imag56984mted45142158RUM2145"
    #vid = "demo"
    vid = "imaginarium"
    curr = "KES"
    cvv = "755"
    cardno = "4444444444444444"
    cardno = "4243142000256650"
    #cardno = "4251996000024395"
    month = "04"
    year = "19"
    #month = "02"
    #year = "21"
    cust_address = "Yaya centre"
    cust_postcode = "00100"
    cust_city = "Nairobi"
    cust_stateprov = "Nairobi"
    cust_country = "Kenya"
    sid = sid
    fname = "John"
    lname = "Patrick M Awori"

    hash_string = "%s%s%s%s%s%s%s%s%s%s%s%s%s" %(sid,vid,cardno,cvv,month,year,cust_address,cust_city,cust_country,cust_postcode,cust_stateprov,fname,lname)
   
    import hmac
    import hashlib
    #generated_hash = hash_hmac('sha256',hash_string , key);
    generated_hash = hmac.new(key, hash_string, hashlib.sha256).hexdigest()

    data = {
        "vid" : vid,
        "curr" : curr,
        "cvv" : cvv,
        "cardno" : cardno,
        "month" : month,
        "year" : year,
        "cust_address" : cust_address,
        "cust_postcode" : cust_postcode,
        "cust_city" : cust_city,
        "cust_stateprov" : cust_stateprov,
        "cust_country" : cust_country,
        "sid" : sid,
        "fname" : fname,
        "lname" : lname,
        "hash": generated_hash,
    }
    print "-=======================================-"
    print data
    response = requests.post(ipay_url, data=data)
    print "--------------------------------------------"
    print response
    print "-------------11--------------------------"
    print response.url
    print "-------------22--------------------------"
    print response.text
    print "-------------33--------------------------"
    print response.encoding
    print "-------------44--------------------------"
    response_json = response.json()
    
    #print response_json
    print "--------------------------------------------"

    """print response_json['status']
    print response_json['header_status']

    print response_json['data']['account']
    print response_json['data']['hash']
    print response_json['data']['payment_channels'] 
    print response_json['data']['oid']
    print response_json['data']['amount']
    print response_json['data']['sid'] """
   
    
def ipay_initiator_request():
    import requests
    size = 6
    import uuid
    code = str(uuid.uuid4()).replace('-', '')
    oid = code.upper()[:size].upper()
    print oid
    
    ipay_url = "https://api.ipayafrica.com/payments/v2/transact"
    ipay_url = "https://apis.ipayafrica.com/payments/v2/transact"
    #ipay_url = "http://localhost/test.php"
    #key = "demo"
    key = "imag56984mted45142158RUM2145"
    
    live = "1"       
    oid= oid
    inv = oid
    amount = "120.00"
    tel = "254739196110"
    eml = "lznduta@gmail.co.ke"
    #vid = "demo"
    vid = "imaginarium"
    curr = "KES"
    p1 = "x" 
    p2 = "y"
    p3 = "z" 
    p4 = "za"
    cbk = "https://146.185.169.101/IPay/callback.php"
    cst = "1"
    crl = "0"
    hash_string = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s" %(live,oid,inv,amount,tel,eml,vid,curr,p1,p2,p3,p4,cst,cbk);
   
    import hmac
    import hashlib
    #generated_hash = hash_hmac('sha256',hash_string , key);
    generated_hash = hmac.new(key, hash_string, hashlib.sha256).hexdigest()

    data = {
        "live": live,        
        "oid": oid,
        "inv": inv,
        "amount": amount,
        "tel": tel,
        "eml": eml,
        "vid": vid,
        "curr": curr,
        "p1": p1, 
        "p2": p2,
        "p3": p3,
        "p4": p4,
        "cbk": cbk,
        "cst": cst,
        "crl": crl,
        "hash": generated_hash,
        
    }
    print data
    response = requests.post(ipay_url, data=data)
    #print response.url
    #print response.text
    #print response.encoding
    response_json = response.json()
    sid = response_json['data']['sid']
    print "--------------------------------------------"
    #print response_json
    print "============================================"
    print sid
    print "============================================"
    """
    print response_json['status']
    print response_json['header_status']
    print response_json['data']['account']
    print response_json['data']['hash']
    print response_json['data']['payment_channels'] 
    print response_json['data']['oid']
    print response_json['data']['amount']
    print response_json['data']['sid']"""
    

    
    credit_card_transaction_request(sid)

if __name__ == '__main__':
    ipay_initiator_request()
    """while True:   
        ipay_initiator_request()
        pass#time.sleep(20) """
    #while True:
    """try:
        pass
    except Exception, e:
        print e
    finally:
        pass #print "completed processing" 
        """
    
