# Generated by Django 4.0.6 on 2022-07-16 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_rename_blogsection_blogsectionm'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogsectionm',
            name='wordCount',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
