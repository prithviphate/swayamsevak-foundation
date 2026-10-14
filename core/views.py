"""
Views for Swayamsevak Foundation web application.
College Major Project.
Full role-based authentication, permissions, and multi-tier dashboards.
"""

import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, url_has_allowed_host_and_scheme
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date

from .models import (
    FoundationSetting,
    ServiceArea,
    ActivityCategory,
    Activity,
    Volunteer,
    SupportInquiry,
    ContactInquiry,
    GalleryItem,
    GalleryMedia,
    UserProfile,
    Event,
    EventRegistration,
    ActivityReport,
    Announcement,
    AuditLog,
    LoginAttempt,
    DonationRecord,
    ImpactStatistic,
    Achievement,
    Collaboration,
    ReminderLog,
)
from .forms import (
    VolunteerForm,
    SupportInquiryForm,
    ContactInquiryForm,
    EmailOrUsernameAuthenticationForm,
    VolunteerRegistrationForm,
    ForgotPasswordRequestForm,
    ResetPasswordConfirmForm,
    ProfileUpdateForm,
    ActivityReportSubmissionForm,
    AnnouncementCreationForm,
)
from .decorators import role_required, admin_required, coordinator_required, volunteer_required


def get_client_ip(request):
    """Safely extract remote IP address for security logging."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


# ============================================================================
# Public Pages
# ============================================================================

def home_view(request):
    """
    Homepage showcasing official foundation mission, story highlight,
    the 11 activity categories, latest published activities, upcoming events,
    gallery previews, verified impact statistics and achievements preview,
    volunteer and donation CTAs, and approved social links.
    """
    settings = FoundationSetting.get_settings()
    activity_categories = ActivityCategory.objects.filter(is_active=True).order_by('order')
    featured_activities = Activity.objects.filter(is_published=True, is_active=True).select_related('category', 'service_area').order_by('order', '-created_at')[:6]
    gallery_media = GalleryMedia.objects.filter(is_published=True).order_by('order', '-created_at')[:6]
    upcoming_events = Event.objects.filter(is_published=True, event_date__gte=date.today(), status='upcoming').order_by('event_date', 'start_time')[:3]
    impact_stats = ImpactStatistic.objects.filter(is_published=True, verification_status='verified').order_by('order')[:4]
    achievements_preview = Achievement.objects.filter(is_published=True, verification_status='verified').order_by('order', '-date_received')[:3]
    collaborations_preview = Collaboration.objects.filter(is_published=True, verification_status='verified').order_by('order')[:4]
    years_of_service = ImpactStatistic.get_calculated_years_of_service()
    recent_stories = Announcement.objects.filter(announcement_type='story', is_published=True, is_active=True).order_by('-created_at')[:3]

    context = {
        'foundation': settings,
        'activity_categories': activity_categories,
        'activities': featured_activities,
        'gallery_media': gallery_media,
        'upcoming_events': upcoming_events,
        'impact_stats': impact_stats,
        'achievements_preview': achievements_preview,
        'collaborations_preview': collaborations_preview,
        'years_of_service': years_of_service,
        'recent_stories': recent_stories,
    }
    return render(request, 'core/home.html', context)


def impact_view(request):
    """
    Dedicated 'Our Impact & Achievements' page presenting:
    1. Verified Impact Statistics (only approved figures, missing metrics hidden)
    2. Genuine Achievements & Recognitions (with supporting certificates/media)
    3. Confirmed Important Collaborations (partners and joint activities)
    Calculates years of service from verified establishment date (January 2024).
    """
    settings = FoundationSetting.get_settings()
    impact_stats = ImpactStatistic.objects.filter(
        is_published=True,
        verification_status='verified'
    ).order_by('order')

    achievements = Achievement.objects.filter(
        is_published=True,
        verification_status='verified'
    ).order_by('order', '-date_received')

    collaborations = Collaboration.objects.filter(
        is_published=True,
        verification_status='verified'
    ).order_by('order')

    years_of_service = ImpactStatistic.get_calculated_years_of_service()

    context = {
        'foundation': settings,
        'impact_stats': impact_stats,
        'achievements': achievements,
        'collaborations': collaborations,
        'years_of_service': years_of_service,
    }
    return render(request, 'core/impact.html', context)


def about_view(request):
    """
    Comprehensive About Us page presenting official story, mission,
    vision, founder details, and values verbatim.
    """
    settings = FoundationSetting.get_settings()
    service_areas = ServiceArea.objects.filter(is_active=True).order_by('order')
    categories = ActivityCategory.objects.filter(is_active=True).order_by('order')

    context = {
        'foundation': settings,
        'service_areas': service_areas,
        'categories': categories,
    }
    return render(request, 'core/about.html', context)


def service_areas_view(request):
    """Detailed presentation of the 7 official key service areas."""
    service_areas = ServiceArea.objects.filter(is_active=True).order_by('order')
    return render(request, 'core/service_areas.html', {'service_areas': service_areas})


def activities_view(request):
    """
    Catalog of ongoing and seasonal social service activities.
    Supports filtering by the 11 Activity Categories and search keyword.
    """
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()

    activities = Activity.objects.filter(is_published=True, is_active=True).select_related('category', 'service_area')
    selected_category = None

    if category_slug:
        selected_category = ActivityCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            activities = activities.filter(category=selected_category)

    if search_query:
        activities = activities.filter(
            Q(title__icontains=search_query) |
            Q(title_mr__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(description_mr__icontains=search_query) |
            Q(venue__icontains=search_query)
        )

    categories = ActivityCategory.objects.filter(is_active=True).annotate(
        active_activities_count=Count('activities', filter=Q(activities__is_published=True, activities__is_active=True))
    ).order_by('order')

    context = {
        'activities': activities,
        'categories': categories,
        'selected_category': selected_category,
        'selected_category_slug': category_slug,
        'search_query': search_query,
    }
    return render(request, 'core/activities.html', context)


def activity_detail_view(request, slug):
    """
    Individual activity detail page.
    Displays bilingual details, category, date, venue, photos/videos,
    and associated upcoming events.
    """
    activity = get_object_or_404(Activity, slug=slug, is_published=True)
    related_events = Event.objects.filter(
        activity=activity,
        is_published=True,
        event_date__gte=date.today(),
        status='upcoming'
    ).order_by('event_date')
    related_activities = Activity.objects.filter(
        category=activity.category,
        is_published=True,
        is_active=True
    ).exclude(id=activity.id)[:3]
    media_items = activity.gallery_media.filter(is_published=True).order_by('order')

    context = {
        'activity': activity,
        'related_events': related_events,
        'related_activities': related_activities,
        'media_items': media_items,
    }
    return render(request, 'core/activity_detail.html', context)


def gallery_view(request):
    """
    Activity visual gallery supporting admin-managed photos and videos.
    Conforms to transparency rules: clean empty state when authentic media is unavailable.
    """
    media_type = request.GET.get('type')  # 'photo', 'video', or None
    category_slug = request.GET.get('category')

    media_items = GalleryMedia.objects.filter(is_published=True).select_related('activity', 'event', 'category')

    if media_type in ['photo', 'video']:
        media_items = media_items.filter(media_type=media_type)

    selected_category = None
    if category_slug:
        selected_category = ActivityCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            media_items = media_items.filter(category=selected_category)

    categories = ActivityCategory.objects.filter(is_active=True).order_by('order')

    context = {
        'gallery_media': media_items,
        'categories': categories,
        'selected_type': media_type or 'all',
        'selected_category': selected_category,
    }
    return render(request, 'core/gallery.html', context)


def events_list_view(request):
    """
    Public listing of upcoming and past events & programs.
    Includes registration status and options when enabled by administrator.
    """
    today = date.today()
    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gte=today
    ).select_related('activity', 'coordinator').order_by('event_date', 'start_time')

    past_events = Event.objects.filter(
        is_published=True,
        event_date__lt=today
    ).select_related('activity', 'coordinator').order_by('-event_date')

    # If volunteer is logged in, fetch list of their registered event IDs
    user_registered_event_ids = []
    if request.user.is_authenticated:
        user_registered_event_ids = list(
            EventRegistration.objects.filter(
                volunteer=request.user,
                status__in=['registered', 'attended']
            ).values_list('event_id', flat=True)
        )

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'user_registered_event_ids': user_registered_event_ids,
    }
    return render(request, 'core/events.html', context)


def announcements_view(request):
    """
    Displays official announcements and impact stories created by authorized administrators.
    """
    filter_type = request.GET.get('type', 'all')
    announcements = Announcement.objects.filter(
        is_published=True,
        is_active=True,
        target_role__in=['all']
    ).order_by('-created_at')

    if filter_type == 'announcement':
        announcements = announcements.filter(announcement_type='announcement')
    elif filter_type == 'story':
        announcements = announcements.filter(announcement_type='story')

    context = {
        'announcements': announcements,
        'filter_type': filter_type,
    }
    return render(request, 'core/announcements.html', context)


def privacy_policy_view(request):
    """Transparent institutional privacy policy for Swayamsevak Foundation."""
    settings = FoundationSetting.get_settings()
    return render(request, 'core/privacy_policy.html', {'foundation': settings})


def custom_404_view(request, exception=None):
    """Custom branded 404 error page."""
    settings = FoundationSetting.get_settings()
    return render(request, '404.html', {'foundation': settings}, status=404)


def volunteer_view(request):
    """Public volunteer registration inquiry page."""
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            messages.success(
                request,
                f"Thank you, {volunteer.full_name}! Your volunteer registration inquiry has been received. "
                "Our team will connect with you soon on your provided phone number."
            )
            return redirect('volunteer')
        else:
            messages.error(
                request,
                "Please correct the errors in the form below to complete your registration."
            )
    else:
        form = VolunteerForm()

    context = {'form': form}
    return render(request, 'core/volunteer.html', context)


def support_view(request):
    """Support Our Work page with contribution inquiry form and transparent notice."""
    if request.method == 'POST':
        form = SupportInquiryForm(request.POST)
        if form.is_valid():
            pledge = form.save()
            messages.success(
                request,
                f"Heartfelt thanks, {pledge.supporter_name}! Your support pledge for "
                f"'{pledge.get_support_type_display()}' has been recorded. "
                "Foundation representatives will contact you directly to coordinate."
            )
            return redirect('support')
        else:
            messages.error(
                request,
                "Please verify the details in the form below and resubmit."
            )
    else:
        form = SupportInquiryForm()

    context = {'form': form}
    return render(request, 'core/support.html', context)


def contact_view(request):
    """Official contact page with address, email, phone, and inquiry form."""
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            messages.success(
                request,
                f"Thank you, {inquiry.name}. Your message has been sent successfully. "
                "We will get back to you shortly."
            )
            return redirect('contact')
        else:
            messages.error(
                request,
                "There was an error in submitting your message. Please check the fields below."
            )
    else:
        form = ContactInquiryForm()

    context = {'form': form}
    return render(request, 'core/contact.html', context)


def switch_language_view(request, lang_code):
    """Switches active website language between English ('en') and Marathi ('mr')."""
    if lang_code in ['en', 'mr']:
        request.session['site_lang'] = lang_code

    next_url = request.META.get('HTTP_REFERER')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return HttpResponseRedirect(next_url)
    return redirect('home')


# ============================================================================
# Authentication Views (Login, Register, Logout, Password Reset)
# ============================================================================

def login_view(request):
    """
    Role-aware login view with rate limiting / brute-force protection.
    Accepts both username and registered email.
    Redirects user directly to their role-specific dashboard.
    """
    if request.user.is_authenticated:
        profile = UserProfile.get_profile_for_user(request.user)
        if profile.is_admin_role:
            return redirect('admin_dashboard')
        elif profile.is_coordinator_role:
            return redirect('coordinator_dashboard')
        return redirect('volunteer_dashboard')

    ip = get_client_ip(request)

    if request.method == 'POST':
        raw_identifier = request.POST.get('username_or_email', '').strip()

        # Brute-force throttling check
        is_locked, remaining_minutes = LoginAttempt.is_locked(raw_identifier, ip)
        if is_locked:
            messages.error(
                request,
                f"Too many failed login attempts. For security, access is temporarily locked. "
                f"Please try again in {remaining_minutes} minute(s)."
            )
            form = EmailOrUsernameAuthenticationForm(request.POST)
            return render(request, 'core/login.html', {'form': form, 'is_locked': True})

        form = EmailOrUsernameAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            profile = UserProfile.get_profile_for_user(user)

            # Check account status
            if profile.status == 'suspended':
                messages.error(request, "Your account has been temporarily suspended by an administrator.")
                return render(request, 'core/login.html', {'form': form})
            elif profile.status == 'deactivated':
                messages.error(request, "This account is deactivated. Please contact foundation administration.")
                return render(request, 'core/login.html', {'form': form})

            # Record success and reset failure counters
            LoginAttempt.record_success(raw_identifier, ip)
            login(request, user)

            AuditLog.log_action(
                user=user,
                action="LOGIN_SUCCESS",
                target_repr=f"User {user.username} logged in as {profile.get_role_display()}",
                ip_address=ip
            )

            messages.success(request, f"Welcome back, {user.first_name or user.username}!")

            # Safe redirect: evaluate next param if permitted, otherwise role-based dashboard
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            if profile.is_admin_role:
                return redirect('admin_dashboard')
            elif profile.is_coordinator_role:
                return redirect('coordinator_dashboard')
            else:
                return redirect('volunteer_dashboard')
        else:
            LoginAttempt.record_failure(raw_identifier, ip)
            AuditLog.log_action(
                user=None,
                action="LOGIN_FAILED",
                target_repr=f"Failed login attempt for identifier: {raw_identifier}",
                ip_address=ip
            )
            messages.error(request, "Invalid username/email or password. Please try again.")
    else:
        form = EmailOrUsernameAuthenticationForm()

    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'core/login.html', context)


def register_view(request):
    """
    Public volunteer sign-up page.
    Enforces privacy consent, password hashing, and initializes pending approval state.
    """
    if request.user.is_authenticated:
        return redirect('volunteer_dashboard')

    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ip = get_client_ip(request)

            AuditLog.log_action(
                user=user,
                action="VOLUNTEER_SIGNUP",
                target_repr=f"Volunteer {user.username} registered (Status: Pending)",
                ip_address=ip
            )

            # Log the volunteer in automatically
            login(request, user)
            messages.success(
                request,
                f"Welcome to Swayamsevak Foundation, {user.first_name}! Your volunteer account has been created. "
                "Your registration is currently pending administrative verification. "
                "You can explore drives and update your profile below."
            )
            return redirect('volunteer_dashboard')
        else:
            messages.error(request, "Please correct the errors in the registration form below.")
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    """Secure logout view with audit logging."""
    if request.user.is_authenticated:
        AuditLog.log_action(
            user=request.user,
            action="LOGOUT",
            target_repr=f"User {request.user.username} logged out",
            ip_address=get_client_ip(request)
        )
        logout(request)
        messages.info(request, "You have been logged out safely.")
    return redirect('login')


def forgot_password_view(request):
    """
    Initiates password reset workflow.
    Generates secure cryptographic tokens and logs recovery links.
    """
    reset_link_preview = None

    if request.method == 'POST':
        form = ForgotPasswordRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
            user = User.objects.filter(email__iexact=email).first()

            if user:
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                )
                reset_link_preview = reset_link

                AuditLog.log_action(
                    user=user,
                    action="PASSWORD_RESET_TOKEN_GENERATED",
                    target_repr=f"Reset token generated for {user.username}",
                    ip_address=get_client_ip(request)
                )

            messages.success(
                request,
                "If an account is associated with this email address, a password reset link has been dispatched."
            )
    else:
        form = ForgotPasswordRequestForm()

    context = {
        'form': form,
        'reset_link_preview': reset_link_preview,
    }
    return render(request, 'core/forgot_password.html', context)


def password_reset_confirm_view(request, uidb64, token):
    """Verifies reset token and updates the user password."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    validlink = bool(user and default_token_generator.check_token(user, token))

    if not validlink:
        messages.error(request, "The password reset link is invalid or has expired. Please request a new one.")
        return render(request, 'core/password_reset_confirm.html', {'validlink': False})

    if request.method == 'POST':
        form = ResetPasswordConfirmForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()

            AuditLog.log_action(
                user=user,
                action="PASSWORD_RESET_SUCCESS",
                target_repr=f"Password updated for {user.username}",
                ip_address=get_client_ip(request)
            )

            messages.success(request, "Your password has been reset successfully! You can now log in.")
            return redirect('login')
    else:
        form = ResetPasswordConfirmForm()

    context = {
        'form': form,
        'validlink': True,
        'uidb64': uidb64,
        'token': token,
    }
    return render(request, 'core/password_reset_confirm.html', context)


