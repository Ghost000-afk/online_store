from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, EditProfileForm, AvatarUploadForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Profile


def signup(request):
    """
    Обрабатывает регистрацию нового пользователя.

    Если метод запроса POST, создается форма регистрации и проверяется её валидность.
    Если форма валидна, создается новый пользователь, и он автоматически входит в систему.
    Затем происходит перенаправление на страницу со списком категорий.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с формой регистрации или перенаправление на страницу со списком категорий.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('category_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {
        'form': form
    })


class CustomLoginView(LoginView):
    """
    Класс для настройки представления входа.

    Устанавливает пользовательский шаблон для страницы входа
    и перенаправление после успешного входа.
    """
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('category_list')


def logout_confirm(request):
    """
    Подтверждает выход пользователя из системы.

    Если метод запроса POST, пользователь выходит из системы
    и происходит перенаправление на страницу со списком категорий.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с подтверждением выхода или перенаправление на страницу со списком категорий.
    """
    if request.method == 'POST':
        logout(request)
        return redirect('category_list')
    return render(request, 'accounts/logout_confirm.html') 


@login_required
def profile(request):
    """
    Отображает страницу профиля пользователя.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с информацией о профиле пользователя.
    """
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    """
    Обрабатывает редактирование профиля пользователя.

    Если метод запроса POST, проверяются формы редактирования пользователя и профиля.
    Если формы валидны, изменения сохраняются, и происходит перенаправление на страницу профиля.

    Args:
        request: HTTP-запрос.

    Returns:
        HttpResponse: HTML-страница с формами редактирования профиля или перенаправление на страницу профиля.
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = AvatarUploadForm(instance=profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
