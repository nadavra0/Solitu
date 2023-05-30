from django.db import models

# Create your models here.
class Stack (models.Model):
    course_name = models.CharField(max_length=50)
    stack_num = models.IntegerField()
    len = models.IntegerField()

    def __str__(self):
        return self.course_name

class Question (models.Model):
    stack = models.ForeignKey(Stack,on_delete=models.PROTECT)
    q = models.CharField(max_length=128)
    a = models.CharField(max_length=128)


    def __str__(self):
        return self.q