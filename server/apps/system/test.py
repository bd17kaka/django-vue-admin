import time
import os
import sys

import AFD.AFD_Constants as Local_Constants
import utilities.Constants as Constants
from AFD import mts_representation_generator
from AFD.AFD_Main import conduct_single_experiment_on_single_representation
from AFD.AFD_Utils import construct_method_call_tree, pad_method_call_tree, get_dataframe_from_jsontrace, \
    create_representation_generator


def get_trace(dataset_name):
    # print('Start to parse: ' + dataset_name)
    start_time = time.time()
    functionality_names_dict, app_trace_dict = {}, {}
    trace_dict = {}
    Local_Constants.ROOT_DIR=os.getcwd()+"/"
    all_category_dir = Local_Constants.ROOT_DIR + 'archives' + '/' + 'APP_TRACE_Archive_2019'
    category_dir = all_category_dir + '/' + dataset_name + '/'
    functionality_names_dict[dataset_name] = os.listdir(category_dir)
    for app_name in functionality_names_dict[dataset_name]:
        trace_names_list = os.listdir(category_dir + '/' + app_name)
        for trace_name in trace_names_list:
            my_trace_url = category_dir + '/' + app_name + '/' + trace_name
            my_trace_name = dataset_name + '&' + app_name + '&' + trace_name
            # call_method_tree, exceptional_lines = construct_method_call_tree(my_trace_name, my_trace_url)
            begin_time = time.time()
            my_thread_one_df, my_event_eight_df, my_event_nine_df = get_dataframe_from_jsontrace(my_trace_url)
            end_time = time.time()
            app_trace_dict[my_trace_name]=[my_thread_one_df, my_event_eight_df, my_event_nine_df]
            trace_dict[my_trace_name] = round(end_time - begin_time, 6)

    complete_time = time.time()
    run_time = round(complete_time - start_time, 6)
    # trace_list = app_trace_dict.keys()
    # print('Complete to parse: ' + dataset_name + ' using ' + str(complete_time - start_time) + ' seconds!')
    # print(app_trace_dict)

    return app_trace_dict, run_time, trace_dict

# get_trace("Memo")


def create_representation(representation_generator, dataset_dict, category_name):
    '''
    对应的是“生成语义表征”按钮
    :param representation_generator:表征类型，字符串格式，可选项为：'LEVEL_HISTO', 'MCT_MTS', 'MCT_SEMANTIC_MTS'三种
    :param dataset_dict:无用的参数，固定为{}
    :param category_name:app类型，字符串格式，可选项为：'Memo', 'Calendar', 'Photography'
    :return:
    '''
    my_generator=create_representation_generator(representation_generator, {}, category_name)
    my_representations_dict=my_generator.get_all_representations_dict()
    return my_representations_dict

# create_representation("MCT_SEMANTIC_MTS",{},"Memo")

def classifier_fit(batch_size,epochs,classifier_name,category_name,representation_generator):
    '''
    对应的是运行分类器按钮
    :param batch_size: 无意义的参数（后面可能有用）
    :param epochs: 无意义的参数（后面可能有用）
    :param classifier_name: 分类器名称，字符串类型，可选的有：'MLP', 'LSTM', 'FCN', 'ResNet'
    :param category_name: app的名称，字符串类型，可选项为：'Memo', 'Calendar', 'Photography'
    :param representation_generator:表征类型，字符串格式，可选项为：'LEVEL_HISTO', 'MCT_MTS', 'MCT_SEMANTIC_MTS'三种
    :return:None
    '''
    # para=para.replace("[","").replace("]","")
    # para=para.split(",")
    # print(para[0])
    # batch_size=int(para[0])
    # epochs=int(para[1])
    # classifier_name=para[2]
    # category_name=para[3]
    # representation_generator=para[4]
    # print(para)
    my_representations_dict=create_representation(representation_generator,{},category_name)
    for my_representation_key in my_representations_dict.keys():
        my_datasets_dict = my_representations_dict[my_representation_key]
        conduct_single_experiment_on_single_representation("APP_TRACE_Archive_2019",category_name, classifier_name,'DPre',1, my_datasets_dict,representation_generator,my_representation_key)


# classifier_fit(sys.argv[1])
# classifier_fit(0,0,"FCN","Test","MCT_MTS")