# ============================================================================
# User Profile View
# ============================================================================

@login_required(login_url='/login/')
def profile_view(request):
    """
    Authenticated user profile view.
    Allows editing contact details and volunteer preferences while strictly preventing role escalation.
    """
    profile = UserProfile.get_profile_for_user(request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            AuditLog.log_action(
                user=request.user,
                action="PROFILE_UPDATED",
                target_repr=f"User {request.user.username} updated profile",
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Your profile information has been saved successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please check the highlighted errors in your profile form.")
    else:
        form = ProfileUpdateForm(request.user)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)


# ============================================================================
# Role-Based Dashboards
# ============================================================================

@admin_required
def admin_dashboard_view(request):
    """
    Administrator Dashboard.
    Provides verified metrics, pending volunteer applications, coordinator assignments,
    activity report reviews, donation inquiries, and audit logs.
    """
    # Real database statistics
    total_volunteers = UserProfile.objects.filter(role='volunteer').count()
    pending_volunteers_count = UserProfile.objects.filter(role='volunteer', status='pending').count()
    active_coordinators_count = UserProfile.objects.filter(role='coordinator', status='approved').count()
    total_events_count = Event.objects.count()
    upcoming_events_count = Event.objects.filter(event_date__gte=date.today(), status='upcoming').count()
    pending_reports_count = ActivityReport.objects.filter(status='pending').count()
    total_support_inquiries = SupportInquiry.objects.count()
    total_contact_inquiries = ContactInquiry.objects.count()

    # Lists for management
    pending_volunteers = UserProfile.objects.filter(
        role='volunteer',
        status='pending'
    ).select_related('user').order_by('-created_at')[:10]

    all_volunteers = UserProfile.objects.filter(
        role='volunteer'
    ).select_related('user').order_by('-created_at')[:15]

    coordinators = UserProfile.objects.filter(
        role='coordinator'
    ).select_related('user').prefetch_related('assigned_activities').order_by('-created_at')

    upcoming_events = Event.objects.filter(
        event_date__gte=date.today()
    ).select_related('activity', 'coordinator', 'service_area').order_by('event_date')[:10]

    pending_reports = ActivityReport.objects.filter(
        status='pending'
    ).select_related('event', 'coordinator').order_by('-submitted_at')

    recent_support_pledges = SupportInquiry.objects.order_by('-created_at')[:8]
    recent_contact_inquiries = ContactInquiry.objects.order_by('-created_at')[:8]
    recent_audit_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:15]
    announcements = Announcement.objects.select_related('created_by', 'event').order_by('-created_at')[:6]

    all_activities = Activity.objects.filter(is_active=True).order_by('title')

    context = {
        'total_volunteers': total_volunteers,
        'pending_volunteers_count': pending_volunteers_count,
        'active_coordinators_count': active_coordinators_count,
        'total_events_count': total_events_count,
        'upcoming_events_count': upcoming_events_count,
        'pending_reports_count': pending_reports_count,
        'total_support_inquiries': total_support_inquiries,
        'total_contact_inquiries': total_contact_inquiries,
        'pending_volunteers': pending_volunteers,
        'all_volunteers': all_volunteers,
        'coordinators': coordinators,
        'upcoming_events': upcoming_events,
        'pending_reports': pending_reports,
        'recent_support_pledges': recent_support_pledges,
        'recent_contact_inquiries': recent_contact_inquiries,
        'recent_audit_logs': recent_audit_logs,
        'announcements': announcements,
        'all_activities': all_activities,
    }
    return render(request, 'core/admin_dashboard.html', context)


