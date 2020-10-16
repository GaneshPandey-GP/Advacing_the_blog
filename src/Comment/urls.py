from django.urls import path
from . import views

urlpatterns = [
  
    path('comments/<id>',views.comment_thread, name='thread'),
    path('comment_delete/<id>',views.comment_delete, name='comment_delete'),
   #path('delete/<slug>',views.delete_post, name='delete'),
]