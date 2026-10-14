"""
Comprehensive test suite for Swayamsevak Foundation application.
Covers models, phone validation, views, bilingual switching, and security permissions.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import (
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
    validate_image_file,
    validate_achievement_media,
)
from datetime import date, timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from core.forms import validate_indian_phone
from django.core.exceptions import ValidationError

User = get_user_model()


class FoundationModelTests(TestCase):
    def setUp(self):
        self.setting = FoundationSetting.get_settings()
        self.service_area = ServiceArea.objects.create(
            title="Supporting Orphanage Children",
            title_mr="अनाथालयातील बालकांना आधार व मदत",
            slug="orphanage-support",
            short_description="Providing care, nutritional food, and essentials.",
            short_description_mr="अनाथालयातील बालकांना मायेची ऊब आणि आधार देणे.",
            order=1
        )

    def test_foundation_setting_singleton(self):
        """Verify singleton get_settings works properly."""
        s2 = FoundationSetting.get_settings()
        self.assertEqual(self.setting.id, s2.id)
        self.assertEqual(self.setting.name, "Swayamsevak Foundation")
        self.assertEqual(self.setting.phone, "9852827771")
        self.assertEqual(self.setting.founder_president, "Om Vinod Dhadbale")
        self.assertEqual(self.setting.city, "Chhatrapati Sambhajinagar, Maharashtra, India")

    def test_service_area_str(self):
        self.assertEqual(str(self.service_area), "1. Supporting Orphanage Children")

    def test_activity_creation(self):
        act = Activity.objects.create(
            title="Every Sunday Food Distribution Drive",
            title_mr="दर रविवारी अन्नदान उपक्रम",
            service_area=self.service_area,
            schedule_frequency="Every Sunday",
            description="Distributing fresh food packets.",
            description_mr="अन्नवाटप करणे.",
            status="regular"
        )
        self.assertEqual(str(act), "Every Sunday Food Distribution Drive")
        self.assertEqual(act.status, "regular")


class FormValidationTests(TestCase):
    def test_valid_indian_phone(self):
        self.assertEqual(validate_indian_phone("9852827771"), "9852827771")
        self.assertEqual(validate_indian_phone("+919852827771"), "9852827771")
        self.assertEqual(validate_indian_phone("09852827771"), "9852827771")
        self.assertEqual(validate_indian_phone("985-282-7771"), "9852827771")

    def test_invalid_indian_phone(self):
        with self.assertRaises(ValidationError):
            validate_indian_phone("12345")
        with self.assertRaises(ValidationError):
            validate_indian_phone("5551234567")  # Starts with 5, not valid Indian mobile


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.setting = FoundationSetting.get_settings()
        self.staff_user = User.objects.create_user(
            username='stafftest',
            password='testpassword123',
            is_staff=True
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Swayamsevak Foundation")
        self.assertContains(response, "स्वावलंबनातून समाजसेवा")
        self.assertContains(response, "9852827771")
        self.assertContains(response, "Om Vinod Dhadbale")

    def test_about_page_status(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Our Story – Why We Started")
        self.assertContains(response, "Humanity is the greatest service")
        self.assertContains(response, "TV Center, Chhatrapati Sambhajinagar, 431001")

    def test_service_areas_page_status(self):
        response = self.client.get(reverse('service_areas'))
        self.assertEqual(response.status_code, 200)

    def test_activities_page_status(self):
        response = self.client.get(reverse('activities'))
        self.assertEqual(response.status_code, 200)

    def test_gallery_page_status(self):
        GalleryMedia.objects.create(
            title="Sunday Food Distribution Drive",
            title_mr="रविवार अन्नदान उपक्रम",
            caption="Food distribution at TV Center",
            caption_mr="टीव्ही सेंटर येथे अन्नवाटप",
            media_type="photo",
            is_published=True
        )
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sunday Food Distribution Drive")

    def test_volunteer_get_and_post(self):
        # GET
        get_res = self.client.get(reverse('volunteer'))
        self.assertEqual(get_res.status_code, 200)

        # Valid POST
        post_data = {
            'full_name': 'Santosh Kulkarni',
            'phone': '9852827771',
            'email': 'santosh@example.com',
            'city_area': 'CIDCO, Chhatrapati Sambhajinagar',
            'availability': 'every_sunday',
            'blood_group': 'O+',
            'occupation': 'Software Engineer',
            'motivation': 'I want to volunteer for the Sunday food drive.',
        }
        post_res = self.client.post(reverse('volunteer'), post_data)
        self.assertEqual(post_res.status_code, 302)  # Redirect upon success
        self.assertTrue(Volunteer.objects.filter(full_name='Santosh Kulkarni').exists())

    def test_support_inquiry_post(self):
        post_data = {
            'supporter_name': 'Meera Patil',
            'phone': '9852827771',
            'email': 'meera@example.com',
            'city': 'Chhatrapati Sambhajinagar',
            'support_type': 'sunday_food',
            'preferred_mode': 'sponsor_food',
            'message': 'Would like to sponsor Sunday food distribution drive.',
        }
        response = self.client.post(reverse('support'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SupportInquiry.objects.filter(supporter_name='Meera Patil').exists())

    def test_contact_inquiry_post(self):
        post_data = {
            'name': 'Ganesh Shinde',
            'email': 'ganesh@example.com',
            'phone': '9852827771',
            'subject': 'Cleanliness Drive Collaboration',
            'message': 'We have a youth group in TV Center interested in participating.',
        }
        response = self.client.post(reverse('contact'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactInquiry.objects.filter(name='Ganesh Shinde').exists())

    def test_bilingual_switch(self):
        response = self.client.get(reverse('switch_language', kwargs={'lang_code': 'mr'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('site_lang'), 'mr')

        home_res = self.client.get(reverse('home'))
        self.assertEqual(home_res.status_code, 200)
        self.assertContains(home_res, "lang-mr")

    def test_staff_dashboard_access_control(self):
        # Anonymous should be redirected to login
        res_anon = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(res_anon.status_code, 302)

        # Logged in staff user should have access
        self.client.force_login(self.staff_user)
        res_staff = self.client.get(reverse('staff_dashboard'))
        # Staff user redirects to appropriate dashboard
        self.assertIn(res_staff.status_code, [200, 302])


class AuthAndRoleTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Admin user
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin_test@swayamsevak.org',
            password='Password123'
        )
        self.admin_profile = UserProfile.get_profile_for_user(self.admin_user)
        self.admin_profile.role = 'admin'
        self.admin_profile.status = 'approved'
        self.admin_profile.save()

        # Coordinator user
        self.coord_user = User.objects.create_user(
            username='coord_test',
            email='coord_test@swayamsevak.org',
            password='Password123',
            first_name='Coordinator',
            last_name='Test'
        )
        self.coord_profile = UserProfile.get_profile_for_user(self.coord_user)
        self.coord_profile.role = 'coordinator'
        self.coord_profile.status = 'approved'
        self.coord_profile.save()

        # Approved Volunteer
        self.vol_user = User.objects.create_user(
            username='vol_test',
            email='vol_test@swayamsevak.org',
            password='Password123',
            first_name='Volunteer',
            last_name='Test'
        )
        self.vol_profile = UserProfile.get_profile_for_user(self.vol_user)
        self.vol_profile.role = 'volunteer'
        self.vol_profile.status = 'approved'
        self.vol_profile.save()

        # Pending Volunteer
        self.pending_user = User.objects.create_user(
            username='pending_test',
            email='pending_test@swayamsevak.org',
            password='Password123'
        )
        self.pending_profile = UserProfile.get_profile_for_user(self.pending_user)
        self.pending_profile.role = 'volunteer'
        self.pending_profile.status = 'pending'
        self.pending_profile.save()

        # Activity and Event
        self.activity = Activity.objects.create(
            title="Sunday Food Distribution Test",
            title_mr="अन्नदान चाचणी",
            schedule_frequency="Every Sunday",
            description="Test food distribution.",
            description_mr="चाचणी",
            status="regular"
        )
        self.coord_profile.assigned_activities.add(self.activity)

        self.event = Event.objects.create(
            title="Sunday Food Drive Session",
            activity=self.activity,
            coordinator=self.coord_user,
            event_date=date.today() + timedelta(days=2),
            start_time="09:00:00",
            location="TV Center, Chhatrapati Sambhajinagar",
            description="Testing event session",
            max_volunteers=15,
            status="upcoming"
        )

        # Unassigned event for IDOR tests
        self.other_event = Event.objects.create(
            title="Other Event Drive",
            activity=None,
            coordinator=None,
            event_date=date.today() + timedelta(days=3),
            start_time="10:00:00",
            location="CIDCO",
            description="Other event",
            max_volunteers=10,
            status="upcoming"
        )

    def test_volunteer_registration_success(self):
        signup_data = {
            'full_name': 'Aarav Patil',
            'email': 'aarav.patil@example.com',
            'phone': '9852827771',
            'city': 'CIDCO, Chhatrapati Sambhajinagar',
            'availability': 'every_sunday',
            'blood_group': 'B+',
            'occupation': 'Student',
            'interests': 'Youth community service',
            'password': 'SecurePassword123',
            'password_confirm': 'SecurePassword123',
            'privacy_consent': True,
        }
        res = self.client.post(reverse('register'), signup_data)
        self.assertEqual(res.status_code, 302)
        new_user = User.objects.filter(email='aarav.patil@example.com').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.profile.role, 'volunteer')
        self.assertEqual(new_user.profile.status, 'pending')

    def test_volunteer_registration_duplicate_email(self):
        signup_data = {
            'full_name': 'Duplicate User',
            'email': 'vol_test@swayamsevak.org',  # already exists
            'phone': '9852827771',
            'city': 'Chhatrapati Sambhajinagar',
            'availability': 'every_sunday',
            'password': 'SecurePassword123',
            'password_confirm': 'SecurePassword123',
            'privacy_consent': True,
        }
        res = self.client.post(reverse('register'), signup_data)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "An account with this email address already exists")

    def test_volunteer_registration_password_mismatch(self):
        signup_data = {
            'full_name': 'Mismatch Test',
            'email': 'mismatch@example.com',
            'phone': '9852827771',
            'city': 'Chhatrapati Sambhajinagar',
            'availability': 'every_sunday',
            'password': 'Password123',
            'password_confirm': 'DifferentPassword123',
            'privacy_consent': True,
        }
        res = self.client.post(reverse('register'), signup_data)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Passwords do not match")

    def test_login_with_username_and_email(self):
        # 1. Login with username
        res_user = self.client.post(reverse('login'), {
            'username_or_email': 'vol_test',
            'password': 'Password123',
        })
        self.assertEqual(res_user.status_code, 302)
        self.assertRedirects(res_user, reverse('volunteer_dashboard'))
        self.client.logout()

        # 2. Login with email
        res_email = self.client.post(reverse('login'), {
            'username_or_email': 'vol_test@swayamsevak.org',
            'password': 'Password123',
        })
        self.assertEqual(res_email.status_code, 302)
        self.assertRedirects(res_email, reverse('volunteer_dashboard'))

    def test_role_based_login_redirects(self):
        # Admin redirect
        res_admin = self.client.post(reverse('login'), {
            'username_or_email': 'admin_test',
            'password': 'Password123',
        })
        self.assertRedirects(res_admin, reverse('admin_dashboard'))
        self.client.logout()

        # Coordinator redirect
        res_coord = self.client.post(reverse('login'), {
            'username_or_email': 'coord_test',
            'password': 'Password123',
        })
        self.assertRedirects(res_coord, reverse('coordinator_dashboard'))
        self.client.logout()

        # Volunteer redirect
        res_vol = self.client.post(reverse('login'), {
            'username_or_email': 'vol_test',
            'password': 'Password123',
        })
        self.assertRedirects(res_vol, reverse('volunteer_dashboard'))

    def test_brute_force_throttling(self):
        # 5 consecutive failed logins trigger lockout
        for _ in range(5):
            self.client.post(reverse('login'), {
                'username_or_email': 'brute_force_target@example.com',
                'password': 'WrongPassword!',
            })

        attempt = LoginAttempt.objects.filter(username_or_email='brute_force_target@example.com').first()
        self.assertIsNotNone(attempt)
        self.assertGreaterEqual(attempt.failed_attempts, 5)
        self.assertIsNotNone(attempt.locked_until)

    def test_dashboard_access_control_server_side_403(self):
        # 1. Volunteer attempts to access Admin dashboard -> 403 Forbidden
        self.client.force_login(self.vol_user)
        res_admin = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_admin.status_code, 403)

        # 2. Volunteer attempts to access Coordinator dashboard -> 403 Forbidden
        res_coord = self.client.get(reverse('coordinator_dashboard'))
        self.assertEqual(res_coord.status_code, 403)

        # 3. Volunteer can access Volunteer dashboard -> 200 OK
        res_vol = self.client.get(reverse('volunteer_dashboard'))
        self.assertEqual(res_vol.status_code, 200)

        # 4. Anonymous user redirected to login
        self.client.logout()
        res_anon = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(res_anon.status_code, 302)
        self.assertIn('/login/', res_anon.url)

    def test_volunteer_approval_workflow(self):
        self.client.force_login(self.admin_user)
        self.assertEqual(self.pending_profile.status, 'pending')

        # Admin approves pending volunteer
        res_approve = self.client.get(
            reverse('admin_update_volunteer_status', kwargs={'profile_id': self.pending_profile.id, 'new_status': 'approved'})
        )
        self.assertEqual(res_approve.status_code, 302)
        self.pending_profile.refresh_from_db()
        self.assertEqual(self.pending_profile.status, 'approved')

        # Admin suspends volunteer
        res_suspend = self.client.get(
            reverse('admin_update_volunteer_status', kwargs={'profile_id': self.pending_profile.id, 'new_status': 'suspended'})
        )
        self.assertEqual(res_suspend.status_code, 302)
        self.pending_profile.refresh_from_db()
        self.assertEqual(self.pending_profile.status, 'suspended')

    def test_event_registration_approved_vs_pending(self):
        # 1. Pending volunteer cannot register
        self.client.force_login(self.pending_user)
        res_pending = self.client.get(reverse('event_register', kwargs={'event_id': self.event.id}))
        self.assertFalse(EventRegistration.objects.filter(event=self.event, volunteer=self.pending_user).exists())

        # 2. Approved volunteer can register
        self.client.force_login(self.vol_user)
        res_approved = self.client.get(reverse('event_register', kwargs={'event_id': self.event.id}))
        self.assertTrue(EventRegistration.objects.filter(event=self.event, volunteer=self.vol_user).exists())

    def test_idor_protection_on_cancel_registration(self):
        reg = EventRegistration.objects.create(event=self.event, volunteer=self.vol_user, status='registered')

        # Other user cannot cancel vol_user's registration
        self.client.force_login(self.pending_user)
        res = self.client.get(reverse('event_cancel', kwargs={'event_id': self.event.id}))
        self.assertEqual(res.status_code, 404)
        reg.refresh_from_db()
        self.assertEqual(reg.status, 'registered')

    def test_coordinator_attendance_marking_and_idor(self):
        reg = EventRegistration.objects.create(event=self.event, volunteer=self.vol_user, status='registered')

        # Assigned coordinator can record attendance
        self.client.force_login(self.coord_user)
        res_own = self.client.post(
            reverse('coordinator_attendance', kwargs={'event_id': self.event.id}),
            {'attended_volunteers': [str(self.vol_user.id)]}
        )
        self.assertEqual(res_own.status_code, 302)
        reg.refresh_from_db()
        self.assertEqual(reg.status, 'attended')

        # Coordinator CANNOT access attendance for unassigned event
        res_other = self.client.get(
            reverse('coordinator_attendance', kwargs={'event_id': self.other_event.id})
        )
        self.assertEqual(res_other.status_code, 403)

    def test_coordinator_report_submission_and_admin_review(self):
        self.client.force_login(self.coord_user)

        # Submit report
        res_submit = self.client.post(
            reverse('coordinator_submit_report', kwargs={'event_id': self.event.id}),
            {
                'title': 'Test Drive Report',
                'summary': 'All food packets distributed successfully at TV Center.',
                'volunteers_present_count': 12,
                'beneficiaries_served_count': 150,
                'challenges_notes': 'None',
            }
        )
        self.assertEqual(res_submit.status_code, 302)
        report = ActivityReport.objects.filter(event=self.event, coordinator=self.coord_user).first()
        self.assertIsNotNone(report)
        self.assertEqual(report.status, 'pending')

        # Admin reviews and approves report
        self.client.force_login(self.admin_user)
        res_review = self.client.post(
            reverse('admin_review_report', kwargs={'report_id': report.id}),
            {
                'review_action': 'approved',
                'admin_feedback': 'Well conducted!',
            }
        )
        self.assertEqual(res_review.status_code, 302)
        report.refresh_from_db()
        self.assertEqual(report.status, 'approved')

    def test_password_reset_flow(self):
        # 1. Generate token
        token = default_token_generator.make_token(self.vol_user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.vol_user.pk))

        # 2. Confirm reset
        confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        res_confirm = self.client.post(confirm_url, {
            'new_password': 'BrandNewPassword123',
            'confirm_password': 'BrandNewPassword123',
        })
        self.assertEqual(res_confirm.status_code, 302)

        # 3. Verify login works with new password
        res_new_login = self.client.post(reverse('login'), {
            'username_or_email': 'vol_test',
            'password': 'BrandNewPassword123',
        })
        self.assertEqual(res_new_login.status_code, 302)

    def test_profile_update_and_privilege_escalation_protection(self):
        self.client.force_login(self.vol_user)

        # Update profile details
        res_update = self.client.post(reverse('profile'), {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName',
            'email': 'updated.email@swayamsevak.org',
            'phone': '9852827771',
            'city': 'CIDCO',
            'blood_group': 'A+',
            'availability': 'every_sunday',
            'occupation': 'Teacher',
            'interests': 'Teaching orphans',
            # Attacking user attempts to inject role='admin'
            'role': 'admin',
            'status': 'approved',
        })
        self.assertEqual(res_update.status_code, 302)
        self.vol_user.refresh_from_db()
        self.assertEqual(self.vol_user.first_name, 'UpdatedFirstName')
        # Role must still be volunteer (privilege escalation blocked!)
        self.assertEqual(self.vol_user.profile.role, 'volunteer')

    def test_logout(self):
        self.client.force_login(self.vol_user)
        res_logout = self.client.get(reverse('logout'))
        self.assertEqual(res_logout.status_code, 302)
        self.assertRedirects(res_logout, reverse('login'))


class PublicPagesAndModelsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.setting = FoundationSetting.get_settings()
        self.category = ActivityCategory.objects.create(
            name="Food Donation",
            name_mr="अन्नदान",
            slug="food-donation",
            icon_bootstrap="bi-basket2-fill",
            order=1,
            is_active=True
        )
        self.activity = Activity.objects.create(
            title="Every Sunday Food Distribution",
            title_mr="दर रविवारी अन्नदान उपक्रम",
            slug="every-sunday-food-distribution",
            category=self.category,
            schedule_frequency="Every Sunday",
            description="Distributing hot, freshly prepared meals to underprivileged families.",
            description_mr="गरजू नागरिकांना ताजे आणि पौष्टिक भोजन वाटप.",
            is_published=True,
            is_active=True,
            venue="TV Center & City Orphanages"
        )

    def test_activity_category_model(self):
        self.assertEqual(str(self.category), "1. Food Donation (अन्नदान)")
        self.assertEqual(self.category.slug, "food-donation")
        self.assertEqual(self.category.icon, "bi-basket2-fill")

    def test_activity_detail_view(self):
        res = self.client.get(reverse('activity_detail', kwargs={'slug': self.activity.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Every Sunday Food Distribution")
        self.assertContains(res, "Food Donation")
        self.assertContains(res, "TV Center")

    def test_events_page_and_can_register(self):
        ev = Event.objects.create(
            title="Blood Donation Camp 2026",
            title_mr="रक्तदान शिबीर २०२६",
            activity=self.activity,
            event_date=date.today() + timedelta(days=7),
            start_time="09:00:00",
            location="TV Center Community Hall",
            venue="TV Center Community Hall",
            is_published=True,
            registration_enabled=True,
            status="upcoming",
            max_volunteers=10
        )
        self.assertTrue(ev.can_register)

        res = self.client.get(reverse('events'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Blood Donation Camp 2026")
        self.assertContains(res, "Registration Open")

        # Test registration closed when deadline passed or closed flag set
        ev.is_closed = True
        ev.save()
        self.assertFalse(ev.can_register)

    def test_announcements_and_stories_view(self):
        ann = Announcement.objects.create(
            title="Official Sunday Drive Notice",
            title_mr="अधिकृत रविवार उपक्रम सूचना",
            content="Volunteers gather at 9 AM.",
            content_mr="सर्व स्वयंसेवकांनी सकाळी ९ वाजता उपस्थित राहावे.",
            announcement_type="announcement",
            target_role="all",
            is_published=True,
            is_active=True
        )
        story = Announcement.objects.create(
            title="Winter Warmth Impact Story",
            title_mr="हिवाळी ऊब समाजकथा",
            content="Over 200 blankets distributed to street sleepers.",
            content_mr="रस्त्यावर झोपणाऱ्या २०० पेक्षा जास्त नागरिकांना ब्लँकेट्स वाटप.",
            announcement_type="story",
            target_role="all",
            is_published=True,
            is_active=True
        )

        res = self.client.get(reverse('announcements'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Official Sunday Drive Notice")
        self.assertContains(res, "Winter Warmth Impact Story")

        # Filter by announcement
        res_ann = self.client.get(reverse('announcements') + '?type=announcement')
        self.assertEqual(res_ann.status_code, 200)
        self.assertContains(res_ann, "Official Sunday Drive Notice")

        # Filter by story
        res_story = self.client.get(reverse('announcements') + '?type=story')
        self.assertEqual(res_story.status_code, 200)
        self.assertContains(res_story, "Winter Warmth Impact Story")

    def test_donate_page(self):
        res = self.client.get(reverse('donate'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Support Pledge / Inquiry Form")
        self.assertContains(res, "Om Vinod Dhadbale")

    def test_privacy_policy_page(self):
        res = self.client.get(reverse('privacy_policy'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Swayamsevak Foundation")
        self.assertContains(res, "Om Vinod Dhadbale")
        self.assertContains(res, "TV Center, Chhatrapati Sambhajinagar, 431001")
        self.assertContains(res, "9852827771")

    def test_custom_404_page(self):
        res = self.client.get('/definitely-nonexistent-page-url-xyz/')
        self.assertEqual(res.status_code, 404)
        self.assertContains(res, "Page Not Found", status_code=404)
        self.assertContains(res, "404", status_code=404)


class ImpactAndAchievementsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.setting = FoundationSetting.get_settings()
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@swayamsevak.org',
            password='AdminPassword123!'
        )

    def test_impact_statistic_model_and_properties(self):
        stat1 = ImpactStatistic.objects.create(
            metric_key='meals_distributed',
            title='Total Meals Distributed',
            title_mr='एकूण अन्नवाटप',
            numeric_value=12500,
            unit_label='Meals',
            unit_label_mr='जेवण',
            verification_status='verified',
            is_published=True,
            internal_verification_notes='Sunday distribution logs verified.'
        )
        self.assertEqual(stat1.display_value, '12,500+')
        self.assertTrue(stat1.is_verified_and_approved)
        self.assertIn('Total Meals Distributed', str(stat1))

        # Dynamic Years of Service calculation
        years = ImpactStatistic.get_calculated_years_of_service()
        expected_years = max(1, date.today().year - 2024)
        self.assertEqual(years, expected_years)

        # Pending metric is not verified & approved
        stat_pending = ImpactStatistic.objects.create(
            metric_key='trees_planted',
            title='Trees Planted',
            numeric_value=450,
            verification_status='pending',
            is_published=False
        )
        self.assertFalse(stat_pending.is_verified_and_approved)

    def test_achievement_model_and_properties(self):
        ach = Achievement.objects.create(
            title='Excellence in Grassroots Social Service',
            title_mr='उत्कृष्ट सामाजिक सेवा सन्मान',
            awarding_organization='Maharashtra Social Council',
            awarding_organization_mr='महाराष्ट्र सामाजिक परिषद',
            date_received=date(2024, 8, 15),
            description='Awarded for consistent weekly food drives.',
            description_mr='साप्ताहिक अन्नदान उपक्रमासाठी सन्मानित.',
            verification_status='verified',
            is_published=True,
            internal_verification_notes='Certificate audited by executive committee.'
        )
        self.assertEqual(str(ach), 'Excellence in Grassroots Social Service (Maharashtra Social Council)')
        self.assertTrue(ach.is_verified_and_approved)

        # Pending achievement
        ach_pending = Achievement.objects.create(
            title='Pending Award',
            awarding_organization='Community Forum',
            date_received=date(2025, 1, 1),
            verification_status='pending',
            is_published=False
        )
        self.assertFalse(ach_pending.is_verified_and_approved)

    def test_collaboration_model_and_properties(self):
        collab = Collaboration.objects.create(
            organization_name='Chhatrapati Sambhajinagar Blood Bank',
            organization_name_mr='छत्रपती संभाजीनगर रक्तपेढी',
            collaboration_purpose='Emergency Blood Donation Network',
            collaboration_purpose_mr='तातडीचे रक्तदान साहाय्य नेटवर्क',
            activities_conducted='Joint quarterly blood donation drives at TV Center.',
            activities_conducted_mr='टीव्ही सेंटर येथे संयुक्त रक्तदान शिबीर.',
            collaboration_period='2024 - Present',
            verification_status='verified',
            is_published=True,
            internal_verification_notes='MOU signed on 15 Feb 2024.'
        )
        self.assertEqual(str(collab), 'Chhatrapati Sambhajinagar Blood Bank (2024 - Present)')
        self.assertTrue(collab.is_verified_and_approved)

        # Pending collaboration
        collab_pending = Collaboration.objects.create(
            organization_name='Unverified Partner',
            collaboration_purpose='Prospective project',
            verification_status='pending',
            is_published=False
        )
        self.assertFalse(collab_pending.is_verified_and_approved)

    def test_file_validators(self):
        # Valid image
        valid_img = SimpleUploadedFile("badge.jpg", b"fake image content", content_type="image/jpeg")
        validate_image_file(valid_img)

        # Invalid image extension
        bad_img = SimpleUploadedFile("malicious.exe", b"fake binary", content_type="application/octet-stream")
        with self.assertRaises(ValidationError):
            validate_image_file(bad_img)

        # Oversized image (> 5MB)
        oversized_img = SimpleUploadedFile("huge.jpg", b"x" * (5 * 1024 * 1024 + 1), content_type="image/jpeg")
        with self.assertRaises(ValidationError):
            validate_image_file(oversized_img)

        # Valid achievement media (PDF)
        valid_pdf = SimpleUploadedFile("cert.pdf", b"%PDF-1.4...", content_type="application/pdf")
        validate_achievement_media(valid_pdf)

        # Invalid achievement extension (.zip)
        bad_cert = SimpleUploadedFile("cert.zip", b"zip archive", content_type="application/zip")
        with self.assertRaises(ValidationError):
            validate_achievement_media(bad_cert)

    def test_zero_fabrication_unverified_records_hidden(self):
        verified_stat = ImpactStatistic.objects.create(
            metric_key='meals_distributed',
            title='Verified Meals Distributed',
            numeric_value=8500,
            verification_status='verified',
            is_published=True
        )
        pending_stat = ImpactStatistic.objects.create(
            metric_key='clothes_distributed',
            title='Unverified Clothes Count',
            numeric_value=300,
            verification_status='pending',
            is_published=True
        )
        rejected_stat = ImpactStatistic.objects.create(
            metric_key='trees_planted',
            title='Rejected Tree Count',
            numeric_value=999,
            verification_status='rejected',
            is_published=False
        )

        verified_ach = Achievement.objects.create(
            title='Verified State Level Honor',
            awarding_organization='State Board',
            date_received=date(2024, 11, 1),
            verification_status='verified',
            is_published=True
        )
        pending_ach = Achievement.objects.create(
            title='Unverified Draft Award',
            awarding_organization='Unknown Group',
            date_received=date(2024, 11, 1),
            verification_status='pending',
            is_published=True
        )

        verified_collab = Collaboration.objects.create(
            organization_name='Verified Hospital Partner',
            collaboration_purpose='Assisting needy patients',
            verification_status='verified',
            is_published=True
        )
        pending_collab = Collaboration.objects.create(
            organization_name='Unverified NGO Partner',
            collaboration_purpose='Discussion stage',
            verification_status='pending',
            is_published=False
        )

        # Check dedicated Impact page (/impact/)
        res_impact = self.client.get(reverse('impact'))
        self.assertEqual(res_impact.status_code, 200)
        self.assertContains(res_impact, 'Verified Meals Distributed')
        self.assertNotContains(res_impact, 'Unverified Clothes Count')
        self.assertNotContains(res_impact, 'Rejected Tree Count')
        self.assertContains(res_impact, 'Verified State Level Honor')
        self.assertNotContains(res_impact, 'Unverified Draft Award')
        self.assertContains(res_impact, 'Verified Hospital Partner')
        self.assertNotContains(res_impact, 'Unverified NGO Partner')

        # Check Homepage (/)
        res_home = self.client.get(reverse('home'))
        self.assertEqual(res_home.status_code, 200)
        self.assertContains(res_home, 'Verified Meals Distributed')
        self.assertNotContains(res_home, 'Unverified Clothes Count')
        self.assertNotContains(res_home, 'Rejected Tree Count')
        self.assertContains(res_home, 'Verified State Level Honor')
        self.assertNotContains(res_home, 'Unverified Draft Award')
        self.assertContains(res_home, 'Verified Hospital Partner')
        self.assertNotContains(res_home, 'Unverified NGO Partner')

    def test_missing_metrics_hidden_and_clean_empty_state(self):
        ImpactStatistic.objects.all().delete()
        Achievement.objects.all().delete()
        Collaboration.objects.all().delete()

        res = self.client.get(reverse('impact'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Official Impact Metrics Under Audit')
        self.assertContains(res, 'Recognitions & Awards Archive')
        self.assertContains(res, 'Institutional Collaborations In Formal Documentation')

        res_home = self.client.get(reverse('home'))
        self.assertEqual(res_home.status_code, 200)
        self.assertContains(res_home, 'Impact Records Under Official Compilation')

    def test_internal_verification_notes_never_exposed(self):
        secret_stat_note = "CONFIDENTIAL_AUDIT_REGISTER_ENTRY_STAT_9876"
        secret_ach_note = "CONFIDENTIAL_CERTIFICATE_FILE_LOCATION_ACH_5432"
        secret_collab_note = "CONFIDENTIAL_INTERNAL_MOU_STAMP_COLLAB_1234"

        ImpactStatistic.objects.create(
            metric_key='meals_distributed',
            title='Verified Meal Service',
            numeric_value=5000,
            verification_status='verified',
            is_published=True,
            internal_verification_notes=secret_stat_note
        )
        Achievement.objects.create(
            title='Verified Merit Citation',
            awarding_organization='Civic Body',
            date_received=date(2024, 10, 1),
            verification_status='verified',
            is_published=True,
            internal_verification_notes=secret_ach_note
        )
        Collaboration.objects.create(
            organization_name='Verified Clinic',
            collaboration_purpose='Health checks',
            verification_status='verified',
            is_published=True,
            internal_verification_notes=secret_collab_note
        )

        res_impact = self.client.get(reverse('impact'))
        self.assertNotContains(res_impact, secret_stat_note)
        self.assertNotContains(res_impact, secret_ach_note)
        self.assertNotContains(res_impact, secret_collab_note)

        res_home = self.client.get(reverse('home'))
        self.assertNotContains(res_home, secret_stat_note)
        self.assertNotContains(res_home, secret_ach_note)
        self.assertNotContains(res_home, secret_collab_note)

    def test_bilingual_impact_rendering(self):
        ImpactStatistic.objects.create(
            metric_key='meals_distributed',
            title='Food Relief Service',
            title_mr='अन्नदान सेवा कार्य',
            description='Serving hot meals every Sunday.',
            description_mr='दर रविवारी गरजू नागरिकांना ताजे जेवण वाटप.',
            numeric_value=1000,
            verification_status='verified',
            is_published=True
        )

        # English
        res_en = self.client.get(reverse('impact') + '?lang=en')
        self.assertEqual(res_en.status_code, 200)
        self.assertContains(res_en, 'Food Relief Service')
        self.assertContains(res_en, 'Serving hot meals every Sunday.')

        # Marathi
        res_mr = self.client.get(reverse('impact') + '?lang=mr')
        self.assertEqual(res_mr.status_code, 200)
        self.assertContains(res_mr, 'अन्नदान सेवा कार्य')
        self.assertContains(res_mr, 'दर रविवारी गरजू नागरिकांना ताजे जेवण वाटप.')

    def test_achievements_url_alias(self):
        res = self.client.get(reverse('achievements'))
        self.assertEqual(res.status_code, 200)

    def test_navigation_links_present(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, reverse('impact'))



