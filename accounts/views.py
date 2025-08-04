from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group


# Create your views here.

def hello_world(request):
    return HttpResponse(f"<h3>Hello {request.user}!</h3>")


@unauthenticated_user
def login_views(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('default_home_name')
        else:
            messages.info(request, "Username or password is incorrect")
    context = {}
    return render(request, 'accounts/loginPage.html', context)


@unauthenticated_user
def register_views(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_email = form.cleaned_data.get('email')
            user_name = form.cleaned_data.get('username')

            # ✅ Assign groups based on email domain
            allowed_college_domain = 'srkrec.ac.in'
            allowed_gmail = 'gmail.com'
            domain = user_email.split('@')[-1]

            if domain == allowed_college_domain:
                # Assign student group for college domain
                user_group = Group.objects.get(name='student')
                user.groups.add(user_group)
            elif domain == allowed_gmail:
                # Assign default group (student) for Gmail
                user_group = Group.objects.get(name='student')
                user.groups.add(user_group)
            else:
                # If email does not match any allowed domain, delete user and show error
                messages.error(request, 'Email must be a college or Gmail address!')
                user.delete()
                return redirect('register_page')

            messages.success(request, f'Account was successfully created for {user_name}')
            return redirect('login_page')

    context = {'form': form}
    return render(request, 'accounts/registerPage.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You are successfully logged out')
    return redirect('login_page')


def default_home(request):
    print('default_home')
    group = None
    if request.user.is_anonymous:
        return redirect('login_page')
    else:
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            print(group)

            if group == 'student':
                return redirect('home')

            elif group == 'warden':
                return redirect('warden_blocks')

            elif group == 'chief warden':
                return redirect('cheif_warden_home')

            else:
                message = "You are not authorized to view this page"
                messages.error(request, message)
                return redirect('logout_page')
