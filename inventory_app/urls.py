from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('list_item/', views.list_items),
    path('item_detail/<str:pk>/', views.item_detail, name="item_detail"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('modlogin/', views.modLoginPage, name="login"),
    path('modlogout/', views.logoutMod, name="logout"),
    path('exportissue/', views.exportIssue, name="exportissue"),
    path('mod/', views.mod, name="mod"),
    path('add_items/', views.add_items, name='add_items'),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('update_items/', views.update_items_list, name="update_items_list"),
    path('accounts/profile/', views.profilepage, name="profile"),
    path('return_items/<str:pk>/', views.return_item, name="return_items"),
    path('exportcreation/', views.exportCreation, name="exportcreation"),
    path('upload/', views.upload_file_view, name='upload')
]
