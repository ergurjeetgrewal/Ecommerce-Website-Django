# Generated by Django 3.0.6 on 2020-06-25 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.CharField(default='', max_length=50),
        ),
    ]