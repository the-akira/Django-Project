from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in!')
			return redirect('login') # Nome que demos ao padrão da URL
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

# Tipos de flash message
# messages.debug, messages.info, messages.success, messages.warning, messages.error

@login_required # Decorador modifica a funcionalidade da função e torna o login necessário para enxergar o profile
def profile(request):
	# instance nos permite pré-popular os formulários com as informações atuais do usuário

	# Testa se a solicitação é válida (POST)
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		# Verifica a validade dos forms
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html', context)