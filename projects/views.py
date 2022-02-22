from django.shortcuts import render, redirect
from .models import Project, Tag
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import search_projects, paginate_projects


def projects(request):
    projects, search_query = search_projects(request)
    custom_range, projects = paginate_projects(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }

    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.get_vote_count

        messages.success(request, message='Your review was successfully submitted!')
        return redirect('project', pk=project.id)


    profile = project.owner
    tags = project.tags.all()
    context = {
        'project': project,
        'tags': tags,
        'profile': profile,
        'form': form,
    }
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, message='Project was created')
            return redirect('account')
    context = {
        'form': form,
    }
    return render(request, "projects/project_form.html", context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, message='Project was updated')
            return redirect('account')
    
    form = ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, message='Project was deleted')
        return redirect('account')     
    context = {
        'object': project,
    }
    return render(request, 'delete_object.html', context)