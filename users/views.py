from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile
from django.db.models import Q
from .utils import search_profiles


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.success(request, message='username does not exist')

        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.success(request, message='Username Or password is incorrect')

    context = {
        'page': page,
    }

    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, message='you have been logged out')
    return redirect('login')



def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # saving and holding a temporary instance of the user to modify before the actual save
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, message='User account was created!')

            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = search_profiles(request)
    context = {
        'profiles': profiles,
        'search_query': search_query,
    }

    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description="")
    projects = profile.project_set.all()
    print(projects)

    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
        'projects': projects,
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
   
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, message='Skill was added')
            return redirect('account')

    context = {
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, message='Skill was updated')
            return redirect('account')

    context = {
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, message='Skill was deleted')
        return redirect('account')
    context = {
        'object': skill,
    }
    return render(request, 'delete_object.html', context)
