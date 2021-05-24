from django.db import models
from django.contrib.auth.models import User
from markdown import Markdown
import markdown

# Create your models here.

class Category(models.Model):
    '''
        文章分类资源模型
    '''

    name        = models.CharField("分类名称", max_length=50, help_text="分类名称")
    create_time = models.DateField("创建时间", auto_now_add=True, help_text="创建时间")
    update_time = models.DateField("更新时间", auto_now=True, help_text="更新时间")
    status      = models.BooleanField("是否显示", default=1, max_length=1, help_text="是否显示, 0-不显示，1-显示")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resource_category'
        ordering = ['-create_time']




class Tag(models.Model):
    '''
        文章标签资源模型
    '''

    text        = models.CharField("标签内容", max_length=20, unique=True, db_index=True, help_text="标签内容")
    create_time = models.DateField("创建时间", auto_now_add=True, help_text="创建时间")
    status      = models.BooleanField("是否显示", default=1, max_length=1, help_text="是否显示, 0-不显示，1-显示")


    def __str__(self):
        return self.text

    class Meta:
        db_table = 'resource_tag'
        ordering = ['id']




class Avatar(models.Model):
    '''
        图像资源模型
    '''

    content = models.ImageField("图像内容", upload_to="avatar/%Y%m%d", help_text="图像内容")
    create_time = models.DateField("创建时间", auto_now_add=True, help_text="创建时间")
    status      = models.BooleanField("是否显示", default=1, max_length=1, help_text="是否显示, 0-不显示，1-显示")

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'resource_avatar'
        ordering = ['id']



class Article(models.Model):
    '''
        文章资源模型
    '''
    
    tags        = models.ManyToManyField(Tag, blank=True, related_name="articles", verbose_name="标签", help_text="标签")
    avatar      = models.ForeignKey(Avatar, on_delete=models.CASCADE, null=True, blank=True,related_name="articles", verbose_name="标题图", help_text="标题图")
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="articles", verbose_name="分类", help_text="分类")
    author      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="articles", verbose_name="作者", help_text="作者")
    title       = models.CharField("标题", max_length=50, db_index=True, help_text="标题")
    content     = models.TextField("内容", help_text="内容")
    create_time = models.DateField("创建时间", auto_now_add=True, help_text="创建时间")
    update_time = models.DateField("更新时间", auto_now=True, help_text="更新时间")
    status      = models.BooleanField("是否显示", default=1, max_length=1, help_text="是否显示, 0-不显示，1-显示")


    def __str__(self):
        return self.title


    def transform_md(self):
        '''
            正文转换成带有 html标签的格式
        '''
        md = Markdown(
            extensions= [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        # 覆写文本格式
        md_content = md.convert(self.content)
        # 返回md文本和渲染目录
        return md_content, md.toc


    class Meta:
        db_table = 'resource_articles'
        ordering = ['-create_time']