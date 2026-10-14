"""
Forms for Swayamsevak Foundation.
Validation, Bootstrap widgets, and accessibility attributes.
"""

import re
from django import forms
from .models import Volunteer, SupportInquiry, ContactInquiry, ServiceArea


def validate_indian_phone(value):
    """
    Validate standard 10-digit Indian mobile number.
    Allows optional +91 or 0 prefix.
    """
    clean_val = re.sub(r'[\s\-\(\)]', '', str(value))
    if clean_val.startswith('+91'):
        clean_val = clean_val[3:]
    elif clean_val.startswith('91') and len(clean_val) == 12:
        clean_val = clean_val[2:]
    elif clean_val.startswith('0') and len(clean_val) == 11:
        clean_val = clean_val[1:]

    if not re.match(r'^[6-9]\d{9}$', clean_val):
        raise forms.ValidationError("Please enter a valid 10-digit Indian contact number (e.g., 9852827771).")
    return clean_val


class VolunteerForm(forms.ModelForm):
    """
    Form for community members wishing to become a volunteer.
    """
    class Meta:
        model = Volunteer
        fields = [
            'full_name',
            'phone',
            'email',
            'city_area',
            'preferred_service_area',
            'availability',
            'blood_group',
            'occupation',
            'motivation',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name (e.g. Rahul Sharma)',
                'required': True,
                'autocomplete': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit Mobile Number (e.g. 9852827771)',
                'required': True,
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address',
                'required': True,
                'autocomplete': 'email',
            }),
            'city_area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Locality / Area (e.g. TV Center, CIDCO, Aurangpura)',
                'required': True,
            }),
            'preferred_service_area': forms.Select(attrs={
                'class': 'form-select',
            }),
            'availability': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-select',
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Student / Teacher / Engineer / Healthcare / Other',
            }),
            'motivation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us why you would like to volunteer with Swayamsevak Foundation...',
                'required': True,
            }),
        }

    def clean_phone(self):
        raw_phone = self.cleaned_data.get('phone')
        return validate_indian_phone(raw_phone)


class SupportInquiryForm(forms.ModelForm):
    """
    Form for well-wishers and donors who want to support foundation work.
    """
    class Meta:
        model = SupportInquiry
        fields = [
            'supporter_name',
            'phone',
            'email',
            'city',
            'support_type',
            'preferred_mode',
            'message',
        ]
        widgets = {
            'supporter_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name or Organization',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number (e.g. 9852827771)',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address (optional)',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City (e.g. Chhatrapati Sambhajinagar)',
                'required': True,
            }),
            'support_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'preferred_mode': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share how you wish to support (e.g., number of meals for Sunday drive, blankets for winter, books for children)...',
                'required': True,
            }),
        }

    def clean_phone(self):
        raw_phone = self.cleaned_data.get('phone')
        return validate_indian_phone(raw_phone)


class ContactInquiryForm(forms.ModelForm):
    """
    Public contact message form.
    """
    class Meta:
        model = ContactInquiry
        fields = [
            'name',
            'email',
            'phone',
            'subject',
            'message',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Number',
                'required': True,
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject / Purpose of Contact',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your message or inquiry...',
                'required': True,
            }),
        }

    def clean_phone(self):
        raw_phone = self.cleaned_data.get('phone')
        return validate_indian_phone(raw_phone)


# ============================================================================
# Role-based Authentication & Dashboard Forms
# ============================================================================

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import (
    UserProfile,
    Event,
    EventRegistration,
    ActivityReport,
    Announcement,
    Activity,
)


