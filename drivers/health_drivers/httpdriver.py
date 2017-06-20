import sys
import os
import requests
import traceback
from health_drivers_log import info, warn, error, debug

def check_http_service_health(url):
    ret = False
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            ret = True
    except Exception as ex:
        ret = False
        error(traceback.format_exc())
        error(ex)
    return ret

def check_health_with_policy(argument_spec):
    url = argument_spec['URL']
    ret = check_http_service_health(url)
    return ret
