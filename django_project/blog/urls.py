from django.urls import path
from . import views # Importa views do diretório atual (.)
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"), # name cria um nome específico para evitar possíveis conflitos
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('about/', views.about, name="blog-about"), # cria um urlpattern para a view about
]