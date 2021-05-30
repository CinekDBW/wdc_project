from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto uzytkownika {username} zostalo utworzone!')
            group_casual = Group.objects.get(name='Casual')
            group_casual.user_set.add(User.objects.get(username=username))
            return redirect('forum-home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form' : form})
