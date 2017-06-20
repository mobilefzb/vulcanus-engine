import sys
import os
import paramiko
import traceback
from health_drivers_log import info, warn, error, debug

def check_remote_shell_script_health(keyword, usr, pwd, host, port=22):
    ret = False
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, usr, pwd)
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep %s | grep -v grep" % (keyword), timeout=10)
        stdout_str = stdout.read()
        if stdout_str:
            ret = True
    except Exception as ex:
        ret = False
        error(traceback.format_exc())
        error(ex)
    return ret

def check_health_with_policy(argument_spec):
    host = argument_spec['ServerHost']
    usrname = argument_spec['Username']
    passwd = argument_spec['Password']
    keyword = argument_spec['Cmd']
    ret = check_remote_shell_script_health(keyword, usrname, passwd, host)
    return ret
