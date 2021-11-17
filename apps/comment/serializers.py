from re import T
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers

from .models import Comment
from user_info.serializers import UserInfoSerializer



class CommentChildrenSerializer(serializers.ModelSerializer):
    '''
        子级评论序列化类
    '''

    url     = serializers.HyperlinkedIdentityField(view_name="comment-detail")
    author  = UserInfoSerializer(read_only=True)

    class Meta:
        model   = Comment
        # 使用 exclude 来定义不需要的字段（排除）
        exclude = [
            'parent',       # parent 为父评论
            'article',
            'create_time',
            # 'update_time'
        ]

    
    def to_representation(self, instance):
  
        author      = instance.author

        ret = super(CommentChildrenSerializer, self).to_representation(instance)
        ret["author"] = {
            # "id": author.id,
            "username": author.username,
            # "date_joined": author.date_joined,
            # "last_login": author.last_login    
        } 

        return ret



class CommentSerializer(serializers.ModelSerializer):
    '''
        文章评论序列化类
    '''
    url        = serializers.HyperlinkedIdentityField(view_name="comment-detail")
    author     = UserInfoSerializer(read_only=True)

    article    = serializers.HyperlinkedRelatedField(view_name="article-detail", read_only=True)
    article_id = serializers.IntegerField(write_only=True, allow_null=False, required=True) 

    parent     = CommentChildrenSerializer(read_only=True)
    parent_id  = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    

    class Meta:
        model  = Comment
        # fields = "__all__"
        fields = [
            "url",
            "author",
            "article",
            "article_id",
            "parent",
            "parent_id",
            "content",
            "update_time",
            "status"
        ]

        read_only_fields  = ["id", "create_time"]


    def to_representation(self, instance):

        author = instance.author

        ret = super(CommentSerializer, self).to_representation(instance)
        ret["author"] = {
            # "id": author.id,
            "username": author.username,
            # "date_joined": author.date_joined,
            # "last_login": author.last_login    
        } 

        return ret

    # 父评论只能在评论创建时被关联，后续不能更改，因此在更新评论时忽略 parent_id 参数
    def update(self, instance, validated_data):
        validated_data.pop('parent_id', None)   # 忽略 parent_id 并预设为 None
        return super().update(instance, validated_data)