from django.urls import path, include
from . import views
urlpatterns = [
    path('main', views.dashboard, name='main'),
    path('profile', views.profile, name = 'profile' ),
    path('delete-blog-topic/<str:uniqueId>/', views.deleteBlogTopic, name='delete-blog-topic'),
    path('generate-blog-from-topic/<str:uniqueId>/', views.createBlogFromTopic, name='generate-blog-from-topic'),
    path('blog-topic', views.blogTopic, name='blog-topic'),
    path('blog-section', views.BlogSection, name='blog-section'),
    path('save-blog-topic/<str:blogTopic>/', views.saveBlogTopic, name='save-blog-topic'),
    path('use-blog-topic/<str:blogTopic>/', views.useBlogTopic, name='use-blog-topic'),
    path('view-generated-blog/<slug:slug>/', views.viewGeneratedBlog, name='view-generated-blog'),
   path('billing', views.billing, name='billing'),
]
