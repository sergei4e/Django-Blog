# Generated by Django 2.2.7 on 2019-11-08 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20171204_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(blank=True, default='2019-11-08'),
        ),
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(default='no-image.jpg', max_length=255, upload_to='images'),
        ),
    ]