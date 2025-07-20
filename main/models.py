from django.db import models

class Teacher(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField(null=False, blank=False)

    class Meta:
        unique_together = ('name', 'subject')
