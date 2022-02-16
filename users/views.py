from django.shortcuts import render
from .models import Profile


def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles,
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