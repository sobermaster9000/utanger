from django.urls import path
from . import views

urlpatterns = [
    path('get-utangs-to-user/', views.getUtangsToUser, name='get-utangs-to-user'),
    path('get-utangs-by-user/', views.getUtangsByUser, name='get-utangs-by-user'),
    path('add-user-utang/', views.addUserUtang, name='add-user-utang'),
    path('delete-user-utang/', views.deleteUserUtang, name='delete-user-utang'),
]