@volunteer_required
def volunteer_dashboard_view(request):
    """
    Volunteer Dashboard.
    Displays profile overview, approval status, registered events,
    participation history, vacancies in upcoming events, and official announcements.
    """
    profile = UserProfile.get_profile_for_user(request.user)

    # User's registrations
    my_registrations = EventRegistration.objects.filter(
        volunteer=request.user
    ).select_related('event', 'event__activity', 'event__coordinator').order_by('event__event_date')

    registered_event_ids = my_registrations.values_list('event_id', flat=True)

    # Upcoming registered events
    upcoming_registrations = my_registrations.filter(
        event__event_date__gte=date.today(),
        status='registered'
    )

    # Past participation history
    past_participations = my_registrations.filter(
        Q(status='attended') | Q(event__event_date__lt=date.today())
    )

    # Browse upcoming events (not yet registered)
    available_events = Event.objects.filter(
        event_date__gte=date.today(),
        status='upcoming'
    ).exclude(id__in=registered_event_ids).select_related('activity', 'service_area', 'coordinator').order_by('event_date')[:8]

    # Official announcements for volunteers
    announcements = Announcement.objects.filter(
        Q(target_role__in=['all', 'volunteer']),
        is_active=True
    ).select_related('created_by', 'event').order_by('-priority', '-created_at')[:5]

    context = {
        'profile': profile,
        'upcoming_registrations': upcoming_registrations,
        'past_participations': past_participations,
        'available_events': available_events,
        'announcements': announcements,
        'total_attended': my_registrations.filter(status='attended').count(),
    }
    return render(request, 'core/volunteer_dashboard.html', context)