class EmailOrUsernameAuthenticationForm(forms.Form):
    """
    Role-aware authentication form accepting either email address or username.
    """
    username_or_email = forms.CharField(
        label="Username or Registered Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email or username',
            'autocomplete': 'username',
            'required': True,
            'id': 'id_username_or_email'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
            'required': True,
            'id': 'id_login_password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('username_or_email', '').strip()
        password = cleaned_data.get('password')

        if identifier and password:
            # Check if identifier is email or username
            user = None
            if '@' in identifier:
                user_obj = User.objects.filter(email__iexact=identifier).first()
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)
            else:
                user = authenticate(username=identifier, password=password)

            if not user:
                raise forms.ValidationError("Invalid credentials. Please verify your username/email and password.")

            cleaned_data['user'] = user

        return cleaned_data


class VolunteerRegistrationForm(forms.Form):
    """
    Secure public volunteer sign-up form.
    Creates a User with hashed password and UserProfile with status='pending'.
    """
    AVAILABILITY_CHOICES = (
        ('every_sunday', 'Every Sunday (Food Distribution Drive)'),
        ('weekends', 'Weekends (Saturday & Sunday)'),
        ('blood_call', 'Blood Donation On-Call / Emergency'),
        ('events', 'Festival & Special Occasions'),
        ('flexible', 'Flexible / Anytime Required'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('unknown', 'Not Sure / Prefer not to say'),
    )

    full_name = forms.CharField(
        label="Full Name",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Pooja Deshmukh',
            'required': True,
            'autocomplete': 'name',
        })
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
            'required': True,
            'autocomplete': 'email',
        })
    )
    phone = forms.CharField(
        label="Mobile Number",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '10-digit mobile number (e.g. 9852827771)',
            'required': True,
            'autocomplete': 'tel',
        })
    )
    city = forms.CharField(
        label="City / Locality",
        max_length=150,
        initial="Chhatrapati Sambhajinagar",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Locality / Area (e.g. TV Center, CIDCO)',
            'required': True,
        })
    )
    availability = forms.ChoiceField(
        label="Availability",
        choices=AVAILABILITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'required': True})
    )
    blood_group = forms.ChoiceField(
        label="Blood Group",
        choices=BLOOD_GROUP_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    occupation = forms.CharField(
        label="Occupation / Student",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student / Professional / Healthcare / Other',
        })
    )
    interests = forms.CharField(
        label="Interests & Skills",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tell us about your interests (e.g. food drives, teaching children, medical camps)...',
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum 8 characters',
            'required': True,
            'autocomplete': 'new-password',
            'id': 'id_reg_password'
        })
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password',
            'required': True,
            'autocomplete': 'new-password',
            'id': 'id_reg_password_confirm'
        })
    )
    privacy_consent = forms.BooleanField(
        label="I agree to the privacy terms and volunteer code of conduct.",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists. Please log in.")
        return email

    def clean_phone(self):
        raw_phone = self.cleaned_data.get('phone')
        return validate_indian_phone(raw_phone)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')

        if p1 and p2:
            if len(p1) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            if p1 != p2:
                self.add_error('password_confirm', "Passwords do not match.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data['email'].lower().strip()
        full_name = cleaned_data['full_name'].strip()
        password = cleaned_data['password']

        # Generate unique username from email prefix
        base_username = re.sub(r'[^a-zA-Z0-9_]', '', email.split('@')[0]) or 'volunteer'
        username = base_username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{count}"
            count += 1

        # Name parts
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Create user with Django password hashing
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Profile gets status='pending' and role='volunteer'
        profile = UserProfile.get_profile_for_user(user)
        profile.role = 'volunteer'
        profile.status = 'pending'
        profile.phone = cleaned_data['phone']
        profile.city = cleaned_data['city']
        profile.availability = cleaned_data['availability']
        profile.blood_group = cleaned_data.get('blood_group', 'unknown')
        profile.occupation = cleaned_data.get('occupation', '')
        profile.interests = cleaned_data.get('interests', '')
        profile.privacy_consent = cleaned_data['privacy_consent']
        profile.save()

        # Also create/link Volunteer application record for unified admin tracking
        Volunteer.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=cleaned_data['phone'],
            city_area=cleaned_data['city'],
            availability=cleaned_data['availability'],
            blood_group=cleaned_data.get('blood_group', 'unknown'),
            occupation=cleaned_data.get('occupation', ''),
            motivation=cleaned_data.get('interests', '') or 'Registered via Volunteer Portal',
            status='pending'
        )

        return user


class ForgotPasswordRequestForm(forms.Form):
    """
    Initiates secure password reset request via email.
    """
    email = forms.EmailField(
        label="Registered Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered email address',
            'required': True,
            'autocomplete': 'email'
        })
    )


