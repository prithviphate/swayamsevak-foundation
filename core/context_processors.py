"""
Context processors to make foundation settings, active language, and user role globally available in templates.
"""

from .models import FoundationSetting, ServiceArea, UserProfile


def foundation_context(request):
    """
    Exposes foundation details, active language, and role-based authentication data to all templates.
    """
    try:
        settings = FoundationSetting.get_settings()
    except Exception:
        settings = None

    current_lang = request.GET.get('lang') or request.session.get('site_lang', 'en')
    if current_lang not in ['en', 'mr']:
        current_lang = 'en'

    # Get service areas and categories for navigation
    try:
        nav_services = ServiceArea.objects.filter(is_active=True).order_by('order')[:7]
    except Exception:
        nav_services = []

    try:
        from .models import ActivityCategory
        nav_categories = ActivityCategory.objects.filter(is_active=True).order_by('order')
    except Exception:
        nav_categories = []

    user_profile = None
    dashboard_url_name = 'login'
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.get_profile_for_user(request.user)
            if user_profile.is_admin_role:
                dashboard_url_name = 'admin_dashboard'
            elif user_profile.is_coordinator_role:
                dashboard_url_name = 'coordinator_dashboard'
            else:
                dashboard_url_name = 'volunteer_dashboard'
        except Exception:
            user_profile = None

    return {
        'foundation': settings,
        'current_lang': current_lang,
        'is_mr': (current_lang == 'mr'),
        'nav_service_areas': nav_services,
        'nav_categories': nav_categories,
        'user_profile': user_profile,
        'dashboard_url_name': dashboard_url_name,
    }
