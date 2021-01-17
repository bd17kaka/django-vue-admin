import os
import time
from test import classifier_fit
import pandas as pd
import matplotlib.pyplot as plt
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

def plot_doubleY(csvPath,savedPath,label1,label2):
    '''
    对指定的csv，指定的列名，绘制双Y轴图像
    :param csvPath: 待读取的csv的文件路径，str类型
    :param savedPath: 要保存的png的路径，例如"test.png",str类型
    :param label1: 要读取哪一列的数据的列明，例如"accuracy"，"loss"等，str类型
    :param label2: 同上
    :return: None
    '''
    allData = pd.read_csv(csvPath)
    loss = allData[label1]
    acc = allData[label2]
    x = [i for i in range(loss.shape[0])]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x, loss, 'r', label="loss")
    ax1.legend(loc=1)
    ax1.set_ylabel('loss values')
    ax1.set_xlabel('epochs')
    ax2 = ax1.twinx()  # this is the important function
    ax2.plot(x, acc, 'g', label="accuracy")
    ax2.legend(loc=2)
    # ax2.set_xlim([0, np.e])
    ax2.set_ylabel('accuracy values')
    plt.savefig(savedPath)
    # plt.show()

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
    curr_path=os.path.dirname(curr_path)
    curr_path=os.path.dirname(curr_path)
    pngPath = curr_path + '/media/' + 'result.png'
    fileList=os.listdir(curr_path) 
    if "classifier_para.txt" in fileList:
        filePath=os.path.join(curr_path,"classifier_para.txt")
        para=txtRead(filePath)
        batch_size=int(para[0].replace("\n",""))
        epochs=int(para[1].replace("\n",""))
        classifier_name=para[2].replace("\n","")
        category_name=para[3].replace("\n","")
        representation_generator=para[4].replace("\n","")
        print(classifier_name,category_name,representation_generator)

        begin_time = time.time()
        classifier_fit(0,0,classifier_name,category_name,representation_generator)
        end_time = time.time()
        run_time = round(end_time - begin_time, 6)
        statusPath = os.path.join(curr_path, "status.txt")

        #绘制结果图
        result_path=os.path.join(curr_path,"apps","system","detailed_results")
        result_path=os.path.join(result_path,classifier_name)
        result_path=os.path.join(result_path,"APP_TRACE_Archive_20191")
        result_path=os.path.join(result_path,category_name)
        result_path=os.path.join(result_path,"DPre")
        result_path=os.path.join(result_path,representation_generator)
        final_folder = os.listdir(result_path)[-1]
        result_path=os.path.join(result_path, final_folder)
        result_path=os.path.join(result_path, "history.csv")
        # print("*****************", result_path)
        plot_doubleY(result_path, pngPath, "loss", "accuracy")

        txtWirte(statusPath, ['done', str(run_time)])
        os.remove(filePath)
    else:
        print("No Classifer to run")
        time.sleep(2)