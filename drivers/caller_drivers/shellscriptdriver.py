import paramiko


class ShellScriptClient(object):

    def __init__(self, req_host, req_username, req_password, req_timeout):

        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh.connect(req_host, username=req_username, password=req_password, timeout=req_timeout)

    def exec_script(self, cmd):

        try:
            stdin, stdout, stderr = self.__ssh.exec_command(cmd)
            print stdout.read()
            # for std in stdout.readlines():
            #    print std

        except Exception as e:

            pass

        finally:
            self.__ssh.close()