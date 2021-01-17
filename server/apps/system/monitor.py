import os
import time
from test import create_representation

def txtRead(filePath):
    '''
    :param filePath: 要读取的txt的文件路径
    :return:读取的文件内容
    '''
    fileHandle=open(filePath,encoding="GBK")
    return fileHandle.readlines()

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

# def create_representation(representation_generator, dataset_dict, category_name):
#     '''
#     对应的是“生成语义表征”按钮
#     :param representation_generator:表征类型，字符串格式，可选项为：'LEVEL_HISTO', 'MCT_MTS', 'MCT_SEMANTIC_MTS'三种
#     :param dataset_dict:无用的参数，固定为{}
#     :param category_name:app类型，字符串格式，可选项为：'Memo', 'Calendar', 'Photography'
#     :return:
#     '''
#     my_generator=create_representation_generator(representation_generator, {}, category_name)
#     my_representations_dict=my_generator.get_all_representations_dict()
#     return my_representations_dict

while True:
    curr_path=os.getcwd()
    # print(curr_path)#D:\codes\django-vue-admin\server\apps\system
    curr_path=os.path.dirname(curr_path)
    curr_path=os.path.dirname(curr_path)
    # print(curr_path)
    fileList=os.listdir(curr_path) 
    # print(fileList)
    if "representations.txt" in fileList:
        begin_time = time.time()
        filePath=os.path.join(curr_path,"representations.txt")
        theList=txtRead(filePath)
        representation_generator = theList[0].replace("\n","")
        category_name = theList[1].replace("\n","")
        my_representations_dict = {}
        my_representations_dict = create_representation(representation_generator, {}, category_name)
        os.remove(filePath)
        end_time = time.time()
        run_time = round(end_time - begin_time, 6)
        timePath = os.path.join(curr_path,"representation_time.txt")
        txtWirte(timePath, [str(run_time)])
    else:
        time.sleep(2)