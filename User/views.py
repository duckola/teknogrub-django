from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, connection
from .models import Users, Role
from Order.models import Order
from Menu.models import Favorite
from django.contrib.auth.hashers import make_password

# You would need to enable the messages framework in settings.py to use these:
# from django.contrib import messages


# --- Helper: Get User Role (For Redirection) ---
def get_user_role(user):
    """Safely retrieves the role name for redirection logic."""
    if user.is_superuser:
        return 'Admin'
    return user.role.role_name if user.role else 'Student'


# --- 1. Login View ---
def login_view(request):
    # If user is already logged in, redirect them
    if request.user.is_authenticated:
        role = get_user_role(request.user)

        if role == 'Admin' and request.user.is_superuser:
            return redirect('admin_dashboard')
        if role == 'Staff':
            return redirect('staff_orders')

        return redirect('menu')

    if request.method == 'POST':
        login_identifier = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=login_identifier, password=password)

        if user is not None:
            login(request, user)
            role = get_user_role(user)
            if role == 'Admin':
                return redirect('admin_dashboard')
            if role == 'Staff':
                return redirect('staff_orders')
            return redirect('menu')
        else:
            return render(request, 'User/login.html', {'error': 'Invalid ID Number or Password.'})

    return render(request, 'User/login.html')


# --- 2. Signup View ---
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id_number = request.POST.get('id_number')
        school_email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([first_name, last_name, id_number, school_email, password]):
            return render(request, 'User/signup.html', {'error': 'All fields are required.'})

        try:
            student_role = Role.objects.get(role_name='Student')
            hashed_password = make_password(password)

            with connection.cursor() as cursor:
                cursor.callproc('CreateUser', [
                    id_number,
                    hashed_password,
                    school_email,
                    first_name,
                    last_name,
                    id_number,
                    student_role.id
                ])

            return redirect('login')

        except Role.DoesNotExist:
            return render(request, 'User/signup.html', {'error': 'System error: Student role not found.'})
        except IntegrityError:
            return render(request, 'User/signup.html', {'error': 'Account already exists for this ID or Email.'})
        except Exception as e:
            return render(request, 'User/signup.html', {'error': f'An unexpected error occurred: {e}'})

    return render(request, 'User/signup.html')


# --- 3. Logout View ---
def logout_view(request):
    logout(request)
    return redirect('login')


# --- 4. Settings View ---
@login_required
def settings_view(request):
    orders_count = Order.objects.filter(user=request.user).count()
    fav_count = Favorite.objects.filter(user=request.user).count()

    return render(request, 'User/settings.html', {
        'orders_count': orders_count,
        'fav_count': fav_count
    })


# --- 5. Password Change View (NEW) ---
@login_required
def password_change_view(request):
    if request.method == 'POST':
        # 1. Use Django's built-in form, passing the user and POST data
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            # 2. Save the new password
            user = form.save()

            # 3. CRITICAL: Update the session hash to prevent the user from being logged out
            update_session_auth_hash(request, user)

            # 4. Success: Redirect back to settings (You would show a success message here)
            return redirect('settings')
        # If form is not valid, it automatically renders the template with errors
    else:
        # 5. GET Request: Initialize an empty form
        form = PasswordChangeForm(request.user)

    return render(request, 'User/password_change.html', {'form': form})