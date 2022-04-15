import views as views
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group

from blog.models import Post
from projects.models import Project
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm, CustomStaffUserCreationForm
from .models import Profile, Message
from django.db.models import Q
from .utils import search_profiles, paginate_profiles
from django.views import View, generic as views


class DashboardAdminView(views.ListView):
    model = Profile
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = Profile.objects.all()
        projects = Project.objects.all()
        number_of_users = len(users)
        number_of_projects = len(projects)
        context['users'] = users
        context['projects'] = projects
        context['number_of_users'] = number_of_users
        context['number_of_projects'] = number_of_projects
        return context


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.success(request, message='username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
            user = form.save(
                commit=False)  # saving and holding a temporary instance of the user to modify before the actual save
            user.username = user.username.lower()
            user.save()

            messages.success(request, message='User account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)


def register_staff_user(request):
    page = 'register'
    form = CustomStaffUserCreationForm()
    if request.method == 'POST':
        form = CustomStaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_staff = True
            user.save()
            staff_group = Group.objects.get(name='Staff')
            staff_group.user_set.add(user)
            staff_group.save()

            messages.success(request, message='New Staff member has been added!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, message='An error has occurred during registration')
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register_staff.html', context)



def profiles(request):
    profiles, search_query = search_profiles(request)
    custom_range, profiles = paginate_profiles(request, profiles, 3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {
        'message_requests': message_requests,
        'unread_count': unread_count,
    }

    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)


def send_issue(request, pk, post_pk):
    page = 'blog'
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    post = Post.objects.get(id=post_pk)
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender
                message.email = sender.email
                message.subject = f'Fix issue with post {post.title} in {post.topic}'
            message.save()
            messages.success(request, message='Your issue has been submitted successfully')
            return redirect('blog-home')
    context = {
        'recipient': recipient,
        'form': form,
        'post': post,
        'page': page,
    }
    return render(request, 'users/message_form.html', context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, message="Message sent successfully")
            return redirect('user-profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form,
    }
    return render(request, 'users/message_form.html', context)
