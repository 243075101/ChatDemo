#coding:utf8
from django.db import models
from django.contrib.auth.models import  User

class UserProfile(models.Model):
    nick = models.CharField(max_length=30) #用户头像
    headr_pic = models.ImageField( upload_to='headr_pic',verbose_name='头像',default='headr_pic/default.jpg')#上传文件
    user= models.OneToOneField(User)
    friends = models.ManyToManyField('self',blank=True,)

    def __unicode__(self):
        return self.nick
    class Mate():
        verbose_name = verbose_name_plural = '用户'  # 对表的配置，，内部类---卑职表明

# Create your models here.
