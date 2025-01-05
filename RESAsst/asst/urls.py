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
    path('get_nodes_list/', views.get_nodes_list, name='get_nodes_list'),
    path('post_selected_node/', views.post_selected_node, name='post_selected_node'),
    path('post_new_folder/', views.post_new_folder, name='post_new_folder'),
    path('post_new_document/', views.post_new_document, name='post_new_document'),
    path('post_deleted_node/', views.post_deleted_node, name='post_deleted_node'),

]
urlpatterns += staticfiles_urlpatterns()