class ResetPasswordConfirmForm(forms.Form):
    """
    Sets a new password using a verified token.
    """
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'At least 8 characters',
            'required': True,
            'id': 'id_new_password'
        })
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your new password',
            'required': True,
            'id': 'id_confirm_new_password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')

        if p1 and p2:
            if len(p1) < 8:
                self.add_error('new_password', "Password must be at least 8 characters long.")
            if p1 != p2:
                self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class ProfileUpdateForm(forms.Form):
    """
    Allows authenticated users to view and update their personal profile.
    Strictly forbids role escalation.
    """
    first_name = forms.CharField(
        label="First Name",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': True})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'required': True})
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        label="City / Locality",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    occupation = forms.CharField(
        label="Occupation",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    blood_group = forms.ChoiceField(
        label="Blood Group",
        choices=VolunteerRegistrationForm.BLOOD_GROUP_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    availability = forms.ChoiceField(
        label="Availability",
        choices=VolunteerRegistrationForm.AVAILABILITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    interests = forms.CharField(
        label="Interests & Community Focus",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        profile = user.profile
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email
        self.fields['phone'].initial = profile.phone
        self.fields['city'].initial = profile.city
        self.fields['occupation'].initial = profile.occupation
        self.fields['blood_group'].initial = profile.blood_group
        self.fields['availability'].initial = profile.availability
        self.fields['interests'].initial = profile.interests

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if User.objects.filter(email__iexact=email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("Another account is already using this email address.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            return validate_indian_phone(phone)
        return ""

    def save(self):
        cleaned_data = self.cleaned_data
        self.user.first_name = cleaned_data['first_name'].strip()
        self.user.last_name = cleaned_data['last_name'].strip()
        self.user.email = cleaned_data['email'].lower().strip()
        self.user.save()

        profile = self.user.profile
        profile.phone = cleaned_data.get('phone', '')
        profile.city = cleaned_data.get('city', '')
        profile.occupation = cleaned_data.get('occupation', '')
        profile.blood_group = cleaned_data.get('blood_group', 'unknown')
        profile.availability = cleaned_data.get('availability', '')
        profile.interests = cleaned_data.get('interests', '')
        profile.save()
        return self.user


class ActivityReportSubmissionForm(forms.ModelForm):
    """
    Allows coordinators to submit on-ground activity reports and authentic photos.
    """
    class Meta:
        model = ActivityReport
        fields = [
            'title',
            'summary',
            'volunteers_present_count',
            'beneficiaries_served_count',
            'challenges_notes',
            'photo_1',
            'photo_2',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Sunday Food Drive Report - 120 Meals Distributed',
                'required': True
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide detailed outcomes, team execution, and areas covered...',
                'required': True
            }),
            'volunteers_present_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'required': True
            }),
            'beneficiaries_served_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'required': True
            }),
            'challenges_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any logistics constraints, weather difficulties, or improvements for next time...',
            }),
            'photo_1': forms.FileInput(attrs={'class': 'form-control'}),
            'photo_2': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AnnouncementCreationForm(forms.ModelForm):
    """
    Admin form to publish announcements for volunteers and coordinators.
    """
    class Meta:
        model = Announcement
        fields = [
            'title',
            'title_mr',
            'content',
            'content_mr',
            'target_role',
            'priority',
            'event',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'title_mr': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'content_mr': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'target_role': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

