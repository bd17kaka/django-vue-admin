# Generated by Django 3.0.7 on 2021-04-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task_type_measument',
            name='test_test',
            field=models.CharField(default='1', max_length=100, verbose_name='测试测试'),
        ),
    ]
