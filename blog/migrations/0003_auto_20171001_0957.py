# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171001_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, default='static/img/images/no-img.jpg', upload_to='static/img/images')),
                ('alt', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='images',
            name='post',
        ),
        migrations.DeleteModel(
            name='Images',
        ),
        migrations.AddField(
            model_name='article',
            name='img',
            field=models.ManyToManyField(to='blog.Image'),
        ),
    ]
