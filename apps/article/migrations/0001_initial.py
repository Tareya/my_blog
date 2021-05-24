# Generated by Django 3.2 on 2021-05-18 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, help_text='标题', max_length=50, unique=True, verbose_name='标题')),
                ('content', models.TextField(help_text='内容', verbose_name='内容')),
                ('create_time', models.DateField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('status', models.BooleanField(default=1, help_text='是否显示, 0-不显示，1-显示', max_length=1, verbose_name='是否显示')),
                ('author', models.ForeignKey(help_text='作者', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'db_table': 'resource_articles',
                'ordering': ('-create_time',),
            },
        ),
    ]
