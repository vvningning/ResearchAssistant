from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('strmatch/', views.strmatch),
    path('bm25/', views.bm25),
    path('login/', views.login)
]
urlpatterns += staticfiles_urlpatterns()
