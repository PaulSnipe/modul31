from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('confirm/<uuid:token>/', views.confirm_email, name='confirm_email'),
    path('posts/create/', views.create_post, name='create_post'),
    path('my_posts/', views.my_posts, name='my_posts'),

    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/response/', views.create_response, name='create_response'),

    path('responses/', views.manage_responses, name='manage_responses'),
    path('response/<int:response_id>/accept/', views.accept_response, name='accept_response'),
    path('response/<int:response_id>/delete/', views.delete_response, name='delete_response'),

    path('subscribe/', views.subscribe_category, name='subscribe_category'),

    path('', views.news_list, name='news_list'),
]
