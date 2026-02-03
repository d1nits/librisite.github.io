from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from .forms import ProfileForm, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
User = get_user_model()


def register(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        return render(request, 'user/register.html', {'form': form})    

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')  
        else:
            return render(request, 'user/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html', {'section': 'dashboard'})



def register_request(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()   
            login(request, user, backend='graphql_jwt.backends.JSONWebTokenBackend')
            messages.success(request, "Registration successful." )
            return redirect("account:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegistrationForm()
    return render(request, "user/register.html", {"register_form":form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'user/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")


    profile, created = Profile.objects.get_or_create(user=user)

 
    is_editing = request.GET.get('edit', False)

    if request.method == 'POST' and is_editing:

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=username) 
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/profile.html', {
        'user': user,
        'profile': profile,
        'form': form,
        'is_editing': is_editing, 
    })

def login_prompt(request):
    return render(request, 'user/login_prompt.html') 