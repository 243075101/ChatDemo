# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nick', models.CharField(max_length=30)),
                ('headr_pic', models.ImageField(default=b'headr_pic/default.jpg', upload_to=b'headr_pic', verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('friends', models.ManyToManyField(related_name='_userprofile_friends_+', to='chatQQ.UserProfile', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
