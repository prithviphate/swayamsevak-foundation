"""
Admin configuration for Swayamsevak Foundation.
Customized with filters, search, actions, and status badges.
"""

from django.contrib import admin
from django.utils.html import format_html
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


@admin.register(FoundationSetting)
class FoundationSettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Foundation Identity & Branding", {
            "fields": (
                "name",
                "logo",
                "logo_preview",
                "tagline_mr",
                "tagline_en",
                "established_date",
                "founder_president",
                "city",
                "belief",
                "belief_mr",
            )
        }),
        ("Official Contact Details", {
            "fields": (
                "phone",
                "email",
                "address",
                "languages_supported",
            )
        }),
        ("Official Social Media Links", {
            "fields": (
                "instagram_url",
                "youtube_url",
                "whatsapp_group_url",
                "facebook_status",
            )
        }),
        ("Official Story", {
            "fields": (
                "our_story_title",
                "our_story_title_mr",
                "our_story_text",
                "our_story_text_mr",
            )
        }),
        ("Official Mission & Vision", {
            "fields": (
                "mission_text",
                "mission_text_mr",
                "vision_text",
                "vision_text_mr",
            )
        }),
        ("Contribution & Support Transparency", {
            "fields": (
                "support_note",
                "support_note_mr",
            )
        }),
    )
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj and obj.logo_url:
            return format_html(
                '<img src="{}" style="height: 90px; width: 90px; object-fit: contain; '
                'border-radius: 50%; border: 2px solid #ea580c; background: #fff; padding: 2px;" />',
                obj.logo_url
            )
        return "No logo configured"
    logo_preview.short_description = "Active Logo Preview"

    def has_add_permission(self, request):
        # Enforce singleton pattern
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'title_mr', 'icon_preview', 'is_active')
    list_display_links = ('title',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'title_mr', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

    def icon_preview(self, obj):
        return format_html('<i class="bi {}" style="font-size: 1.2rem;"></i> {}', obj.icon_bootstrap, obj.icon_bootstrap)
    icon_preview.short_description = "Icon"


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'name_mr', 'icon_preview', 'activities_count', 'is_active')
    list_display_links = ('name',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'name_mr', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def icon_preview(self, obj):
        return format_html('<i class="bi {}" style="font-size: 1.2rem; color: #b84a1a;"></i> <code>{}</code>', obj.icon_bootstrap, obj.icon_bootstrap)
    icon_preview.short_description = "Icon"

    def activities_count(self, obj):
        return obj.activities.count()
    activities_count.short_description = "Activities"


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'service_area', 'venue', 'status_badge', 'is_published', 'order', 'is_active')
    list_filter = ('category', 'status', 'is_published', 'is_active')
    search_fields = ('title', 'title_mr', 'description', 'venue')
    list_editable = ('order', 'is_published', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

    def status_badge(self, obj):
        badge_colors = {
            'regular': '#198754',
            'seasonal': '#fd7e14',
            'planned': '#0d6efd',
        }
        color = badge_colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Drive Frequency/Status"


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'city_area', 'availability', 'blood_group', 'status_badge', 'created_at')
    list_filter = ('status', 'availability', 'blood_group', 'preferred_service_area')
    search_fields = ('full_name', 'phone', 'email', 'city_area', 'motivation')
    date_hierarchy = 'created_at'
    actions = ['mark_as_approved', 'mark_as_contacted']

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'approved': '#198754',
            'contacted': '#0dcaf0',
            'inactive': '#6c757d',
        }
        text_color = '#000' if obj.status in ['pending', 'contacted'] else '#fff'
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            text_color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected volunteers as Approved")
    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Mark selected volunteers as Contacted")
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')


