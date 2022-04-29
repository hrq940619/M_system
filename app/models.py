from django.db import models

# Create your models here.

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='部门名称',max_length=32)

class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名',max_length=16)
    password = models.CharField(verbose_name='密码',max_length=64)
    age = models.SmallIntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name='入职时间')

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name='部门ID')

    # 有约束
    # - to:与哪张表关联
    # - to_field:表中的哪一列关联
    # - 数据列生成后会自动带上_id: depart_id
    # - 如果部门表被删除，1、
    #       1、做级联删除：on_delete=models.CASCADE
    #       2、置空：on_delete=models.SET_NULL
    depart = models.ForeignKey(verbose_name='部门ID',to='Department',to_field="id",on_delete=models.SET_NULL,null=True,blank=True)
    gender_choices = (
        (1,"男"),
        (2,"女")
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices)