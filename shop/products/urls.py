from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.products_list, name='search'),
    path('', views.products_list, name='home'),
    # path('page/<int:page>/', views.products_list, name='home'),
    path('product/<slug:product_slug>', views.products_detail, name='detail'),
    path('remove/<int:comment_id>', views.comment_remove, name='comment_remove'),
    path('update/<int:pk>/', views.CommentUpdate.as_view(), name='comment_update'),
    path('share/<slug:product_slug>', views.product_share, name='share'),
    path('send_message<slug:product_slug>', views.send_message, name='send_message')
]
