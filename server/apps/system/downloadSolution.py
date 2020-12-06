import os
from zipfile import ZipFile
import shutil


def myOwnZip(zfile,folder,baseDir=""):
    print("folder:",folder)
    print("baseDir:",baseDir)
    fileList=os.listdir(folder)
    for file in fileList:
        if os.path.isfile(os.path.join(folder,file)): # 如果是文件
            zfile.write(os.path.join(folder,file),os.path.join(baseDir,file))
        else:
            zfile.write(os.path.join(folder,file),baseDir+"/"+file) # 创建文件夹
            print(baseDir+"/"+file)
            print("将文件夹",file,"添加到压缩包中")
            # baseFolderName=os.path.basename(folder)
            myOwnZip(zfile,os.path.join(folder,file),baseDir=os.path.join(baseDir,file))

    print('Done.')



def folder2zip(folder,goalFolder):                               #文件夹打包为zip的函数
    zipfile_name = os.path.basename(folder) + '.zip'
    if not os.path.exists(zipfile_name):          #检查压缩包是否存在，如果已存在则询问是否继续
        zfile=ZipFile(zipfile_name,'w')
        myOwnZip(zfile,folder)
        zfile.close()
        shutil.move(zipfile_name,os.path.join(goalFolder,zipfile_name))
    else:
        # response = input("Zipfile exists. Coutinue?('q' for quit): ")
        # if response != 'q':
        os.remove(zipfile_name)
        zfile = ZipFile(zipfile_name, 'w')
        myOwnZip(zfile,folder)
        zfile.close()
        shutil.move(zipfile_name, os.path.join(goalFolder, zipfile_name))

# folder2zip("C:/Users/10073\Desktop/knn","D:/")