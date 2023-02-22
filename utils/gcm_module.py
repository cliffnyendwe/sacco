import os
from gcm import GCM
#from pyramid.api_resources import order_resource

from django.conf import settings

gcm = GCM(settings.GCM_KEY)
from pyfcm import FCMNotification
push_service = FCMNotification(api_key=settings.GCM_KEY)

# this is a test message
def send_json_data(ids, data_message):
    result = push_service.notify_multiple_devices(registration_ids=ids, data_message=data_message)
    #result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message)
    print "-----------------------------"
    print result 
    print "-----------------------------"
    return result
    
def send_json_data_x(ids, data):
    response = gcm.json_request(registration_ids=ids, data=data)

    if 'errors' in response:
        for error, reg_ids in response['errors'].items():
            # Check for errors and act accordingly
            print('%s %s' %(error, reg_ids))
    if 'canonical' in response:
        for reg_id, canonical_id in response['canonical'].items():
            # Replace reg_id with canonical_id in your database - means an id was regenerated for same device
            print('Replace %s with %s.' %(reg_id, canonical_id))


def android_notification(notification_category, object_id, user, notification_data = None):        
    if user.android_device_id:
        data = {'type': notification_category}  
        
        if notification_data:
            data = dict(data.items() + notification_data.items())
        send_json_data([user.android_device_id,], data)
        #        send_json_data([user.android_device_id + 'xx',], data)
        return data
    return None
    

def android_notification_test(notification_category, device_id, notification_data = None):        
    if device_id:
        data = {'note_type': notification_category}  
        
        if notification_data:
            data = dict(data.items() + notification_data.items())
        send_json_data([device_id,], data)
        #        send_json_data([user.android_device_id + 'xx',], data)
        return data
    return None
