# Generated by Django 4.0.2 on 2022-04-16 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_topic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
