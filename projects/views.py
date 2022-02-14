from django.shortcuts import render, redirect


def projects(request):
    msg = 'Hello, you are on the projects page'
    context = {
        'message': msg,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    return render(request, 'projects/single-project.html')
