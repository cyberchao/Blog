from django.urls import path
from .views import post,blog,search,get_category_blogs,get_tag_blogs,about,license
from .register import loginde, logoutde, active, profile, change_profile, signup

urlpatterns = [
    path('', post, name='post_list'),
    path('blog/<id>/', blog, name='blog_detail'),
    path('category/<id>/', get_category_blogs, name='get_category_blogs'),
    path('tag/<id>/', get_tag_blogs, name='get_tag_blogs'),
    path('search/',search,name='search'),
    path('about/',about,name='about'),
    path('license/',license,name='license'),
    path('signup',signup,name='signup'),
    path('login',loginde,name='login'),
    path('logout',logoutde,name='logout'),
    path('profile',profile,name='profile'),
    path('change-profile',change_profile,name='change-profile'),
    path('active/<code>',active, name='get_tag_blogs'),
]
