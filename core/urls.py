"""
URL configuration for core foundation features.
Includes public pages, authentication, role-based dashboards, and event operations.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('initiatives/', views.service_areas_view, name='service_areas'),
    path('activities/', views.activities_view, name='activities'),
    path('activities/<slug:slug>/', views.activity_detail_view, name='activity_detail'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('events/', views.events_list_view, name='events'),
    path('volunteer/', views.volunteer_view, name='volunteer'),
    path('donate/', views.support_view, name='donate'),
    path('support-our-work/', views.support_view, name='support'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('impact/', views.impact_view, name='impact'),
    path('achievements/', views.impact_view, name='achievements'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('switch-language/<str:lang_code>/', views.switch_language_view, name='switch_language'),

    # Role-Based Authentication & Account Management
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('profile/', views.profile_view, name='profile'),

    # Role-Based Dashboards
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('volunteer-dashboard/', views.volunteer_dashboard_view, name='volunteer_dashboard'),
    path('coordinator-dashboard/', views.coordinator_dashboard_view, name='coordinator_dashboard'),
    path('portal/dashboard/', views.staff_dashboard_view, name='staff_dashboard'),

    # Operational Event & Volunteer Actions
    path('events/<int:event_id>/register/', views.event_register_view, name='event_register'),
    path('events/<int:event_id>/cancel/', views.event_cancel_registration_view, name='event_cancel'),
    path('coordinator/event/<int:event_id>/attendance/', views.coordinator_attendance_view, name='coordinator_attendance'),
    path('coordinator/event/<int:event_id>/report/', views.coordinator_submit_report_view, name='coordinator_submit_report'),

    # Administrative Actions
    path('manage/volunteers/<int:profile_id>/status/<str:new_status>/', views.admin_update_volunteer_status_view, name='admin_update_volunteer_status'),
    path('manage/coordinators/assign/', views.admin_assign_coordinator_view, name='admin_assign_coordinator'),
    path('manage/reports/<int:report_id>/review/', views.admin_review_report_view, name='admin_review_report'),
    path('manage/announcements/create/', views.admin_create_announcement_view, name='admin_create_announcement'),
]