@admin.register(SupportInquiry)
class SupportInquiryAdmin(admin.ModelAdmin):
    list_display = ('supporter_name', 'phone', 'support_type', 'preferred_mode', 'status_badge', 'created_at')
    list_filter = ('status', 'support_type', 'preferred_mode')
    search_fields = ('supporter_name', 'phone', 'email', 'message')
    date_hierarchy = 'created_at'
    actions = ['mark_as_contacted', 'mark_as_completed']

    def status_badge(self, obj):
        colors = {
            'new': '#ffc107',
            'contacted': '#0d6efd',
            'completed': '#198754',
            'archived': '#6c757d',
        }
        text_color = '#000' if obj.status == 'new' else '#fff'
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            text_color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected inquiries as Contacted")
    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')

    @admin.action(description="Mark selected inquiries as Completed")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'status_badge', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_responded']

    def status_badge(self, obj):
        colors = {
            'new': '#dc3545',
            'read': '#ffc107',
            'responded': '#198754',
            'closed': '#6c757d',
        }
        text_color = '#000' if obj.status == 'read' else '#fff'
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            text_color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected inquiries as Read")
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')

    @admin.action(description="Mark selected inquiries as Responded")
    def mark_as_responded(self, request, queryset):
        queryset.update(status='responded')


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_area', 'placeholder_label', 'is_featured', 'order')
    list_filter = ('service_area', 'is_featured')
    search_fields = ('title', 'title_mr', 'caption')
    list_editable = ('order', 'is_featured')


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'media_preview', 'activity', 'category', 'is_published', 'is_featured', 'order', 'created_at')
    list_filter = ('media_type', 'is_published', 'is_featured', 'category')
    search_fields = ('title', 'title_mr', 'caption')
    list_editable = ('is_published', 'is_featured', 'order')

    def media_preview(self, obj):
        if obj.media_type == 'photo' and obj.image:
            return format_html('<img src="{}" style="height: 50px; width: 75px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        elif obj.media_type == 'video' and obj.video_url:
            return format_html('<a href="{}" target="_blank"><i class="bi bi-play-circle-fill text-danger fs-5"></i> Video</a>', obj.video_url)
        return "No Media"
    media_preview.short_description = "Preview"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'role_badge', 'status_badge', 'phone', 'city', 'created_at')
    list_filter = ('role', 'status')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone', 'city')
    actions = ['approve_users', 'suspend_users', 'deactivate_users']
    filter_horizontal = ('assigned_activities',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = "Username"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"

    def role_badge(self, obj):
        colors = {'admin': '#dc3545', 'coordinator': '#0d6efd', 'volunteer': '#198754'}
        return format_html(
            '<span style="background:{}; color:#fff; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:12px;">{}</span>',
            colors.get(obj.role, '#6c757d'),
            obj.get_role_display()
        )
    role_badge.short_description = "Role"

    def status_badge(self, obj):
        colors = {'approved': '#198754', 'pending': '#ffc107', 'suspended': '#fd7e14', 'deactivated': '#dc3545'}
        text_color = '#000' if obj.status == 'pending' else '#fff'
        return format_html(
            '<span style="background:{}; color:{}; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:12px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            text_color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Approve selected user accounts")
    def approve_users(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Suspend selected user accounts")
    def suspend_users(self, request, queryset):
        queryset.update(status='suspended')

    @admin.action(description="Deactivate selected user accounts")
    def deactivate_users(self, request, queryset):
        queryset.update(status='deactivated')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'start_time', 'location', 'coordinator', 'capacity_display', 'status')
    list_filter = ('status', 'event_date', 'service_area')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}

    def capacity_display(self, obj):
        return f"{obj.registered_count} / {obj.max_volunteers}"
    capacity_display.short_description = "Volunteers"


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('volunteer_name', 'event_title', 'status', 'registered_at', 'attendance_marked_at')
    list_filter = ('status', 'event__event_date')
    search_fields = ('volunteer__username', 'volunteer__email', 'event__title')

    def volunteer_name(self, obj):
        return obj.volunteer.get_full_name() or obj.volunteer.username
    volunteer_name.short_description = "Volunteer"

    def event_title(self, obj):
        return obj.event.title
    event_title.short_description = "Event"


@admin.register(ActivityReport)
class ActivityReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'coordinator', 'volunteers_present_count', 'beneficiaries_served_count', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('title', 'summary', 'coordinator__username')
    actions = ['approve_reports', 'reject_reports']

    @admin.action(description="Approve selected activity reports")
    def approve_reports(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Reject selected activity reports")
    def reject_reports(self, request, queryset):
        queryset.update(status='rejected')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_type', 'target_role', 'priority', 'is_published', 'is_active', 'created_by', 'created_at')
    list_filter = ('announcement_type', 'target_role', 'priority', 'is_published', 'is_active')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(DonationRecord)
class DonationRecordAdmin(admin.ModelAdmin):
    list_display = ('supporter_name', 'phone', 'donation_type', 'quantity_or_amount', 'status_badge', 'is_public', 'created_at')
    list_filter = ('donation_type', 'status', 'is_public')
    search_fields = ('supporter_name', 'phone', 'email', 'city', 'receipt_number')
    date_hierarchy = 'created_at'

    def status_badge(self, obj):
        colors = {
            'pledged': '#0d6efd',
            'received': '#198754',
            'distributed': '#0dcaf0',
            'cancelled': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = "Status"


@admin.register(ImpactStatistic)
class ImpactStatisticAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'metric_key',
        'display_val',
        'verification_badge',
        'is_published',
        'order',
        'reporting_period',
        'last_updated_date'
    )
    list_filter = ('verification_status', 'is_published', 'metric_key')
    search_fields = ('title', 'title_mr', 'metric_value', 'internal_verification_notes')
    fieldsets = (
        ("Metric Identity & Figures", {
            "fields": (
                "metric_key",
                "title",
                "title_mr",
                "numeric_value",
                "metric_value",
                "unit_label",
                "unit_label_mr",
                "description",
                "description_mr",
            )
        }),
        ("Audit & Verification (Strictly Confidential / Internal)", {
            "fields": (
                "verification_status",
                "internal_verification_notes",
                "verified_by",
                "verified_date",
                "reporting_period",
                "last_updated_date",
            )
        }),
        ("Display & Ordering", {
            "fields": (
                "icon_bootstrap",
                "order",
                "is_published",
            )
        }),
    )
    actions = ['mark_as_verified_and_published', 'unpublish_selected', 'archive_selected']

    def display_val(self, obj):
        return obj.display_value
    display_val.short_description = "Value"

    def verification_badge(self, obj):
        colors = {
            'verified': '#198754',
            'pending': '#ffc107',
            'rejected': '#dc3545',
            'archived': '#6c757d',
        }
        text_color = '#000' if obj.verification_status == 'pending' else '#fff'
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.verification_status, '#6c757d'),
            text_color,
            obj.get_verification_status_display()
        )
    verification_badge.short_description = "Verification"

    @admin.action(description="Verify and Publish selected statistics")
    def mark_as_verified_and_published(self, request, queryset):
        queryset.update(
            verification_status='verified',
            is_published=True,
            verified_by=request.user,
            verified_date=timezone.now().date()
        )

    @admin.action(description="Unpublish selected statistics")
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Archive selected statistics")
    def archive_selected(self, request, queryset):
        queryset.update(verification_status='archived', is_published=False)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'awarding_organization',
        'date_received',
        'verification_badge',
        'is_published',
        'order'
    )
    list_filter = ('verification_status', 'is_published', 'date_received')
    search_fields = ('title', 'title_mr', 'awarding_organization', 'description', 'internal_verification_notes')
    fieldsets = (
        ("Recognition & Award Information", {
            "fields": (
                "title",
                "title_mr",
                "awarding_organization",
                "awarding_organization_mr",
                "date_received",
            )
        }),
        ("Citation & Official Media", {
            "fields": (
                "description",
                "description_mr",
                "supporting_media",
            )
        }),
        ("Audit & Verification (Strictly Confidential / Internal)", {
            "fields": (
                "verification_status",
                "internal_verification_notes",
                "verified_by",
                "verified_date",
            )
        }),
        ("Publishing & Display", {
            "fields": (
                "order",
                "is_published",
            )
        }),
    )
    actions = ['mark_as_verified_and_published', 'unpublish_selected', 'archive_selected']

    def verification_badge(self, obj):
        colors = {
            'verified': '#198754',
            'pending': '#ffc107',
            'rejected': '#dc3545',
            'archived': '#6c757d',
        }
        text_color = '#000' if obj.verification_status == 'pending' else '#fff'
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.verification_status, '#6c757d'),
            text_color,
            obj.get_verification_status_display()
        )
    verification_badge.short_description = "Verification"

    @admin.action(description="Verify and Publish selected achievements")
    def mark_as_verified_and_published(self, request, queryset):
        queryset.update(
            verification_status='verified',
            is_published=True,
            verified_by=request.user,
            verified_date=timezone.now().date()
        )

    @admin.action(description="Unpublish selected achievements")
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Archive selected achievements")
    def archive_selected(self, request, queryset):
        queryset.update(verification_status='archived', is_published=False)


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = (
        'organization_name',
        'collaboration_period',
        'verification_badge',
        'is_published',
        'order'
    )
    list_filter = ('verification_status', 'is_published')
    search_fields = (
        'organization_name',
        'organization_name_mr',
        'collaboration_purpose',
        'activities_conducted',
        'internal_verification_notes'
    )
    fieldsets = (
        ("Partner Institution Details", {
            "fields": (
                "organization_name",
                "organization_name_mr",
                "collaboration_period",
                "partner_logo",
                "partner_website",
            )
        }),
        ("Scope, Purpose & Joint Activities", {
            "fields": (
                "collaboration_purpose",
                "collaboration_purpose_mr",
                "activities_conducted",
                "activities_conducted_mr",
            )
        }),
        ("Audit & Verification (Strictly Confidential / Internal)", {
            "fields": (
                "verification_status",
                "internal_verification_notes",
                "verified_by",
                "verified_date",
            )
        }),
        ("Publishing & Ordering", {
            "fields": (
                "order",
                "is_published",
            )
        }),
    )
    actions = ['mark_as_verified_and_published', 'unpublish_selected', 'archive_selected']

    def verification_badge(self, obj):
        colors = {
            'verified': '#198754',
            'pending': '#ffc107',
            'rejected': '#dc3545',
            'archived': '#6c757d',
        }
        text_color = '#000' if obj.verification_status == 'pending' else '#fff'
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            colors.get(obj.verification_status, '#6c757d'),
            text_color,
            obj.get_verification_status_display()
        )
    verification_badge.short_description = "Verification"

    @admin.action(description="Verify and Publish selected collaborations")
    def mark_as_verified_and_published(self, request, queryset):
        queryset.update(
            verification_status='verified',
            is_published=True,
            verified_by=request.user,
            verified_date=timezone.now().date()
        )

    @admin.action(description="Unpublish selected collaborations")
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Archive selected collaborations")
    def archive_selected(self, request, queryset):
        queryset.update(verification_status='archived', is_published=False)


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ('event', 'recipient', 'reminder_type', 'status', 'sent_at')
    list_filter = ('reminder_type', 'status', 'sent_at')
    search_fields = ('event__title', 'recipient__username', 'details')
    readonly_fields = ('event', 'recipient', 'reminder_type', 'status', 'sent_at', 'details')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'target_repr', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'action', 'target_repr', 'details', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'action', 'target_repr', 'details', 'ip_address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username_or_email', 'ip_address', 'failed_attempts', 'last_attempt', 'locked_until')
    search_fields = ('username_or_email', 'ip_address')
