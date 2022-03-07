# Generated by Django 4.0.2 on 2022-03-07 14:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0008_alter_profile_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('featured_image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
