# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, default='static/img/images/no-img.jpg', upload_to='static/img/images')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='img',
        ),
        migrations.AddField(
            model_name='images',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='blog.Article'),
        ),
    ]