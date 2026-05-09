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

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                # Redirect based on role stored in DB (not from POST)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('home')

            return render(
                request,
                'authentication/logIN.html',
                {
                    'form': form,
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'authentication/logIN.html',
        {'form': form}
    )


def signup(request):

    form = SignupForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Username exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
                return render(
                    request,
                    'authentication/signup.html',
                    {'form': form}
                )

            # Email exists
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists.')
                return render(
                    request,
                    'authentication/signup.html',
                    {'form': form}
                )

            # All new users get role='user'
            # Admin accounts must be created via Django admin panel
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='user'
            )

            return redirect('login')

    return render(
        request,
        'authentication/signup.html',
        {'form': form}
    )


def request_reset_code(request):
    """
    Step 1: User submits their email and receives a reset code.
    """
    if request.method == 'POST':

        email = request.POST.get('email', '').strip()

        try:
            user = User.objects.get(email=email)

            # Delete any existing codes for this user
            PasswordResetCode.objects.filter(user=user).delete()

            # Create a new code
            reset_code = PasswordResetCode.objects.create(user=user)

            # Send the code via email
            send_mail(
                subject='Your password reset code',
                message=f'Your reset code is: {reset_code.code}\n\nIt expires in 15 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

        except User.DoesNotExist:
            # Don't reveal whether the email exists
            pass

        # Always show the same message to avoid email enumeration
        return render(
            request,
            'authentication/request_reset_code.html',
            {
                'info': 'If that email is registered, a code has been sent.'
            }
        )

    return render(request, 'authentication/request_reset_code.html')


def reset_password(request):
    """
    Step 2: User submits their email, the code they received, and a new password.
    """
    form = ResetPasswordForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():

            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)

                reset_code = PasswordResetCode.objects.filter(
                    user=user,
                    code=code
                ).first()

                if not reset_code:
                    return render(
                        request,
                        'authentication/reset_password.html',
                        {
                            'form': form,
                            'error': 'Invalid code.'
                        }
                    )

                # Check expiry (15 minutes)
                if reset_code.is_expired():
                    reset_code.delete()
                    return render(
                        request,
                        'authentication/reset_password.html',
                        {
                            'form': form,
                            'error': 'This code has expired. Please request a new one.'
                        }
                    )

                # Change password and clean up
                user.set_password(password)
                user.save()
                reset_code.delete()

                return render(
                    request,
                    'authentication/reset_password.html',
                    {'success': 'Password updated successfully.'}
                )

            except User.DoesNotExist:
                return render(
                    request,
                    'authentication/reset_password.html',
                    {
                        'form': form,
                        'error': 'Email does not exist.'
                    }
                )

    return render(
        request,
        'authentication/reset_password.html',
        {'form': form}
    )
