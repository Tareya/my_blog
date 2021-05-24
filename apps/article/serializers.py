from django.contrib.auth.models import User
from django.db import models
from django.db.models import manager
from rest_framework import serializers

from .models import Article, Category, Tag, Avatar
from user_info.serializers import UserInfoSerializer



class CategorySerializer(serializers.ModelSerializer):
    '''
        文章分类序列化类
    '''

    class Meta:
        model  = Category
        fields = [
            "url",
            "name",
            "status"
        ]

        read_only_fields = ["id", "create_time", "update_time"]

        extra_kwargs = {
            'url': {'view_name': 'category-detail'}
        }

        

class TagSerializer(serializers.ModelSerializer):
    '''
        文章标签序列化类
    '''

    class Meta:
        model  = Tag
        fields = [
            "url",
            "text",
            "status"
        ]
 
        read_only_fields = ["id", "create_time"]

        extra_kwargs = {
            'url': {'view_name': 'tag-detail'}
        }


    # 创建标签前先行验证，如果已存在，则不再重复创建（保证唯一性）



class AvatarSerializer(serializers.ModelSerializer):
    '''
        图像序列化类
    '''

    url = serializers.HyperlinkedIdentityField(view_name="avatar-detail")

    class Meta:
        model  = Avatar
        # fields = "__all__"
        fields = [
            "url",
            "content",
            "status"
        ]
 
        read_only_fields = ["id", "create_time"]

        # extra_kwargs = {
        #     'url': {'view_name': 'avatar-detail'}
        # }



class ArticleBasicSerializer(serializers.ModelSerializer):
    '''
        文章列表序列化类
        返回本身url的超链接
    '''
    author      = serializers.CharField(required=True, label="作者", help_text="作者")
    # author_id   = serializers.IntegerField(required=False, allow_null=True, write_only=True, label="作者用户外键ID", help_text="作者用户外键ID")
    category    = serializers.CharField(required=False, max_length=50, label="文章分类", help_text="文章分类")
    # category_id = serializers.IntegerField(required=False, allow_null=True, write_only=True, label="文章分类外键ID", help_text="文章分类外键ID")
    tags        = serializers.SlugRelatedField(required=False, queryset=Tag.objects.all(), many=True, slug_field="text",label="文章标签", help_text="文章标签")
    avatar      = AvatarSerializer(required=False, read_only=True)
    avatar_id   = serializers.IntegerField(required=False, write_only=True, allow_null=True)


    # 覆写反序列化过程，在进行字段验证之前，先行对request_body中的 tag字段做检验，如果不存在则先行创建，否则在序列化字段验证时会抛错
    def to_internal_value(self, data):
        # 从 request_body 中获取 tags的值
        tag_list = data.get('tags')

        if isinstance(tag_list, list):  # 需求 tags 是一个列表，故只有当其是一个列表时才做覆写处理
            for text in tag_list:
                if not Tag.objects.filter(text__exact=text).exists():   # 如果不存在该tag对象，则主动创建
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)


    
    def validate_category(self, value):
        """
            字段验证 - category 
            验证: category 表中是否存在 name，如果不存在则创建
        """    
        # 如果传入的值不为空，并且category 表中不存在该主键
        # if not Category.objects.filter(pk=value).exists and value is not None:
        #     raise serializers.ValidationError(f"id {value} doesn't exist in Category.")

        # return value

        try:
            # 如果 category表中存在对应 name，则返回其对象
            return Category.objects.get(name__exact=value)
        except Category.DoesNotExist:
            # 如果 category表中不存在对应的 name，则自动创建该对象
            return self.create_category(category_name=value)
    


    def validate_avatar(self, value):
        """
            字段验证 - avatar
            验证: avatar 表中是否存在该 content，如果不存在则创建
        """

        try:
            return Avatar.objects.get(content__exact=value)
        except Avatar.DoesNotExist:
            return self.create_avatar(avatar_content=value)



    def create_category(self, category_name, *args, **kwargs):
        """
            根据传入的 name 自动创建文章分类对象
        """
        return Category.objects.create(name=category_name)



    def create_avatar(self, avatar_content, *args, **kwargs):
        """
            根据传入的 content 自动创建媒体对象
        """
        return Avatar.objects.create(content=avatar_content)

    

    def validate(self, data):
        """
            对象验证 - author
            验证: author 对应的用户是否存在于 User表中，如不存在则抛出异常
        """
        author_obj = data["author"]

        try:
            data["author"]    = User.objects.get(username__exact=data["author"])           # 验证用户是否存在
            data["author_id"] = User.objects.get(username__exact=data["author"]).id     # 如果用户存在，则设置 外键关联ID

        except User.DoesNotExist:
            raise serializers.ValidationError("user {} doesn't exist in table User.".format(data["author"]))
        
        return data




