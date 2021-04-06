import paramiko
import time
import os
import shutil
import winrm
import json
import numpy as np
import pymysql

# hostname="10.201.147.111"
# username="dell"
# password="2019202210088"

# hostname = "172.20.10.2"
hostname="10.201.147.111"
# username = "ADMIN"
username="dell"
password = "2019202210088"

port = 22

transport = paramiko.Transport((hostname, port))  # 建立远程连接
transport.connect(username=username, password=password)

sftp = paramiko.SFTPClient.from_transport(transport)

def getDirName(filePath):
    '''
    获取所在文件夹名称
    :param filePath:str类型，文件的绝对路径
    :return: 文件所在的文件夹的名称
    '''
    filePath=filePath.replace("/","\\")
    nameList=filePath.split("\\")
    nameList[-2]=nameList[-2].replace("\\","")
    return nameList[-2]


def getFile(filePath,resultList):
    filesList = os.listdir(filePath)  # 列出文件夹下所有的目录与文件
    # print(len(filesList))  # len(filesList)包含了目录数
    for i in range(0, len(filesList)):
        path = os.path.join(filePath, filesList[i])
        # print('该文件路径为：', path)
        if os.path.isfile(path):  # 判断是否为文件
            # print((filePath,filesList[i]))
            dirName=getDirName(path)
            resultList.append((dirName,filesList[i]))
        else:
            getFile(path,resultList)



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
    # 上传文件
    print(hereFilePath)
    print(thereFilePath)
    sftp.put(hereFilePath, thereFilePath)

def backupFile(originalFile,goalPath,file):
    print("开始执行备份")
    print("目标文件夹:",goalPath)
    if not os.path.exists(goalPath):
        print("不存在文件路径:",goalPath,"开始创建")
        os.mkdir(goalPath)
    shutil.move(originalFile, os.path.join(goalPath,file))

def getTestTag(test_tag_path):
    test_tag=np.loadtxt(test_tag_path)
    return test_tag


def getUnused():
    '''
    获取没有运行的方案
    '''
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select * from system_solution where solution_status=%d" %(0)
    print("查询命令为:",sql)
    cur.execute(sql)
    result = cur.fetchall()
    print("查询结果为:",result)
    cur.close()
    conn.close()
    return result

def locateFile(unusedSolutionTuple):
    '''
    unusedSolutionTuple: 未运行的方案tuple
    '''
    fileList=[]
    for i in range(len(unusedSolutionTuple)):
        solutionName=unusedSolutionTuple[i][4]
        taskName=unusedSolutionTuple[i][5]
        id=unusedSolutionTuple[i][0]
        
        # 拼凑地址
        # print("folder:",taskName)
        # print("fileName:",solutionName)
        fileList.append((taskName,solutionName,id))
    return fileList

def get_dataset_from_task(task_name):
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select matched_dataset from system_task where task_name='%s'" %(task_name)
    print("查询命令为:",sql)
    cur.execute(sql)
    result = cur.fetchall()
    print("查询结果为:",result)
    cur.close()
    conn.close()
    return result[0][0]

def updateSolution(soulutionId,status,result):
    '''
    更改方案运行状态和结果
    '''
    
    if result is not None:
        # 如果已经有结果了
        conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
        cur = conn.cursor()
        sql="update system_solution set solutionResult='%s' where solutionId=%d" %(str(result),soulutionId)
        cur.execute(sql)
        conn.commit()
        sql="update system_solution set solution_status=%d where solutionId=%d" %(status,soulutionId)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    else:
        conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
        cur = conn.cursor()
        sql="update system_solution set solution_status=%d where solutionId=%d" %(status,soulutionId)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()


# 首先检查指定文件夹是否有文件
codesPath="/proj/django-vue-admin/server/media/codes"
while True:
    # fileList=[]
    unusedSolutionTuple=getUnused()
    fileList=locateFile(unusedSolutionTuple)
    
    # getFile("/proj/django-vue-admin/server/server/codes",fileList) # 获取方案文件及其任务名
    if len(fileList)>0: # 如果有文件就把所有文件都上传到计算服务器
        print("存在文件")
        for folder,file,solution_id in fileList:
            print("任务文件夹:",folder) # 任务名
            datasetName=get_dataset_from_task(folder)
            print("使用的数据集:",datasetName)
            file=file.replace(folder+"_","")
            file=file+".zip"
            print("方案文件名:",file) # 方案文件
            fileName=file.split(".")[0] # 提取方案名(也就是学号)
            updateSolution(solution_id,1,None)

            absFolderPath=os.path.join("/proj/django-vue-admin/server/media/codes",folder)
            zippedFilePath=os.path.join(absFolderPath,file)
            print("zippedFilePath:",zippedFilePath)
            sendFile('/proj/django-vue-admin/server/media/codes/'+folder+'/'+file,r"D:/"+file) # 把压缩包送到计算服务器D盘根目录
            print("发送成功")
            backupFile(zippedFilePath,os.path.join("/proj/django-vue-admin/server/media/codes",folder),file)
            # 运行解压程序
            print("运行解压程序")
            print("python D:/unzip.py "+"D:/"+file+" D:/codes/"+folder) # 让计算服务器把代码解压到指定位置
            server_obj = ServerByPara("python D:/unzip.py "+"D:/"+file+" D:/codes/"+folder, hostname, username, password, "windows")
            server_obj.run()
            time.sleep(3)
            # 上传完成后执行命令
            goalFolder=os.path.join("D:/codes/"+folder,fileName)
            goalFile=os.path.join(goalFolder,"main.py")
            print("开始运行的文件是:",goalFile)
            server_obj = ServerByPara("python "+goalFile+" D:/data/"+datasetName+"/train.csv"+" D:/data/"+datasetName+"/test.csv", hostname, username, password, "windows")
            server_obj.run()
            fileHandle=open("script_info.txt","r")
            for line in fileHandle.readlines():
                resultDict=json.loads(line)
            print(type(resultDict["data"]))
            data=resultDict["data"].replace("[","")
            data=data.replace("]","")
            print(data)
            resultList=data.split(",")
            # data=list(data)
            for i in range(len(resultList)):
                resultList[i]=float(resultList[i])
            print(resultList)
            print(data)
            test_tag=getTestTag("/proj/django-vue-admin/server/server/dataset/"+datasetName+"/test_tag.csv")
            rightCount=0
            for i in range(len(test_tag)):
                print(test_tag[i])
                print(resultList[i])
                if float(test_tag[i])==resultList[i]:
                    rightCount+=1
            print("任务",folder,"方案",file,"的accuracy:",rightCount/len(test_tag))
            updateSolution(solution_id,2,rightCount/len(test_tag))
    else:
        print("未扫描到文件")
        time.sleep(10)
