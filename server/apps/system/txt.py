'''
author: TRACYF
python version:3.6
'''
def txtWirte(filePath,contentList):
    '''
    :param filePath: 要写入的txt文件的路径
    :param contentList: 要写入的txt的所有内容,List类型，每一个元素都代表一行内容
    :return: 无
    '''
    fileHandle=open(filePath,mode='w')
    for item in contentList:
        fileHandle.write(item+"\n")
    fileHandle.close()

'''
author: TRACYF
python version:3.6
'''
def txtRead(filePath):
    '''
    :param filePath: 要读取的txt的文件路径
    :return:读取的文件内容
    '''
    fileHandle=open(filePath,encoding="GBK")
    return fileHandle.readlines()