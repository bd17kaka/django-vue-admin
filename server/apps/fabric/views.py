from django.shortcuts import render

# Create your views here.
import logging

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
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

import requests as rq
import json 
import _thread
import os

logger = logging.getLogger('log')
from django.conf import settings

def login():
    url = settings.FABRIC_URL_PREFIX + '/users'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    values = {"username":"admin1", "password":"admin1"}
    data = json.dumps(values)
    res = rq.post(url=url, data=data, headers=headers)
    obj = res.json()

    return obj

def get_channel_info(channel, token):
    url = settings.FABRIC_URL_PREFIX + '/channels/' + channel
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + token
    }
    res = rq.get(url=url, headers=headers)
    return res.json()

def get_channels(token):
    url = settings.FABRIC_URL_PREFIX + "/channels"
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + token
    }
    res = rq.get(url=url, headers=headers)
    return res.json()

def get_chaincodes(token):
    url = settings.FABRIC_URL_PREFIX + "/chaincodes"
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + token
    }
    res = rq.get(url=url, headers=headers)
    return res.json()

def get_block_info(channel, token, id):
    url = settings.FABRIC_URL_PREFIX + '/channels/' + channel + "/blocks/" + str(id)
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + token
    }
    res = rq.get(url=url, headers=headers)
    return res.json()

class ChannelView(GenericViewSet):
    
    @action(methods=['get'], detail=False, url_name='queryAll', permission_classes=[IsAuthenticated])
    def queryAll(self, request):
        token = login()
        if not token: 
            return Response('登录到fabric服务器失败', status=status.HTTP_200_OK)
        print("token:%s" % token)

        result = []
        channellist = get_channels(token)
        for item in channellist:
            channel = item['channel_id']
            info = get_channel_info(channel, token)
            height = info['height']['low']

            block_info = get_block_info(channel, token, (height - 1))
            currentBlockHash = block_info['header']['data_hash']

            result.append({
                'channel_id':  channel,
                'height': info['height']['low'],
                'currentBlockHash': currentBlockHash
            })

        return Response(result)

class ChaincodeView(GenericViewSet):
    
    @action(methods=['get'], detail=False, url_name='queryAll', permission_classes=[IsAuthenticated])
    def queryAll(self, request):
        token = login()
        if not token: 
            return Response('登录到fabric服务器失败', status=status.HTTP_200_OK)
        print("token:%s" % token)

        result = []
        chaincodelist = get_chaincodes(token)
        for item in chaincodelist:
            name = item['name']
            version = item['version']
            path = item['path']

            result.append({
                'name':  name,
                'version': version,
                'path': path
            })

        return Response(result)