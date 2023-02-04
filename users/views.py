from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


def login(request):
    """Login page display and get username, password

    :param request: HttpRequest
    :return: object HttpResponse of login page
    """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/', reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    """Registration page display and get first_name, last_name, username, email, password1, password2

    :param request: HttpRequest
    :return: object HttpResponse of registration page
    """
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались.')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }

    return render(request, 'users/registration.html', context)


def profile(request):
    """Profile page display and update first name, last_name, image

    :param request: HttpRequest
    :return: object HttpResponse of profile page
    """
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            form.errors()
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),

    }
    return render(request, 'users/profile.html', context)


def logout(request):
    """Main page display and logout

    :param request: HttpRequest
    :return: object HttpResponse of main page
    """
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