@coordinator_required
def coordinator_dashboard_view(request):
    """
    Coordinator Dashboard.
    Displays assigned activities and events, roster of registered volunteers,
    attendance recording links, and activity report submissions.
    Strictly isolated: coordinators cannot view unassigned events or administrative settings.
    """
    profile = UserProfile.get_profile_for_user(request.user)

    # Fetch only assigned events
    assigned_activity_ids = profile.assigned_activities.values_list('id', flat=True)
    assigned_events = Event.objects.filter(
        Q(coordinator=request.user) | Q(activity_id__in=assigned_activity_ids)
    ).select_related('activity', 'service_area').distinct().order_by('event_date')

    upcoming_assigned = assigned_events.filter(event_date__gte=date.today())
    past_assigned = assigned_events.filter(event_date__lt=date.today()).order_by('-event_date')

    # Submitted reports by this coordinator
    my_reports = ActivityReport.objects.filter(
        coordinator=request.user
    ).select_related('event', 'reviewed_by').order_by('-submitted_at')

    # Announcements for coordinators
    announcements = Announcement.objects.filter(
        Q(target_role__in=['all', 'coordinator']),
        is_active=True
    ).order_by('-created_at')[:5]

    context = {
        'profile': profile,
        'assigned_events': assigned_events,
        'upcoming_assigned': upcoming_assigned,
        'past_assigned': past_assigned,
        'my_reports': my_reports,
        'announcements': announcements,
    }
    return render(request, 'core/coordinator_dashboard.html', context)


