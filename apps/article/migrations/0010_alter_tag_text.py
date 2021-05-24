# Generated by Django 3.2 on 2021-05-20 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_auto_20210520_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='text',
            field=models.CharField(db_index=True, help_text='标签内容', max_length=20, unique=True, verbose_name='标签内容'),
        ),
    ]