from django.contrib import admin
from django.urls import path, include
from rooyesh import views
from rooyesh.views import week, login_page, do_login, panel, answer, do_answer, do_logout, index, blog
urlpatterns = [
    path('', index, name='index'),
    path('do_login/', do_login, name='do_login'),
    path('do_logout/', do_logout, name='do_logout'),
    path('login/', login_page, name='login'),
    path('content/<str:content>', blog, name='blog'),
    path('week/<int:id>', week, name='week'),
    path('week/<int:id>/answer', answer, name='answer'),
    # path('week/<int:id>/review',  review, name='review'),
    path('week/<int:week_id>/do_answer', do_answer, name='do_answer'),
    path('home/', panel, name='panel'),
]
