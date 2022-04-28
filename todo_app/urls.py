from django.urls import path

from . import views

app_name='todo_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('all/delete/<int:id>', views.delete_todo, name='delete_todo'),
    path('dashboard/all/edit/<int:id>', views.edit_todo, name='edit_todo'),
    path('all/status/<int:id>', views.status_todo, name='status_todo'),
    path('completed/', views.completed_todo, name='completed_todo'),
    path('active/', views.active_todo, name='active_todo'),
    #path('sorted-todos/', views.sorted_todo, name='sorted_todo'),
    path('logout/', views.logout_view, name='logout'),
    path('analytics-page/', views.analytics_view, name='analytics_view'),

]