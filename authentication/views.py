from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetCode
from .forms import LoginForm, SignupForm, ResetPasswordForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')
            return render(request, 'authentication/logIN.html', {'form': form, 'error': 'Invalid username or password.'})
    return render(request, 'authentication/logIN.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'user')

        # validation
        if password != confirm_password:
            return render(request, 'authentication/signup.html', {'error': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'authentication/signup.html', {'error': 'Username already exists.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'authentication/signup.html', {'error': 'Email already exists.'})

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )
        if role == 'admin':
            user.is_staff = True
            user.save()

        return redirect('login')

    return render(request, 'authentication/signup.html')

def request_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            PasswordResetCode.objects.filter(user=user).delete()
            reset_code = PasswordResetCode.objects.create(user=user)
            send_mail(
                subject='Your password reset code',
                message=f'Your reset code is: {reset_code.code}\n\nIt expires in 15 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except User.DoesNotExist:
            pass
        return render(request, 'authentication/request_reset_code.html', {'info': 'If that email is registered, a code has been sent.'})
    return render(request, 'authentication/request_reset_code.html')

def reset_password(request):
    form = ResetPasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                reset_code = PasswordResetCode.objects.filter(user=user, code=code).first()
                if not reset_code:
                    return render(request, 'authentication/reset_password.html', {'form': form, 'error': 'Invalid code.'})
                if reset_code.is_expired():
                    reset_code.delete()
                    return render(request, 'authentication/reset_password.html', {'form': form, 'error': 'This code has expired. Please request a new one.'})
                user.set_password(password)
                user.save()
                reset_code.delete()
                return render(request, 'authentication/reset_password.html', {'success': 'Password updated successfully.'})
            except User.DoesNotExist:
                return render(request, 'authentication/reset_password.html', {'form': form, 'error': 'Email does not exist.'})
    return render(request, 'authentication/reset_password.html', {'form': form})