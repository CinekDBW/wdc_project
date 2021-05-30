from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='forum-home'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic-details'),
    path('topic/<int:pk>/add-post', views.PostCreateView.as_view(), name='add-post'),
    path('topic/add-topic/', views.TopicCreateView.as_view(), name='add-topic'),
    path('topic/verify/', views.topicVerifyView, name='verify-topics'),
    path('topic/private/', views.private_topics, name='private-topics'),
    path('topic/<int:topic>/post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete-post'),
    path('google/', include('social_django.urls', namespace='social'))
]