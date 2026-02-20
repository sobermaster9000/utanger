from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, CustomUserCreationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def dashboard(request):
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     amount = request.POST.get('amount')
    #     utang_type = request.POST.get('utang')

    #     if utang_type == 'to_user':
    #         utang = UtangsToUser.objects.create(name=name, amount=amount)
    #         if not utang.users_utangs_to_users.filter(id=request.user.id).exists():
    #             utang.users_utangs_to_users.add(request.user)
        
    #     elif utang_type == 'by_user':
    #         utang = UtangsByUser.objects.create(name=name, amount=amount)
    #         if not utang.users_utangs_by_users.filter(id=request.user.id).exists():
    #             utang.users_utangs_by_users.add(request.user)
        
    #     return redirect('dashboard')
    
    return render(request, 'dashboard.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        
        messages.error(request, 'Invalid username or password.')
        return redirect('login')
    
    return render(request, 'login.html', {'form': form})

def signup(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )

            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            
            messages.error(request, 'Signup successful, but authentication failed. Please try logging in.')
            return redirect('login')
        
        messages.error(request, 'Signup failed. Username might already be taken, or password is too weak.')
        return redirect('signup')
    
    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('home')