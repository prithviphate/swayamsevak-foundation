"""
Notification utilities for Swayamsevak Foundation.
Handles email dispatch, event reminders, duplicate prevention, and failsafe logging.
"""

import logging
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import ReminderLog, AuditLog, FoundationSetting

logger = logging.getLogger(__name__)


def is_email_configured():
    """
    Check if email credentials or a viable local backend are available.
    """
    backend = getattr(settings, 'EMAIL_BACKEND', '')
    if 'console' in backend or 'locmem' in backend or 'filebased' in backend:
        return True
    host_user = getattr(settings, 'EMAIL_HOST_USER', '')
    host_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    return bool(host_user and host_password)


def safe_send_mail(subject, message, recipient_list, from_email=None, fail_silently=False):
    """
    Dispatches email using Django send_mail with exception handling.
    Returns (success: bool, status_message: str).
    """
    if not recipient_list:
        return False, "No recipient provided."

    sender = from_email or getattr(
        settings,
        'DEFAULT_FROM_EMAIL',
        'Swayamsevak Foundation <swayamsevakfoundation24@gmail.com>'
    )

    if not is_email_configured():
        msg = "Email delivery is not configured on this server (credentials missing). Message logged locally."
        logger.info(f"[Email Not Sent - Unconfigured] Subject: {subject} | To: {recipient_list}")
        return False, msg

    try:
        count = send_mail(
            subject=subject,
            message=message,
            from_email=sender,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
        )
        return bool(count > 0), "Email delivered successfully."
    except Exception as exc:
        err_msg = f"Email delivery failed: {str(exc)}"
        logger.error(err_msg)
        return False, err_msg


def notify_volunteer_registration(user, profile):
    """
    Sends welcome and pending approval notification to newly registered volunteer.
    """
    setting = FoundationSetting.get_settings()
    subject = f"Welcome to {setting.name} – Volunteer Registration Received"
    body = (
        f"Namaste {user.get_full_name() or user.username},\n\n"
        f"Thank you for registering as a volunteer with {setting.name}!\n\n"
        f"Your registration status is currently: PENDING REVIEW.\n"
        f"Our team reviews all volunteer profiles to ensure a safe, collaborative community. "
        f"Once an administrator approves your profile, your account will be activated for full event participation.\n\n"
        f"In the meantime, you can log in to your Volunteer Dashboard to view foundation activities, "
        f"upcoming Sunday food distribution schedules, and announcements.\n\n"
        f"Foundation Contact: {setting.phone}\n"
        f"Email: {setting.email}\n"
        f"Address: {setting.address}\n\n"
        f"With warm regards,\n"
        f"{setting.founder_president}\n"
        f"President, {setting.name}\n"
        f"Tagline: {setting.tagline_mr} ({setting.tagline_en})"
    )
    success, note = safe_send_mail(subject, body, [user.email])
    AuditLog.log(
        user=user,
        action='email_notification',
        target_repr=f"Volunteer Welcome: {user.username}",
        details=f"Status: {'Success' if success else 'Skipped/Failed'} - {note}"
    )
    return success, note


def notify_volunteer_status_change(profile, admin_user=None):
    """
    Notifies volunteer when an administrator approves, suspends, or updates their profile.
    """
    user = profile.user
    if not user.email:
        return False, "User has no email address."

    setting = FoundationSetting.get_settings()
    status_display = profile.get_status_display()
    subject = f"Your Volunteer Account Status Update – {setting.name}"
    
    if profile.status == 'approved':
        body = (
            f"Namaste {user.get_full_name() or user.username},\n\n"
            f"Great news! Your volunteer profile with {setting.name} has been APPROVED.\n\n"
            f"You can now participate in upcoming Sunday food distribution drives, "
            f"health camps, tree plantations, and register for active events.\n\n"
            f"Log in to your Volunteer Dashboard: https://swayamsevak-foundation-lp3k-beta.vercel.app/login/\n\n"
            f"Thank you for joining our movement: '{setting.tagline_mr}'.\n\n"
            f"With warm regards,\n"
            f"{setting.name} Coordination Team\n"
            f"Contact: {setting.phone}"
        )
    else:
        body = (
            f"Namaste {user.get_full_name() or user.username},\n\n"
            f"Your volunteer account status with {setting.name} has been updated to: {status_display}.\n\n"
            f"If you have any questions or require clarification, please contact our team at {setting.email} "
            f"or phone {setting.phone}.\n\n"
            f"Regards,\n{setting.name}"
        )

    success, note = safe_send_mail(subject, body, [user.email])
    AuditLog.log(
        user=admin_user or user,
        action='email_notification',
        target_repr=f"Status update to {profile.status} for {user.username}",
        details=f"{'Success' if success else 'Skipped/Failed'} - {note}"
    )
    return success, note


def notify_event_registration(registration):
    """
    Confirms an event registration to the volunteer.
    """
    user = getattr(registration, 'volunteer', None) or getattr(registration, 'user', None)
    event = registration.event
    setting = FoundationSetting.get_settings()

    if not user or not user.email:
        return False, "User has no email."

    subject = f"Event Registration Confirmed: {event.title} – {setting.name}"
    body = (
        f"Namaste {user.get_full_name() or user.username},\n\n"
        f"Your registration for the following foundation event has been confirmed:\n\n"
        f"Event: {event.title}\n"
        f"Date: {event.event_date.strftime('%A, %d %B %Y')}\n"
        f"Time: {event.start_time.strftime('%I:%M %p') if event.start_time else 'Morning 10:00 AM'}\n"
        f"Location: {event.location}\n\n"
        f"Reporting notes:\n"
        f"- Please arrive 15 minutes before the scheduled time.\n"
        f"- Wear comfortable clothing.\n"
        f"- Contact phone for event coordination: {setting.phone}\n\n"
        f"Thank you for serving society with us!\n"
        f"{setting.name}"
    )

    success, note = safe_send_mail(subject, body, [user.email])
    return success, note


