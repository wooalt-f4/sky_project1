from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('weekly/', views.weekly, name='weekly'),
    path('monthly/', views.monthly, name='monthly'),
    path('create/', views.create_meeting, name='create_meeting'),
    path('<int:id>/', views.meeting_detail, name='meeting_detail'),
    path('<int:id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('<int:id>/delete/', views.delete_meeting, name='delete_meeting'),
    path('<int:id>/cancel/', views.cancel_meeting, name='cancel_meeting'),
]
