from django.urls import path
from . import views

urlpatterns = [
    path('',views.List_post,name='home'),
    path('create/',views.create_post),
    path('details/<slug>',views.details_post, name='detail'),
    path('update/<slug>',views.update_post, name='Update'),
    path('delete/<slug>',views.delete_post, name='delete'),
    path('login/',views.Login_view,name="login"),
    path('logout/',views.Logout_view,name="logout"),
    path('register/',views.Register_view,name="register"),
]