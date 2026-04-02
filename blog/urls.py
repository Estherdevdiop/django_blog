from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/nouveau/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/modifier/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/supprimer/', views.ArticleDeleteView.as_view(), name='article-delete'),
]