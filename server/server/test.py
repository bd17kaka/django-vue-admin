import paramiko
import time
import os
import shutil
import winrm
import json
import numpy as np
import pymysql
from sklearn.metrics import f1_score,recall_score


hostname="10.201.147.111"
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
    return: tuple类型，每个元素是数据库中的一条记录
    '''
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select * from system_solution where solution_status=%d" %(0)
    # print("查询命令为:",sql)
    cur.execute(sql)
    result = cur.fetchall()
    # print("查询结果为:",result)
    cur.close()
    conn.close()
    return result


def get_dataset_from_task(task_name):
    '''
    task_name: 字符串类型，任务名称
    return: string类型，返单个数据集的名称（因为之前默认是单数据集）
    '''
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select matched_dataset from system_task where task_name='%s'" %(task_name)
    # print("查询命令为:",sql)
    cur.execute(sql)
    result = cur.fetchall()
    # print("查询结果为:",result)
    cur.close()
    conn.close()
    return result[0][0]


def get_datasetname_from_dataset(id):
    '''
    根据数据集id获得数据集的名字
    id: int类型，数据集的id
    '''
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select dataset_name from system_dataset where id=%d" %(id)
    # print("查询dataset_id的sql语句为:",sql)
    cur.execute(sql)
    result=cur.fetchall()
    # print("查询结果为:",result)
    cur.close()
    conn.close()
    return result[0][0]


def get_datasetid_measurementid_from_solution_result(solutionId):
    '''
    从system_solution_result表中获取方案所需要的所有数据集的id以及评价指标的id
    solutionId: int类型
    '''
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select dataset_id,measurement_id from system_solution_result where solution_id=%d" %(solutionId)
    # print("查询dataset_id的sql语句为:",sql)
    cur.execute(sql)
    result=cur.fetchall()
    # print("查询结果为:",result)
    cur.close()
    conn.close()
    return result

def get_measurement_name_from_measurement(measurementid):
    '''
    从system_measurement表中获取指定id对应的评价名称
    measurementid:int类型，评价指标id
    return: 字符串类型，评价指标名称
    '''

    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select name from system_measurement where id=%d" %(measurementid)
    # print("查询dataset_id的sql语句为:",sql)
    cur.execute(sql)
    result=cur.fetchall()
    # print("查询结果为:",result)
    cur.close()
    conn.close()
    return result[0][0]

def get_task_name_from_task(taskid):
    '''
    从system_task表中获取指定id对应的评价名称
    taskid:int类型，评价指标id
    return: 字符串类型，任务名称
    '''
    conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
    cur = conn.cursor()
    sql="select task_name from system_task where id=%d" %(taskid)
    # print("查询dataset_id的sql语句为:",sql)
    cur.execute(sql)
    result=cur.fetchall()
    # print("查询结果为:",result)
    cur.close()
    conn.close()
    # print(result)
    return result[0][0]

def updateSolution(soulutionId,status,result,dataset_id,measurement_id):
    '''
    更改方案运行状态和结果
    '''
    if result is not None:
        # 如果已经有结果了
        conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
        cur = conn.cursor()
        sql="update system_solution_result set solution_result='%s' where solution_id=%d and dataset_id=%d and measurement_id=%d" %(str(result),soulutionId,dataset_id,measurement_id)
        cur.execute(sql)
        conn.commit()
        sql="update system_solution set solution_status=%d where id=%d" %(status,soulutionId)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    else:
        conn = pymysql.connect(host='10.201.200.222', port=3306, user='root', password='123456', db='aishare', charset='utf8')
        cur = conn.cursor()
        sql="update system_solution set solution_status=%d where id=%d" %(status,soulutionId)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()


def locateFile(unusedSolutionTuple):
    '''
    获取还没有运行的方案的方案名，任务名，和id
    unusedSolutionTuple: 未运行的方案tuple
    return: list类型，每个元素是一个tuple（方案名，任务名，id）
    '''
    fileList=[]
    for i in range(len(unusedSolutionTuple)):
        solutionName=unusedSolutionTuple[i][4]
        taskName=get_task_name_from_task(unusedSolutionTuple[i][5])
        id=unusedSolutionTuple[i][0]
        # 拼凑地址
        fileList.append((taskName,solutionName,id))

    return fileList

if __name__ == "__main__":
    # updateSolution(1,2,"123",1,1)
    while True:
        result=getUnused()
        if len(result)>0: # 如果存在未运行的方案
            for item in result: # 对于每一个方案
                dataset_measurement_id_all=get_datasetid_measurementid_from_solution_result(item[0]) # 获取该方案用到的所有数据集和评价指标的id
                for dataset_id,measurement_id in dataset_measurement_id_all:
                    dataset_name=get_datasetname_from_dataset(dataset_id) # 获取这条记录数据集的名称
                    measurement_name=get_measurement_name_from_measurement(measurement_id) # 获取这条记录评价指标的名称
                    taskName=get_task_name_from_task(item[5])
                    solution_id=item[0]
                    solutionName=item[4]+".zip"

                    # 知道了方案名，所属任务名，数据集，评价指标名称就可以开始运行代码了
                    print("方案名为",item[4],"所属任务:",taskName,"数据集为:",dataset_name,"评价指标为:",measurement_name)
                    folder=taskName # 任务名称也是codes子文件夹的名称
                    updateSolution(solution_id,1,None,dataset_id,measurement_id) # 在运行之前先把方案改为正在运行
                    absFolderPath=os.path.join("/proj/django-vue-admin/server/media/codes",folder) # 所有该任务的代码都存在这个文件夹下
                    zippedFilePath=os.path.join(absFolderPath,solutionName) # 获得方案文件的绝对路径
                    print("该方案文件夹所在地址:",zippedFilePath)

                    # 发送方案到计算服务器
                    print("发送文件到计算服务器")
                    sendFile('/proj/django-vue-admin/server/media/codes/'+folder+'/'+solutionName,r"D:/"+solutionName) # 把压缩包送到计算服务器D盘根目录
                    print("发送成功")
                    
                    # 远程解压方案到计算服务器指定位置
                    print("运行解压程序")
                    print("python D:/unzip.py "+"D:/"+solutionName+" D:/codes/"+folder) # 让计算服务器把代码解压到指定位置
                    server_obj = ServerByPara("python D:/unzip.py "+"D:/"+solutionName+" D:/codes/"+folder, hostname, username, password, "windows")
                    server_obj.run()
                    time.sleep(3)
                    # 上传完成后执行命令
                    goalFolder=os.path.join("D:/codes/"+folder,solutionName.replace(".zip",""))
                    goalFile=os.path.join(goalFolder,"main.py")
                    print("开始运行的文件是:",goalFile)
                    server_obj = ServerByPara("python "+goalFile+" D:/data/"+dataset_name.replace(".zip","")+"/train.csv"+" D:/data/"+dataset_name.replace(".zip","")+"/test.csv", hostname, username, password, "windows")
                    server_obj.run()
                    print("运行成功")

                    fileHandle=open("script_info.txt","r")
                    # 获取预测结果list
                    for line in fileHandle.readlines():
                        resultDict=json.loads(line)
                    data=resultDict["data"].replace("[","")
                    data=data.replace("]","")
                    resultList=data.split(",")
                    for i in range(len(resultList)):
                        resultList[i]=float(resultList[i])
                    print("预测结果:",resultList)
                    test_tag=getTestTag("/proj/django-vue-admin/server/server/dataset/"+dataset_name.replace(".zip","")+"/test_tag.csv")
                    if measurement_name=="accuracy":
                        rightCount=0
                        for i in range(len(test_tag)):
                            print(test_tag[i])
                            print(resultList[i])
                            if float(test_tag[i])==resultList[i]:
                                rightCount+=1
                        print("任务",folder,"方案",solutionName,"的accuracy:",rightCount/len(test_tag))
                        updateSolution(solution_id,2,rightCount/len(test_tag),dataset_id,measurement_id)
                    elif measurement_name=="F1-score":
                        score=f1_score(test_tag,resultList,average='micro')
                        print("任务",folder,"方案",solutionName,"的f1-score:",score)
                        updateSolution(solution_id, 2, score, dataset_id, measurement_id)
                    elif measurement_name=="recall":
                        score=recall_score(test_tag, resultList, average='macro')
                        print("任务",folder,"方案",solutionName,"的recall_score:",score)
                        updateSolution(solution_id, 2, score, dataset_id, measurement_id)


        else:
            print("无待运行的方案")
            time.sleep(10)

                


