from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat')
]
urlpatterns += staticfiles_urlpatterns()
