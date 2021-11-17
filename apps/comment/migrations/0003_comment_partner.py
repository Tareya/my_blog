# Generated by Django 3.2 on 2021-05-27 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='partner',
            field=models.ForeignKey(help_text='评论', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='comment.comment', verbose_name='父级评论'),
        ),
    ]
