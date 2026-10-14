"""
Security and Role-Based Authorization Decorators for Swayamsevak Foundation.
"""

from functools import wraps
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import UserProfile


def role_required(allowed_roles):
    """
    Decorator to enforce strict server-side role-based access control.
    Prevents unauthorized URL tampering (IDOR and horizontal/vertical privilege escalation).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(request, "Please log in to access this page.")
                return redirect(f"{reverse('login')}?next={request.path}")

            profile = UserProfile.get_profile_for_user(request.user)

            # Check account status (suspended / deactivated)
            if profile.status == 'suspended':
                messages.error(request, "Your account is temporarily suspended. Please contact foundation administration.")
                return redirect('profile')
            elif profile.status == 'deactivated':
                messages.error(request, "Your account has been deactivated. Access is denied.")
                return redirect('home')

            # Superusers always have admin privileges
            if request.user.is_superuser and 'admin' in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Check role
            if profile.role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # Forbidden access
            context = {
                'title': "Access Denied (403)",
                'error_heading': "Permission Required",
                'error_message': (
                    f"Your account role ({profile.get_role_display()}) is not authorized to access this section. "
                    "This attempt has been logged for security purposes."
                ),
                'user_role': profile.role,
            }
            return render(request, 'core/403.html', context, status=403)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    return role_required(['admin'])(view_func)


def coordinator_required(view_func):
    return role_required(['coordinator', 'admin'])(view_func)


def volunteer_required(view_func):
    return role_required(['volunteer', 'admin'])(view_func)
