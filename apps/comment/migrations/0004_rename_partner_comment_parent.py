# Generated by Django 3.2 on 2021-06-09 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_comment_partner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='partner',
            new_name='parent',
        ),
    ]