# ============================================================================
# Operational Actions (Registration, Attendance, Status Updates, Reports)
# ============================================================================

@volunteer_required
def event_register_view(request, event_id):
    """Allows an approved volunteer to register for an upcoming event."""
    event = get_object_or_404(Event, id=event_id, status='upcoming')
    profile = UserProfile.get_profile_for_user(request.user)

    if profile.status != 'approved':
        messages.warning(
            request,
            "Your volunteer account is currently pending administrative approval. "
            "Event registrations activate once your account is verified."
        )
        return redirect('volunteer_dashboard')

    if event.is_full:
        messages.error(request, f"Sorry, '{event.title}' has reached its volunteer capacity.")
        return redirect('volunteer_dashboard')

    registration, created = EventRegistration.objects.get_or_create(
        event=event,
        volunteer=request.user,
        defaults={'status': 'registered'}
    )

    if created:
        AuditLog.log_action(
            user=request.user,
            action="EVENT_REGISTERED",
            target_repr=f"Volunteer registered for {event.title}",
            ip_address=get_client_ip(request)
        )
        messages.success(request, f"You are successfully registered for '{event.title}' on {event.event_date}!")
    else:
        if registration.status == 'cancelled':
            registration.status = 'registered'
            registration.save()
            messages.success(request, f"Your registration for '{event.title}' has been re-activated.")
        else:
            messages.info(request, f"You are already registered for '{event.title}'.")

    return redirect('volunteer_dashboard')


