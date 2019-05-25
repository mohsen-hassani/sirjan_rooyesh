from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Week(models.Model):
    def __str__(self):
        return self.week_name
    week_name = models.CharField(max_length=20)
    expired = models.BooleanField(default=False)
    start_date = models.CharField(max_length=20,blank=True, null=True)
    expire_date = models.CharField(max_length=20,blank=True, null=True)
    total_answers = models.IntegerField(blank=True, null=True)


# GENDERS = (
#     ('male','m'),
#     ('female', 'f'),
# )

class Student(models.Model):
    # gender = models.CharField(max_length=6, choices=GENDERS)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length = 12)
    national_code = models.CharField(max_length = 10)

class Question(models.Model):
    def __str__(self):
        return self.week.week_name + ': ' + str(self.question_text)[:50]
    question_text = models.TextField()
    comment = models.TextField(blank=True, null=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)



class Choice(models.Model):
    def __str__(self):
        return self.question.question_text + ": " + str(self.choice_text)[:50]
    choice_text = models.TextField()
    is_answer = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

class UserAnswer(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    score = models.FloatField(default=0)

class WeeklyAnswer(models.Model):
    week1 = models.FloatField(default=0)
    week2 = models.FloatField(default=0)
    week3 = models.FloatField(default=0)
    week4 = models.FloatField(default=0)
    week5 = models.FloatField(default=0)
    week6 = models.FloatField(default=0)
    week7 = models.FloatField(default=0)
    all_weeks = models.FloatField(default=0)
    student_code = models.CharField(max_length=15, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
