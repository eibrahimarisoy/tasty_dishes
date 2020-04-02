from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from user.forms import RegisterForm, LoginForm, UserUpdateForm
from recipe.models import Recipe

STATUS = "published"

def user_register(request):
    context = dict()
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.clean_username()
        first_name = form.clean_first_name()
        last_name = form.clean_last_name()
        email = form.clean_email()
        password = form.clean_password()
        new_user = User(username=username, last_name=last_name,
                        first_name=first_name, email=email)
        new_user.set_password(password)
        new_user.is_active = True
        new_user.save()

        login(request, new_user)
        messages.success(request, "You have successfully registered.")
        return redirect("index")

    context["register_form"] = form
    return render(request, "user/register.html", context)


def user_login(request):
    context = dict()
    form = LoginForm(request.POST or None)
    context["form"] = form
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.info(request, "Username is wrong.")
            return render(request, "user/login.html", context)

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.info(request, "Username or password is wrong")
            return render(request, "user/login.html", context)
        else:
            messages.success(request, "You have successfully logged in.")
            login(request, user)
            return redirect("index")

    return render(request, "user/login.html", context)

@login_required()
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("index")


@login_required()
def user_like_recipe_list(request):
    context = dict()
    user = request.user
    recipes = Recipe.objects.filter(likes=user)
    context['recipes'] = recipes
    return render(request, "user/like_recipe_list.html", context)


@login_required()
def user_recipe_list(request):
    context = dict()
    user = request.user
    recipes = Recipe.objects.filter(
        owner=user,
        status=STATUS,    
    )
    context['recipes'] = recipes
    return render(request, "user/recipe_list.html", context)


@login_required()
def user_profile(request):
    context = dict()
    user = get_object_or_404(User, pk=request.user.pk)
    context['user'] = user
    return render(request, "user/profile.html", context)


@login_required()
def update_user_profile(request):
    context = dict()
    form = UserUpdateForm(request.POST or None, instance=request.user)
    context['form'] = form
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile updated successfully.")
            return redirect("user_profile")
    return render(request, "user/update_profile.html", context)


@login_required()
def change_password(request):
    context = dict()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed!')
            return redirect('user_profile')
        else:
            messages.error(request, 'You have logged in incorrectly!')
    else:
        form = PasswordChangeForm(request.user)
    
    context['form'] = form
    return render(request, 'user/change_password.html', context)