@volunteer_required
def event_cancel_registration_view(request, event_id):
    """Allows a volunteer to cancel their own registration (IDOR protected)."""
    registration = get_object_or_404(EventRegistration, event_id=event_id, volunteer=request.user)
    event_title = registration.event.title

    registration.status = 'cancelled'
    registration.save()

    AuditLog.log_action(
        user=request.user,
        action="EVENT_REGISTRATION_CANCELLED",
        target_repr=f"Registration cancelled for {event_title}",
        ip_address=get_client_ip(request)
    )

    messages.info(request, f"Your registration for '{event_title}' has been cancelled.")
    return redirect('volunteer_dashboard')


@coordinator_required
def coordinator_attendance_view(request, event_id):
    """
    Allows a coordinator to record/update attendance for an assigned event.
    Strictly verifies event ownership/assignment to prevent IDOR attacks.
    """
    event = get_object_or_404(Event, id=event_id)
    profile = UserProfile.get_profile_for_user(request.user)

    # Permission check: must be designated coordinator or assigned to event's activity
    is_assigned = (
        event.coordinator_id == request.user.id or
        profile.assigned_activities.filter(id=event.activity_id).exists() or
        profile.is_admin_role
    )

    if not is_assigned:
        return HttpResponseForbidden("Access Denied: You are not authorized to manage attendance for this event.")

    registrations = EventRegistration.objects.filter(
        event=event
    ).select_related('volunteer', 'volunteer__profile').order_by('volunteer__first_name')

    if request.method == 'POST':
        attended_ids = request.POST.getlist('attended_volunteers')
        now = timezone.now()

        for reg in registrations:
            volunteer_id_str = str(reg.volunteer_id)
            if volunteer_id_str in attended_ids:
                reg.status = 'attended'
            else:
                reg.status = 'absent'
            reg.attendance_marked_at = now
            reg.attendance_marked_by = request.user
            reg.save()

        AuditLog.log_action(
            user=request.user,
            action="ATTENDANCE_RECORDED",
            target_repr=f"Attendance recorded for {event.title} ({len(attended_ids)} attended)",
            ip_address=get_client_ip(request)
        )

        messages.success(request, f"Attendance updated successfully for '{event.title}'.")
        return redirect('coordinator_dashboard')

    context = {
        'event': event,
        'registrations': registrations,
    }
    return render(request, 'core/coordinator_attendance.html', context)


