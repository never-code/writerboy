# Generated by Django 4.0.6 on 2022-07-14 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_blog_blogsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='audience',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='topic',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]