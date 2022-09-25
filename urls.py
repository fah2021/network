
from django.urls import path

from . import views
from .views import Following, PostsList, Owners_views


urlpatterns = [
    path("", PostsList.as_view(), name="index"),
    path("my_account", Owners_views.as_view(), name="my_account"),
    path("following", Following.as_view(), name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name ="add_post"),
    path("get_message", views.get_message, name ="get_message"),
    path("get_all_messages", views.get_all_messages, name ="get_all_messages"),
    path('like/<int:post_id>', views.like, name='likes'),
    path("followers_count/<int:post_owner>",views.followers_count,name="followers_count"),
    path("profile/<int:post_owner>", views.profile, name="profile"),
    path("edit/<str:post_id>", views.edit, name="edit"), 

]
  