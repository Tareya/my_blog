from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers



class UserInfoSerializer(serializers.ModelSerializer):
    '''
        用户信息 序列化类
    '''

    class Meta:
        model  = User
        # fileds = [
        #     "id",
        #     "username",
        #     "date_joined",
        #     "last_login"
        # ]
        fields = "__all__"

        

