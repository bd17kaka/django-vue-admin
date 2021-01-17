import logging
import os
import time
import subprocess
from pathlib import Path
import pandas as pd
import shutil
import pymysql

import paramiko
import time
import winrm
import json
import numpy as np
from .downloadSolution import folder2zip
from . import system_settings

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect,HttpResponse
from django.core.cache import cache
from django_celery_beat.models import PeriodicTask
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import (FileUploadParser, JSONParser,
                                    MultiPartParser)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from utils.queryset import get_child_queryset2
import urllib.request

from .filters import UserFilter
from .mixins import CreateUpdateModelAMixin, CreateUpdateModelBMixin
from .models import (Dict, DictType, File, Organization, Permission, Position,
                     Role, User, Measurement, Task, Dataset, Solution, Tasktype,
                     task_type_measument, task_dataset_measurement, solution_result)
from .permission import RbacPermission, get_permission_list
from .permission_data import RbacFilterSet
from .serializers import (DictSerializer, DictTypeSerializer, FileSerializer,
                          OrganizationSerializer, PermissionSerializer,
                          PositionSerializer, RoleSerializer, TaskSerializer,
                          UserCreateSerializer, UserListSerializer,
                          UserModifySerializer, MeasurementSerializer, DatasetSerializer, SolutionSerializer, TasktypeSerializer,
                          task_type_measurementSerializer, task_dataset_measurementSerializer, solution_resultSerializer)

from .test import get_trace, create_representation, classifier_fit
from .txt import txtWirte, txtRead

logger = logging.getLogger('log')
# logger.info('请求成功！ response_code:{}；response_headers:{}；response_body:{}'.format(response_code, response_headers, response_body[:251]))
# logger.error('请求出错-{}'.format(error))

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

class LogoutView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):  # 可将token加入黑名单
        return Response(status=status.HTTP_200_OK)

# class TaskViewSet(ModelViewSet):
#     queryset = PeriodicTask.objects.all()
#     serializer_class = TaskSerializer
#     search_fields = ['name']
#     filterset_fields = ['enabled']
#     ordering = ['-pk']



class DictTypeViewSet(ModelViewSet):
    """
    数据字典类型-增删改查
    """
    perms_map = {'get': '*', 'post': 'dicttype_create',
                 'put': 'dicttype_update', 'delete': 'dicttype_delete'}
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['pk']
    ordering = ['pk']


class DictViewSet(ModelViewSet):
    """
    数据字典-增删改查
    """
    perms_map = {'get': '*', 'post': 'dict_create',
                 'put': 'dict_update', 'delete': 'dict_delete'}
    # queryset = Dict.objects.get_queryset(all=True) # 获取全部的,包括软删除的
    queryset = Dict.objects.all()
    filterset_fields = ['type', 'is_used', 'type__code']
    serializer_class = DictSerializer
    search_fields = ['name']
    ordering_fields = ['sort']
    ordering = ['sort']

    def paginate_queryset(self, queryset):
        """
        如果查询参数里没有page但有type或type__code时则不分页,否则请求分页
        """
        if self.paginator is None:
            return None
        elif (not self.request.query_params.get('page', None)) and ((self.request.query_params.get('type__code', None)) or (self.request.query_params.get('type', None))):
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    @action(methods=['get'], detail=False, permission_classes=[], authentication_classes=[],url_name='correct_dict')
    def correct(self, request, pk=None):
        for i in Dict.objects.all():
            i.save()
        return Response(status=status.HTTP_200_OK)

class PositionViewSet(ModelViewSet):
    """
    岗位-增删改查
    """
    perms_map = {'get': '*', 'post': 'position_create',
                 'put': 'position_update', 'delete': 'position_delete'}
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    pagination_class = None
    search_fields = ['name','description']
    ordering_fields = ['pk']
    ordering = ['pk']


class TestView(APIView):
    perms_map = {'get': 'test_view'}  # 单个API控权
    pass


