from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_folders_request),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request),
    path('logout/', views.logout_request),
    path('folders/', views.list_folders_request),
    path('create_folder/', views.create_folder_request),
    path('view_folder_content/<str:folder_name>', views.view_folder_content),
    path('new_note_save/', views.save_new_note_request),
    path('view_note_content/<str:folder_name>/<str:note_name>', views.view_note_content_request),
    path('create_note/<str:folder_name>', views.create_note_request),
    path('note_update/', views.note_update_request),
    path('delete_folder/<str:folder_name>', views.delete_folder_request),
    path('delete_note/<str:folder_name>/<str:note_name>', views.delete_note_request),
]
