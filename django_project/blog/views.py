from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post 
#from django.http import HttpResponse

# Create your views here.
def home(request):
	context = {
		'posts': Post.objects.all()
	}
	#return HttpResponse('<h1>Home</h1>')
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted'] # Ordenará os posts pela data
	paginate_by = 4 # Define o número de posts por página

class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 4 # Define o número de posts por página

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	# Sobrescreve o método form_valid
	def form_valid(self, form):
		form.instance.author = self.request.user # Setamos o autor do post
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	# Sobrescreve o método form_valid
	def form_valid(self, form):
		form.instance.author = self.request.user # Setamos o autor do post
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author: # Checa se o usuário logado atualmente é o autor do post, se for true ele poderá atualizar o post
			return True
		return False 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/' # Garante que voltemos para home ao deletar o post

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author: # Checa se o usuário logado atualmente é o autor do post, se for true ele poderá atualizar o post
			return True
		return False 

def about(request):
	#return HttpResponse('<h1>About</h1>')
	return render(request, 'blog/about.html', {'title':'About'})