class PermissionViewSet(ModelViewSet):
    """
    权限-增删改查
    """
    perms_map = {'get': '*', 'post': 'perm_create',
                 'put': 'perm_update', 'delete': 'perm_delete'}
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['sort']
    ordering = ['pk']


class OrganizationViewSet(ModelViewSet):
    """
    组织机构-增删改查
    """
    perms_map = {'get': '*', 'post': 'org_create',
                 'put': 'org_update', 'delete': 'org_delete'}
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = None
    search_fields = ['name', 'method']
    ordering_fields = ['pk']
    ordering = ['pk']


class RoleViewSet(ModelViewSet):
    """
    角色-增删改查
    """
    perms_map = {'get': '*', 'post': 'role_create',
                 'put': 'role_update', 'delete': 'role_delete'}
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['pk']
    ordering = ['pk']


class UserViewSet(ModelViewSet):
    """
    用户管理-增删改查
    """
    perms_map = {'get': '*', 'post': 'user_create',
                 'put': 'user_update', 'delete': 'user_delete'}
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filterset_class = UserFilter
    search_fields = ['username', 'name', 'phone', 'email']
    ordering_fields = ['-pk']

    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.get_serializer_class(), 'setup_eager_loading'):
            queryset = self.get_serializer_class().setup_eager_loading(queryset)  # 性能优化
        dept = self.request.query_params.get('dept', None)  # 该部门及其子部门所有员工
        if dept is not None:
            deptqueryset = get_child_queryset2(Organization.objects.get(pk=dept))
            queryset = queryset.filter(dept__in=deptqueryset)
        return queryset

    def get_serializer_class(self):
        # 根据请求类型动态变更serializer
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserModifySerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        #print(request.data['file'])
        if(request.data['file'] == None):
            # 创建用户默认添加密码
            password = request.data['password'] if 'password' in request.data else None
            if password:
                password = make_password(password)
            else:
                password = make_password('0000')
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(password=password)
            # from apps.employee.models import Employee
            # Employee.objects.create(user=instance,create_by=request.user)
            return Response(serializer.data)
        
        else:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            parent_path = os.path.dirname(current_dir)
            parent_path = os.path.dirname(parent_path)
            path = parent_path + '/media/' + request.data['file']
            allData = pd.read_excel(path)
            Number = allData["学号"]
            Name = allData["姓名"]
            #Dept = allData["部门"]
            #Role = allData["角色"]
            for number,name in zip(Number,Name):
                tempDict={}
                tempDict["id"]=''
                tempDict["name"]=name
                tempDict["username"]=number
                tempDict["dept"]=None
                tempDict["avatar"]='/media/default/avatar.png'
                tempDict["dept"]=request.data['dept']
                tempDict["roles"] = request.data['roles']
                print(tempDict)
                password = make_password('0000')
                serializer = self.get_serializer(data = tempDict)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save(password=password)
                # from apps.employee.models import Employee
                # Employee.objects.create(user=instance,create_by=request.user)
            return Response('批量新增成功', status=status.HTTP_200_OK)
        

    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated], # perms_map={'put':'change_password'}
            url_name='change_password')
    def password(self, request, pk=None):
        """
        修改密码
        """
        user = request.user
        old_password = request.data['old_password']
        if check_password(old_password, user.password):
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password2)
                user.save()
                return Response('密码修改成功!', status=status.HTTP_200_OK)
            else:
                return Response('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)

    # perms_map={'get':'*'}, 自定义action控权
    @action(methods=['get'], detail=False, url_name='my_info', permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        """
        初始化用户信息
        """
        user = request.user
        perms = get_permission_list(user)
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'roles': user.roles.values_list('name', flat=True),
            # 'avatar': request._request._current_scheme_host + '/media/' + str(user.image),
            'avatar': user.avatar,
            'perms': perms,
        }
        return Response(data)

class FileViewSet(CreateUpdateModelBMixin, ModelViewSet):
    """
    文件-增删改查
    """
    perms_map = {'get': '*', 'post': 'file_create',
                 'put': 'file_update', 'delete': 'file_delete'}
    parser_classes = [MultiPartParser, JSONParser]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filterset_fields = ['type']
    search_fields = ['name']
    ordering = ['-create_time']
    def sendFile(self,hereFilePath,thereFilePath):
        hostname = system_settings.hostname
        # username = "ADMIN"
        username = system_settings.username
        password = system_settings.password
        port = system_settings.port
        transport = paramiko.Transport((hostname, port))  # 建立远程连接
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 上传文件
        print(hereFilePath)
        print(thereFilePath)
        sftp.put(hereFilePath, thereFilePath)
    
    def perform_create(self, serializer):
        fileobj = self.request.data.get('file')
        print("******", self.request.data)
        name = fileobj._name
        #print(name)
        size = fileobj.size
        mime = fileobj.content_type
        type = '其它'
        if 'image' in mime:
            type = '图片'
        elif 'video' in mime:
            type = '视频'
        elif 'audio' in mime:
            type = '音频'
        elif 'application' or 'text' in mime:
            type = '文档'
        
        instance = serializer.save(create_by = self.request.user, name=name, size=size, type=type, mime=mime)
        instance.path = settings.MEDIA_URL + name
        instance.save()
        # if '_' in name:
        #     dir_name, file_name = name.split('_')

        #     current_path = os.path.abspath(os.path.dirname(__file__))
        #     parent_path = os.path.dirname(current_path)
        #     parent_path = os.path.dirname(parent_path)
        #     #media_path = parent_path + '\\media'
        #     media_path = os.path.join(parent_path, 'media')
        #     #dir_path = media_path + '\\codes\\' + dir_name
        #     dir_path = os.path.join(media_path, 'codes', dir_name)
        #     #print(dir_path)
        #     instance = serializer.save(create_by = self.request.user, name=name, size=size, type=type, mime=mime)
        #     #instance.path = settings.MEDIA_URL + dir_name + '/' + file_name
        #     instance.path = os.path.join(settings.MEDIA_URL, dir_name, file_name)
        #     print(instance.path)
        #     instance.save()
        #     if not os.path.exists(dir_path):
        #         os.makedirs(dir_path)
        #     shutil.copy(os.path.join(media_path,name),os.path.join(dir_path,file_name))
            # os.remove(os.path.name)
        # elif '-' in name:

        #     dir_name, file_name = name.split('-') #dataset-iris
        
        #     current_path = os.path.abspath(os.path.dirname(__file__))
        #     parent_path = os.path.dirname(current_path)
        #     parent_path = os.path.dirname(parent_path)
        #     #media_path = parent_path + '\\media'
        #     media_path = os.path.join(parent_path, 'media')
        #     #dir_path = media_path + '\\codes\\' + dir_name
        #     dir_path = os.path.join(media_path, 'dataset', dir_name)
        #     #print(dir_path)
        #     instance = serializer.save(create_by = self.request.user, name=name, size=size, type=type, mime=mime)
        #     #instance.path = settings.MEDIA_URL + dir_name + '/' + file_name
        #     instance.path = os.path.join(settings.MEDIA_URL, 'dataset', dir_name, file_name)
        #     print(instance.path)
        #     instance.save()
        #     if not os.path.exists(dir_path):
        #         os.makedirs(dir_path)
        #     shutil.copy(os.path.join(media_path,name),os.path.join(dir_path,file_name))
        #     # os.remove(os.path.name)
            # if 'dataset' in name:
            #     hostname=system_settings.hostname
            #     username=system_settings.username
            #     password = system_settings.password
            #     port = system_settings.port
            #     #self.sendFile('D:\codes\django-vue-admin\server/'+instance.path, "D:/"+file_name)
            #     self.sendFile('/proj/django-vue-admin/server/' + instance.path, "D:/"+file_name)
            #     server_obj = ServerByPara("python D:/unzip.py "+"D:/"+file_name+" D:/data/"+file_name.replace('.zip',''), hostname, username, password, "windows")
            #     server_obj.run()
            #     print("运行完毕")
                
        

class MeasurementViewSet(ModelViewSet):
    """
    评价指标管理-增删改查
    """
    perms_map = {'get': '*', 'post': 'measurement_create',
                 'put': 'measurement_update', 'delete': 'measurement_delete'}
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    pagination_class = None
    search_fields = ['name']
    ordering_fields = ['sort']
    ordering = ['pk']


class TaskViewSet(RbacFilterSet, ModelViewSet):
    '''
    任务-增删改查
    '''
    perms_map = {'get': '*', 'post': 'task_create',
                 'put': 'task_update', 'delete': 'task_delete'}
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # pagination_class = None
    search_fields = ['task_name','description']
    ordering_fields = ['pk']
    ordering = ['pk']

    def get_task_id(self,task_name):
        '''
        获取任务id
        '''
        conn = pymysql.connect(host=system_settings.mysql_host, port=system_settings.mysql_port, 
        user=system_settings.mysql_user, password=system_settings.mysql_password, db='aishare', charset='utf8')
        cur = conn.cursor()
        print("连接成功")
        sql="select id from system_task where task_name='%s'" %(task_name)
        print("查询命令为:",sql)
        cur.execute(sql)
        result = cur.fetchall()
        print("查询结果为:",result)
        cur.close()
        conn.close()
        return result[0][0]

    def create(self, request, *args, **kwargs):
        print(*args, "  ", **kwargs)
        print(type(request),request)
        serializer = self.get_serializer(data=request.data)
        # print("类型：",type(request.data))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # {'id': '', 'task_name': 'test3', 'task_measurement': [1], 
        # 'task_type_id': 1, 'matched_dataset': 1, 
        # 'description': '123'}
        print(request.data)
        task_id = self.get_task_id(request.data["task_name"])
        for dataset_temp in request.data["matched_dataset"]:
            #print(dataset_temp)
            for measurement_temp in request.data["task_measurement"]:
                #print(measurement_temp)
                # to_be_stored_data['dataset_id']=dataset_temp
                # to_be_stored_data['measurement_id']=measurement_temp
                # print(to_be_stored_data)
                task_dataset_measurement.objects.create(task_id = task_id, dataset_id = dataset_temp,
                measurement_id = measurement_temp)
                # self.t_d_mea = task_dataset_measurementViewSet()
                # self.t_d_mea.create(request=to_be_stored_data)
                # self.t_d_mea_serializer = self.t_d_mea.get_serializer(data=to_be_stored_data)
                # self.t_d_mea_serializer.is_valid(raise_exception=True)
                # self.t_d_mea.perform_create(self.t_d_mea_serializer)
                print("多表保存成功")
       
        
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # def perform_create():

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        #获得要删除的任务id
        theStringRequest=str(request._request)
        theStringRequest=theStringRequest.replace("/"," ")
        print(theStringRequest)
        theID=theStringRequest.split(" ")[-2]

        #删除该任务下的所有方案
        query_result = Solution.objects.filter(task_id = int(theID))
        for temp_solution in query_result:
            query_solution_result = solution_result.objects.filter(solution_id = temp_solution.id)
            for temp_result in query_solution_result:
                temp_result.is_deleted=1
                temp_result.save()
            temp_solution.is_deleted=1
            temp_solution.save()

        #删除该任务与数据集和评价指标的匹配信息
        query_result = task_dataset_measurement.objects.filter(task_id = int(theID))
        for temp_match in query_result:
            temp_match.is_deleted=1
            temp_match.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        # partial=False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        task_id = self.get_task_id(request.data["task_name"])

        task_dataset_measurement.objects.filter(task_id=task_id).delete()
        for dataset_temp in request.data["matched_dataset"]:
            for measurement_temp in request.data["task_measurement"]:
                task_dataset_measurement.objects.create(task_id = task_id, dataset_id = dataset_temp,
                measurement_id = measurement_temp)



        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
        
class DatasetViewSet(ModelViewSet):
    '''
    数据集-增删改查
    '''
    perms_map = {'get': '*', 'post': 'dataset_create',
                 'put': 'dataset_update', 'delete': 'dataset_delete'}
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    # pagination_class = None
    search_fields = ['dataset_name']
    ordering_fields = ['pk']
    ordering = ['pk']
    def sendFile(self,hereFilePath,thereFilePath):
        hostname = system_settings.hostname
        # username = "ADMIN"
        username = system_settings.username
        password = system_settings.password
        port = system_settings.port
        transport = paramiko.Transport((hostname, port))  # 建立远程连接
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        # 上传文件
        print(hereFilePath)
        print(thereFilePath)
        sftp.put(hereFilePath, thereFilePath)
        
    def create(self, request, *args, **kwargs):
        #保存文件
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(request.data)
        filename = request.data["dataset_name"] + ".zip"
        #获取media路径
        current_path = os.path.abspath(os.path.dirname(__file__))
        parent_path = os.path.dirname(current_path)
        parent_path = os.path.dirname(parent_path)
        media_path = os.path.join(parent_path, 'media')
        obj_path = media_path + "/dataset/dataset"
        if not os.path.exists(obj_path):
            os.makedirs(obj_path)
        shutil.move(os.path.join(media_path, filename), os.path.join(obj_path, filename))

        #发送到计算服务器
        hostname=system_settings.hostname
        username=system_settings.username
        password = system_settings.password
        port = system_settings.port
        #self.sendFile('D:\codes\django-vue-admin\server/'+instance.path, "D:/"+file_name)
        self.sendFile(os.path.join(obj_path, filename), "D:/"+filename)
        server_obj = ServerByPara("python D:/unzip.py "+"D:/"+filename+" D:/data/", hostname, username, password, "windows")
        server_obj.run()
        print("运行完毕")

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        parent_path = os.path.dirname(current_dir)
        parent_path = os.path.dirname(parent_path)
        # os.remove(parent_path+'/media/'+instance.dataset_name+'.zip')
        instance.delete()


class SolutionViewSet(RbacFilterSet, ModelViewSet):
    """
    方案管理-增删改查
    """
    perms_map = {'get': '*', 'post': 'solution_create',
                 'put': 'solution_update', 'delete': 'solution_delete'}
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    # pagination_class = None
    # filterset_class = UserFilter
    search_fields = ['solutionId','solutionName', 'taskName']
    ordering_fields = ['pk']
    ordering=['pk']

    def get_task_name(self,task_id):
        '''
        获取任务name
        '''
        conn = pymysql.connect(host=system_settings.mysql_host, port=system_settings.mysql_port, 
        user=system_settings.mysql_user, password=system_settings.mysql_password, db='aishare', charset='utf8')
        cur = conn.cursor()
        print("连接成功")
        sql="select task_name from system_task where id=%d" %(task_id)
        print("查询命令为:",sql)
        cur.execute(sql)
        result = cur.fetchall()
        print("查询结果为:",result)
        cur.close()
        conn.close()
        return result[0][0]

    def get_solution_id(self,solutionName):
        '''
        获取方案id
        '''
        conn = pymysql.connect(host=system_settings.mysql_host, port=system_settings.mysql_port, 
        user=system_settings.mysql_user, password=system_settings.mysql_password, db='aishare', charset='utf8')
        cur = conn.cursor()
        print("连接成功")
        sql="select id from system_solution where solutionName='%s'" %(solutionName)
        print("查询命令为:",sql)
        cur.execute(sql)
        result = cur.fetchall()
        print("查询结果为:",result)
        cur.close()
        conn.close()
        return result[0][0]

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        solution_id = self.get_solution_id(request.data["solutionName"])
        for dataset_temp in request.data["dataset_id"]:
            for measurement_temp in request.data["measurement_id"]:
                s_r_obj = solution_result.objects.create(solution_id = solution_id, dataset_id = dataset_temp,
                measurement_id = measurement_temp)
                print("多表保存成功")
        headers = self.get_success_headers(serializer.data)

        filename = request.data["solutionName"] + ".zip"

        # 获取media路径
        current_path = os.path.abspath(os.path.dirname(__file__))
        parent_path = os.path.dirname(current_path)
        parent_path = os.path.dirname(parent_path)
        media_path = os.path.join(parent_path, 'media')

        foldername = self.get_task_name(request.data["task_id"])
        print(foldername)
        obj_path = media_path + "/codes/" + foldername
        if not os.path.exists(obj_path):
            os.makedirs(obj_path)
        shutil.move(os.path.join(media_path, filename), os.path.join(obj_path, filename))

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        #获得要删除的方案id
        theStringRequest=str(request._request)
        theStringRequest=theStringRequest.replace("/"," ")
        print(theStringRequest)
        theID=theStringRequest.split(" ")[-2]
        #print(theID)

        instance = self.get_object()
        self.perform_destroy(instance)

        query_result = solution_result.objects.filter(solution_id = int(theID))
        #print(solution_result)
        for temp_solution in query_result:
            temp_solution.is_deleted=1
            temp_solution.save()
            # print(temp_solution.)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TasktypeViewSet(ModelViewSet):
    '''
    任务类型-增删改查
    '''
    perms_map = {'get': '*', 'post': 'tasktype_create',
                 'put': 'tasktype_update', 'delete': 'tasktype_delete'}
    queryset = Tasktype.objects.all()
    serializer_class = TasktypeSerializer
#   pagination_class = None
    search_fields = ['tasktype_name','tasktype_description']
    ordering_fields = ['pk']
    ordering = ['pk']

class task_type_measurementViewSet(ModelViewSet):
    queryset = task_type_measument.objects.all()
    serializer_class = task_type_measurementSerializer
    search_fields = ["id"]
    ordering_fields = ['pk']
    ordering = ['pk']

class task_dataset_measurementViewSet(ModelViewSet):
    queryset = task_dataset_measurement.objects.all()
    serializer_class = task_dataset_measurementSerializer
    search_fields = ["id"]
    ordering_fields = ['pk']
    ordering = ['pk']
    def create(self, request, *args, **kwargs):
        #print(type(request),request)
        serializer = self.get_serializer(data=request)
        # print("类型：",type(request.data))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)


class solution_resultViewSet(ModelViewSet):
    queryset = solution_result.objects.all()
    serializer_class = solution_resultSerializer    
    search_fields = ["id"]
    ordering_fields = ['pk']
    ordering = ['pk']

def Download(request,filename):
    print('test')
    print(filename)
    folder2zip(os.path.join(system_settings.originToBeZippedFolder,"codes/"+filename), system_settings.originToBeZippedFolder)
    print("打包完毕")
    # return HttpResponseRedirect("http://localhost:8000/media/"+filename+".zip")
    return HttpResponseRedirect(system_settings.ip+"media/"+filename+".zip")

#软件测试
class AFDResponse(Response):
    def __init__(self, code=10000, msg="Success", data="", status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(AFDResponse, self).__init__(data, status, template_name, headers,
                                         exception, content_type)

        self.data = {"code": code, "msg": msg, "data": data}

class TraceView(APIView):
    def post(self, request, *args, **kwargs):
        trace_type = request.data['trace_name']
        data = {}
        run_time = ''           #解析日志用时
        trace_dict = {}        #日志名列表
        if(trace_type == 'Memo'):
            app_trace_dict, run_time, trace_dict = get_trace("Memo")
        elif(trace_type == 'Calendar'):
            app_trace_dict, run_time, trace_dict = get_trace("Calendar")
        trace_list = []
        for key,value in trace_dict.items():
            temp_dict = {}
            temp_dict['name'] = key
            temp_dict['time'] = value
            trace_list.append(temp_dict)
        data['time'] = run_time
        data['trace_list'] = trace_list
        return AFDResponse(data = data)

class RepresentationView(APIView):
    def post(self, request, *args, **kwargs):
        # classifier_fit(0,0,"FCN","Test","MCT_MTS")
        representation_generator = request.data['representation_generator']
        category_name = request.data['category_name']
        current_path = os.getcwd()
        status_file = Path(current_path + '/representation_time.txt')
        if status_file.is_file():
            os.remove(status_file)
        txt_path = current_path + '/representations.txt'
        txtWirte(txt_path, [representation_generator, category_name])
        
        data = {}
        return AFDResponse(data = data)

class ClassifierView(APIView):
    def post(self, request, *args, **kwargs):
        classifier_name = request.data['classifier_name']
        # print(classifier_name)
        category_name = request.data['category_name']
        representation_generator = request.data['representation_generator']
        os.system("taskkill -f -im tensorboard.exe")
        current_path = os.getcwd()
        comm = "tensorboard --logdir " + current_path + '/trained/' + classifier_name
        # print(comm)
        p = subprocess.Popen(comm)
        time.sleep(2)
        data = {}
        return AFDResponse(data = data)

class TrainingView(APIView):
    status = 0
    def post(self, request, *args, **kwargs):
        classifier_name = request.data['classifier_name']
        category_name = request.data['category_name']
        representation_generator = request.data['representation_generator']
        current_path = os.getcwd()
        status_file = Path(current_path + '/status.txt')
        if status_file.is_file():
            os.remove(status_file)
        txt_path = current_path + '/classifier_para.txt'
        txtWirte(txt_path, ['0', '0', classifier_name, category_name, representation_generator])

        data = {}
        return AFDResponse(data = data)

class ResultView(APIView):
    def post(self, request, *args, **kwargs):
        classifier_name = request.data['classifier_name']
        category_name = request.data['category_name']
        representation_generator = request.data['representation_generator']
        data = {}
        current_path = os.getcwd()
        status_file = Path(current_path + '/status.txt')
        if status_file.is_file():
            # current_path = os.getcwd()
            # result_path=os.path.join(current_path,"apps","system","detailed_results")
            # result_path=os.path.join(result_path,classifier_name)
            # result_path=os.path.join(result_path,"APP_TRACE_Archive_20191")
            # result_path=os.path.join(result_path,category_name)
            # result_path=os.path.join(result_path,"DPre")
            # result_path=os.path.join(result_path,representation_generator)
            # fileList=os.listdir(result_path)
            # # print(fileList)
            # acc=-1
            # for item in fileList:
            #     csv_folder_path=os.path.join(result_path,item)
            #     tempList=os.listdir(csv_folder_path)
            #     for _file in tempList:
            #         if _file=="df_metrics.csv":
            #             csvPath=os.path.join(csv_folder_path,_file)
            #             content=pd.read_csv(csvPath)
            #             tempAcc=content["best_model_train_acc"][0]
            #             if acc<tempAcc:
            #                 acc=tempAcc
            # acc = round(acc, 6)
            data['time'] = txtRead(status_file)[1].replace("\n","")
            os.system("taskkill -f -im tensorboard.exe")
            current_path = os.getcwd()
            comm = "tensorboard --logdir " + current_path + '/apps/system/' + classifier_name
            p = subprocess.Popen(comm)
            time.sleep(2)
            data['done'] = 1
        else:
            data['done'] = 0
        return AFDResponse(data = data)

class RepResultView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        current_path = os.getcwd()
        status_file = Path(current_path + '/representation_time.txt')
        if status_file.is_file():
            data['time'] = txtRead(status_file)[0].replace("\n","")
            data['done'] = 1
        else:
            data['done'] = 0
        return AFDResponse(data = data)