def send_event_reminder(event, user, force=False):
    """
    Dispatches an event reminder to a registered volunteer.
    Guarantees duplicate prevention: checks ReminderLog before sending.
    """
    if not user.email:
        return False, "User has no email."

    # Prevent duplicate email reminders for the same event
    existing = ReminderLog.objects.filter(
        event=event,
        recipient=user,
        reminder_type='email',
        status='sent'
    ).first()

    if existing and not force:
        msg = f"Reminder already sent on {existing.sent_at.strftime('%Y-%m-%d %H:%M')}. Skipping duplicate."
        return False, msg

    setting = FoundationSetting.get_settings()
    subject = f"Reminder: Upcoming Event Tomorrow – {event.title}"
    body = (
        f"Namaste {user.get_full_name() or user.username},\n\n"
        f"This is a gentle reminder regarding your participation in tomorrow's event:\n\n"
        f"Event: {event.title}\n"
        f"Date: {event.event_date.strftime('%A, %d %B %Y')}\n"
        f"Time: {event.start_time.strftime('%I:%M %p') if event.start_time else '10:00 AM'}\n"
        f"Location: {event.location}\n\n"
        f"If you are unable to attend due to an emergency, please notify our team in advance at {setting.phone}.\n\n"
        f"Together for society,\n{setting.name}"
    )

    success, note = safe_send_mail(subject, body, [user.email])

    # Record reminder log
    ReminderLog.objects.create(
        event=event,
        recipient=user,
        reminder_type='email',
        status='sent' if success else 'failed',
        details=note
    )

    return success, note


def notify_contact_inquiry(inquiry):
    """
    Sends receipt acknowledgment to person contacting foundation and notifies admin email.
    """
    setting = FoundationSetting.get_settings()
    subject = f"Thank you for contacting {setting.name}"
    body = (
        f"Namaste {inquiry.name},\n\n"
        f"We have received your enquiry regarding '{inquiry.subject}'.\n"
        f"Our team will get in touch with you shortly at {inquiry.phone} or via this email.\n\n"
        f"For urgent assistance, you may reach us directly at {setting.phone}.\n\n"
        f"Warm regards,\n"
        f"{setting.name}\n"
        f"{setting.address}"
    )
    safe_send_mail(subject, body, [inquiry.email])

    # Notify admin
    admin_subject = f"New Public Enquiry: {inquiry.subject} from {inquiry.name}"
    admin_body = (
        f"New contact inquiry received:\n\n"
        f"Name: {inquiry.name}\n"
        f"Email: {inquiry.email}\n"
        f"Phone: {inquiry.phone}\n"
        f"Subject: {inquiry.subject}\n"
        f"Message:\n{inquiry.message}\n"
    )
    safe_send_mail(admin_subject, admin_body, [setting.email])
    return True, "Enquiry notification processed."


def notify_csr_enquiry(csr):
    """
    Sends formal acknowledgement to corporate partner and alerts foundation leadership.
    """
    setting = FoundationSetting.get_settings()
    subject = f"CSR Collaboration Proposal Received – {setting.name}"
    body = (
        f"Dear {csr.contact_person} ({csr.designation}),\n\n"
        f"Thank you for expressing interest in partnering with {setting.name} under Corporate Social Responsibility.\n\n"
        f"Proposal Summary:\n"
        f"- Organization: {csr.company_name}\n"
        f"- Target Category: {csr.get_project_category_display()}\n"
        f"- Collaboration Type: {csr.get_proposed_collaboration_display()}\n"
        f"- Budget Range: {csr.get_budget_range_display()}\n\n"
        f"Our foundation leadership and project coordinators will review your proposal and contact you "
        f"at {csr.phone} or {csr.email} within 2–3 business days.\n\n"
        f"Direct Contact for CSR Affairs: {setting.phone} | {setting.email}\n"
        f"Address: {setting.address}\n\n"
        f"Warm regards,\n"
        f"{setting.founder_president}\n"
        f"President, {setting.name}"
    )
    safe_send_mail(subject, body, [csr.email])

    # Leadership alert
    admin_subject = f"New CSR Proposal from {csr.company_name} ({csr.get_project_category_display()})"
    admin_body = (
        f"A new CSR enquiry has been submitted:\n\n"
        f"Company: {csr.company_name}\n"
        f"Contact Person: {csr.contact_person} ({csr.designation})\n"
        f"Email: {csr.email}\n"
        f"Phone: {csr.phone}\n"
        f"Category: {csr.get_project_category_display()}\n"
        f"Collaboration: {csr.get_proposed_collaboration_display()}\n"
        f"Budget Range: {csr.get_budget_range_display()}\n\n"
        f"Message:\n{csr.message}\n"
    )
    safe_send_mail(admin_subject, admin_body, [setting.email])
    return True, "CSR notifications processed."
