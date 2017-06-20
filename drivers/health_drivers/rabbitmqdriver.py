import sys
import os
import pika
import traceback
from health_drivers_log import info, warn, error, debug

def check_rabbitmq_service_health(conn_str):
    ret = False
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(conn_str))
        ret = True
        connection.close()
    except Exception as ex:
        ret = False
        error(traceback.format_exc())
        error(ex)
    return ret

def check_health_with_policy(argument_spec):
    conn_str = argument_spec['BrokerServerHost']
    ret = check_rabbitmq_service_health(conn_str)
    return ret