class ArticleSerializer(ArticleBasicSerializer):
    '''
        文章列表序列化类 - 继承父类
    '''

    class Meta:
        model  = Article
        fields = [
            "url",            
            "category",
            "tags",
            "title",
            "content",
            "status",
        ]

        extra_kwargs = {
            'url': {'view_name': 'article-detail'},
            'content': {'write_only': True}
        }


    def to_representation(self, instance):
        """
            覆写序列化过程，article表中并没有 author字段，而是外键字段 author_id，故如果要在序列化结果中显示，则需要做覆写处理
            如果存在父类继承的情况，由于系列化是在直接反馈的最后一步，super覆写需要在子类做，而不能在父类进行
        """    
        
        print(instance.author)

        author      = instance.author

        ret = super(ArticleSerializer, self).to_representation(instance)
        ret["author"] = {
            "id": author.id,
            "username": author.username,
            "date_joined": author.date_joined,
            "last_login": author.last_login    
        } 

        return ret



class ArticleDetailUserSerializer(ArticleBasicSerializer):
    '''
        文章详情序列化类
    '''

    class Meta:
        model  = Article
        fields = "__all__"


    def to_representation(self, instance):
        """
            覆写序列化过程，article表中并没有 author字段，而是外键字段 author_id，故如果要在序列化结果中显示，则需要做覆写处理
            如果存在父类继承的情况，由于系列化是在直接反馈的最后一步，super覆写需要在子类做，而不能在父类进行
        """    
        author      = instance.author

        ret = super(ArticleDetailUserSerializer, self).to_representation(instance)
        ret["author"] = {
            "id": author.id,
            "username": author.username,
            "date_joined": author.date_joined,
            "last_login": author.last_login    
        } 

        return ret





class ArticleDetailAdminSerializer(ArticleBasicSerializer):
    '''
        文章详情序列化类
    '''

    content_html = serializers.SerializerMethodField()
    toc_html     = serializers.SerializerMethodField()


    # SerializerMethodField 方法，会自动调用 get_xx 方法
    def get_content_html(self, obj):
        # 获取渲染后的 md格式文本内容
        return obj.transform_md()[0]

    def get_toc_html(self, obj):
        # 获取渲染后的 md格式目录
        return obj.transform_md()[1]


    class Meta:
        model  = Article
        fields = "__all__"


    def to_representation(self, instance):
        """
            覆写序列化过程，article表中并没有 author字段，而是外键字段 author_id，故如果要在序列化结果中显示，则需要做覆写处理
            如果存在父类继承的情况，由于系列化是在直接反馈的最后一步，super覆写需要在子类做，而不能在父类进行
        """    
        author      = instance.author

        ret = super(ArticleDetailAdminSerializer, self).to_representation(instance)
        ret["author"] = {
            "id": author.id,
            "username": author.username,
            "date_joined": author.date_joined,
            "last_login": author.last_login    
        }    

        return ret

    


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    '''
        文章分类详情嵌套
    '''

    class Meta:
        model  = Article
        fields = [
            "url",            
            "title",
        ]

        extra_kwargs = {
            'url': {'view_name': 'article-detail'}
        }



class CategoryDetailSerializer(serializers.ModelSerializer):
    '''
        文章分类详情序列化类
    '''

    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model  = Category
        fields = [
            "id",
            "name",
            "create_time",
            "articles"
        ]