@coordinator_required
def coordinator_submit_report_view(request, event_id):
    """
    Allows coordinators to submit on-ground activity reports and photos for admin review.
    Enforces authorization check on event.
    """
    event = get_object_or_404(Event, id=event_id)
    profile = UserProfile.get_profile_for_user(request.user)

    is_assigned = (
        event.coordinator_id == request.user.id or
        profile.assigned_activities.filter(id=event.activity_id).exists() or
        profile.is_admin_role
    )

    if not is_assigned:
        return HttpResponseForbidden("Access Denied: You are not authorized to submit reports for this event.")

    if request.method == 'POST':
        form = ActivityReportSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.event = event
            report.coordinator = request.user
            report.status = 'pending'
            report.save()

            AuditLog.log_action(
                user=request.user,
                action="ACTIVITY_REPORT_SUBMITTED",
                target_repr=f"Report '{report.title}' submitted for {event.title}",
                ip_address=get_client_ip(request)
            )

            messages.success(
                request,
                f"Report '{report.title}' submitted successfully! It is now pending administrator review."
            )
            return redirect('coordinator_dashboard')
    else:
        attended_count = EventRegistration.objects.filter(event=event, status='attended').count()
        form = ActivityReportSubmissionForm(initial={
            'title': f"Drive Report: {event.title}",
            'volunteers_present_count': attended_count,
        })

    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'core/coordinator_submit_report.html', context)


