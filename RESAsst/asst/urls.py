from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('show_history/', views.show_history, name='show_history'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('strmatch/', views.strmatch),
    path('bm25/', views.bm25),
    path('login/', views.login),
    path('sendVerification/', views.sendVerification),
    path('register/', views.register),
    path('translate/', views.translate)
]
urlpatterns += staticfiles_urlpatterns()
