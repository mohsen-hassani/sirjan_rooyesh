from django.contrib import admin
from rooyesh.models import UserAnswer, Student, Question, Week, Choice, WeeklyAnswer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'

class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 7


class WeekAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user','question','choice','score','week')
    list_filter = ['week','question','user']

admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Week, WeekAdmin)
admin.site.register(Choice)
admin.site.register(Student)
admin.site.register(WeeklyAnswer)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)