@admin_required
def admin_update_volunteer_status_view(request, profile_id, new_status):
    """
    Administrator action to approve, suspend, or deactivate volunteer accounts.
    """
    target_profile = get_object_or_404(UserProfile, id=profile_id)

    if new_status not in ['approved', 'suspended', 'deactivated', 'pending']:
        messages.error(request, "Invalid status choice.")
        return redirect('admin_dashboard')

    old_status = target_profile.status
    target_profile.status = new_status
    if new_status == 'approved':
        target_profile.approved_by = request.user
        target_profile.approved_at = timezone.now()
    target_profile.save()

    # Also sync legacy Volunteer record if present
    Volunteer.objects.filter(user=target_profile.user).update(status=new_status)

    AuditLog.log_action(
        user=request.user,
        action="VOLUNTEER_STATUS_UPDATED",
        target_repr=f"Volunteer {target_profile.user.username} status: {old_status} -> {new_status}",
        ip_address=get_client_ip(request)
    )

    messages.success(
        request,
        f"Volunteer '{target_profile.user.get_full_name() or target_profile.user.username}' marked as '{target_profile.get_status_display()}'."
    )
    return redirect('admin_dashboard')


@admin_required
def admin_assign_coordinator_view(request):
    """
    Administrator action to assign or unassign coordinators to activities.
    """
    if request.method == 'POST':
        coordinator_id = request.POST.get('coordinator_id')
        activity_id = request.POST.get('activity_id')
        action = request.POST.get('action', 'add')

        coord_profile = get_object_or_404(UserProfile, id=coordinator_id, role='coordinator')
        activity = get_object_or_404(Activity, id=activity_id)

        if action == 'add':
            coord_profile.assigned_activities.add(activity)
            msg = f"Assigned coordinator {coord_profile.user.username} to '{activity.title}'."
        else:
            coord_profile.assigned_activities.remove(activity)
            msg = f"Removed coordinator {coord_profile.user.username} from '{activity.title}'."

        AuditLog.log_action(
            user=request.user,
            action="COORDINATOR_ASSIGNMENT_CHANGED",
            target_repr=msg,
            ip_address=get_client_ip(request)
        )

        messages.success(request, msg)
    return redirect('admin_dashboard')


@admin_required
def admin_review_report_view(request, report_id):
    """
    Administrator action to review and approve/reject activity reports.
    """
    report = get_object_or_404(ActivityReport, id=report_id)

    if request.method == 'POST':
        action = request.POST.get('review_action')
        remarks = request.POST.get('admin_feedback', '')

        if action in ['approved', 'rejected']:
            report.status = action
            report.admin_feedback = remarks
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.save()

            AuditLog.log_action(
                user=request.user,
                action=f"ACTIVITY_REPORT_{action.upper()}",
                target_repr=f"Report '{report.title}' marked as {action}",
                details=remarks,
                ip_address=get_client_ip(request)
            )

            messages.success(request, f"Report '{report.title}' marked as {report.get_status_display()}.")

    return redirect('admin_dashboard')


@admin_required
def admin_create_announcement_view(request):
    """Administrator action to publish official announcements."""
    if request.method == 'POST':
        form = AnnouncementCreationForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()

            AuditLog.log_action(
                user=request.user,
                action="ANNOUNCEMENT_CREATED",
                target_repr=f"Announcement '{announcement.title}' published for {announcement.get_target_role_display()}",
                ip_address=get_client_ip(request)
            )

            messages.success(request, f"Announcement '{announcement.title}' published successfully.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Please check the form inputs.")
    return redirect('admin_dashboard')


# Retain legacy staff_dashboard_view redirecting to admin_dashboard
@login_required(login_url='/login/')
def staff_dashboard_view(request):
    """Redirects to the new comprehensive admin dashboard."""
    profile = UserProfile.get_profile_for_user(request.user)
    if profile.is_admin_role:
        return redirect('admin_dashboard')
    elif profile.is_coordinator_role:
        return redirect('coordinator_dashboard')
    return redirect('volunteer_dashboard')
