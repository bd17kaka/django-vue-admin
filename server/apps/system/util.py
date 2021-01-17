import paramiko
import time
import winrm
import json
import numpy as np

class ServerByPara(object):
    def __init__(self, cmd, host, user, password, system_choice):
        self.cmd = cmd
        self.client = paramiko.SSHClient()
        self.host = host
        self.user = user
        self.pwd = password
        self.system_choice = system_choice

    def exec_linux_cmd(self):
        data_init = ''
        
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.host, username=self.user, password=self.pwd)
        stdin, stdout, stderr = self.client.exec_command(self.cmd, get_pty=True)
        if stderr.readlines():
            exec_tag = 1
            for data in stdout.readlines():
                data_init += data
        else:
            exec_tag = 0
            for data in stdout.readlines():
                data_init += data
        return json.dumps({
            "exec_tag": exec_tag,
            "data": data_init,
        }, ensure_ascii=False)

    def exec_win_cmd(self):
        data_init = ""
        print("开始连接")
        s = winrm.Session(self.host, auth=(self.user, self.pwd))
        print("连接成功")
        # try:
        ret = s.run_cmd(self.cmd)
        # except:
            
        print(ret)
        encoding="utf-8"
        try: 
            ret.std_err.decode(encoding)
        except:
            encoding="gbk"

        if ret.std_err.decode(encoding):
            exec_tag = 1
            for data in ret.std_err.decode(encoding).split("\r\n"):
                data_init += data
        else:
            exec_tag = 0
            for data in ret.std_out.decode("gbk").split("\r\n"):
                data_init += data
        return json.dumps({
            "exec_tag": exec_tag,
            "data": data_init,
        }, ensure_ascii=False)

    def run(self):
        if self.system_choice == "Linux":
            result = self.exec_linux_cmd()
        else:
            result = self.exec_win_cmd()
        print(result)
        with open(r"script_info.txt", "w") as f:
            f.write(result)

def sendFile(hereFilePath,thereFilePath):
    hostname="10.201.147.111"
    # username = "ADMIN"
    username="dell"
    password = "2019202210088"
    port = 22
    transport = paramiko.Transport((hostname, port))  # 建立远程连接
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    # 上传文件
    print(hereFilePath)
    print(thereFilePath)
    sftp.put(hereFilePath, thereFilePath)