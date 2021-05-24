from os import extsep
from re import I, search
from django.shortcuts import render

# 视图集
from rest_framework import serializers, viewsets, mixins

# 权限控制
# from rest_framework.permissions import IsAdminUser    # 管理员权限控制
from .permissions import IsAdminUserorReadonly          # 自定义权限控制

# 通用过滤 - 关键词匹配
from django_filters.rest_framework import DjangoFilterBackend    # 注意需要rest_framework 的 form.html 支持，路径 django_filters/rest_framework/form.html

# 模糊匹配
from rest_framework import filters

# 模型、序列化类
from .models import Article, Category, Tag, Avatar
from .serializers import ArticleSerializer, ArticleDetailUserSerializer, ArticleDetailAdminSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, AvatarSerializer



# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    '''
        list: 返回文章分类信息列表
        create: 新建一条文章分类信息
        read: 返回指定文章分类信息
        update: 修改指定文章分类信息
        partial_update: 更新部分字段
        delete: 删除指定文章分类信息
    '''

    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminUserorReadonly]

    def get_serializer_class(self):

        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer




class TagViewset(viewsets.ModelViewSet):
    '''
        list: 返回文章标签信息列表
        create: 新建一条文章标签信息
        read: 返回指定文章标签信息
        update: 修改指定文章标签信息
        partial_update: 更新部分字段
        delete: 删除指定文章标签信息
    '''

    queryset            = Tag.objects.all()
    serializer_class    = TagSerializer
    permission_classes  = [IsAdminUserorReadonly]




class AvatarViewset(viewsets.ModelViewSet):
    '''
        list: 返回文章标签信息列表
        create: 新建一条文章标签信息
        read: 返回指定文章标签信息
        update: 修改指定文章标签信息
        partial_update: 更新部分字段
        delete: 删除指定文章标签信息
    '''

    queryset            = Avatar.objects.all()
    serializer_class    = AvatarSerializer
    permission_classes  = [IsAdminUserorReadonly]




class ArticleViewset(viewsets.ModelViewSet):
    '''
        list: 返回文章信息列表
        create: 新建一条文章信息
        read: 返回指定文章信息
        update: 修改指定文章信息
        partial_update: 更新部分字段
        delete: 删除指定文章信息
    '''

    queryset           = Article.objects.all()
    serializer_class   = ArticleSerializer
    permission_classes = [IsAdminUserorReadonly]

    # 通用过滤配置
    # filter_backends  = [DjangoFilterBackend]
    # filterset_fields = ['author', 'title']       

    # 模糊匹配
    filter_backends = [filters.SearchFilter]
    search_fields   = ['author__username', 'title']     # author__username  django模型反向查询 


    # 根据请求方式动态获取序列化类
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailAdminSerializer


    # 从用户请求中获取用户信息，并通过序列化类保存数据
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    # # 条件查询 - 字段过滤（username）
    # def get_queryset(self):
    #     queryset = self.queryset
    #     username = self.request.query_params.get('username', None)

    #     if username is not None:
    #         queryset = queryset.filter(author__username=username)

    #     return queryset

