from django.db import models

# Create your models here.


# Create your models here.

class Liaotianuser(models.Model):
    username = models.CharField("用户名", max_length=30, unique=True)

    password = models.CharField("密码", max_length=32)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return "用户%s" % self.username
