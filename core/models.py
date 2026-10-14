"""
Database models for Swayamsevak Foundation website.
College Major Project.
"""

import os
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_image_file(file):
    """Ensure uploaded image is under 5MB and has valid extension."""
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError("File size exceeds 5MB limit. Please upload an image under 5MB.")
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        raise ValidationError("Unsupported file format. Allowed formats: JPG, JPEG, PNG, WEBP.")


def validate_achievement_media(file):
    """Ensure uploaded achievement certificate/media is under 5MB and valid format."""
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError("File size exceeds 5MB limit. Please upload a file under 5MB.")
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.pdf']:
        raise ValidationError("Unsupported file format. Allowed formats: JPG, JPEG, PNG, WEBP, PDF.")


class FoundationSetting(models.Model):
    """
    Singleton model to store official foundation metadata and content,
    fully editable by authorized administrators.
    """
    name = models.CharField(
        max_length=200,
        default="Swayamsevak Foundation",
        help_text="Official name of the foundation"
    )
    logo = models.ImageField(
        upload_to='logos/',
        blank=True,
        null=True,
        help_text="Official foundation logo emblem"
    )
    tagline_mr = models.CharField(
        max_length=255,
        default="स्वावलंबनातून समाजसेवा",
        verbose_name="Tagline (Marathi)"
    )
    tagline_en = models.CharField(
        max_length=255,
        default="Social Service through Self-Reliance",
        verbose_name="Tagline (English)"
    )
    established_date = models.CharField(
        max_length=100,
        default="January 2024",
        help_text="Official establishment period"
    )
    city = models.CharField(
        max_length=200,
        default="Chhatrapati Sambhajinagar, Maharashtra, India"
    )
    founder_president = models.CharField(
        max_length=200,
        default="Om Vinod Dhadbale"
    )
    phone = models.CharField(
        max_length=20,
        default="9852827771"
    )
    email = models.EmailField(
        default="swayamsevakfoundation24@gmail.com"
    )
    address = models.CharField(
        max_length=300,
        default="TV Center, Chhatrapati Sambhajinagar, 431001"
    )
    languages_supported = models.CharField(
        max_length=100,
        default="English and Marathi"
    )

    # Social Media Links
    instagram_url = models.URLField(
        max_length=300,
        default="https://www.instagram.com/swayamsevak_foundation/"
    )
    youtube_url = models.URLField(
        max_length=300,
        default="https://youtube.com/@swayamsevakfoundation"
    )
    whatsapp_group_url = models.URLField(
        max_length=300,
        default="https://chat.whatsapp.com/B4roMDAWjr4BMUCVspUgQE"
    )
    facebook_status = models.CharField(
        max_length=100,
        default="Pending",
        help_text="Official status of Facebook page"
    )

    # Official Foundation Belief
    belief = models.CharField(
        max_length=255,
        default="Humanity is the greatest service."
    )
    belief_mr = models.CharField(
        max_length=255,
        default="मानवता हीच खरी सेवा आहे."
    )

    # Official Our Story
    our_story_title = models.CharField(
        max_length=255,
        default="Our Story – Why We Started"
    )
    our_story_title_mr = models.CharField(
        max_length=255,
        default="आमची गोष्ट – आम्ही का सुरुवात केली"
    )
    our_story_text = models.TextField(
        default=(
            "Swayamsevak Foundation was started with one simple belief: "
            "Humanity is the greatest service.\n\n"
            "Our aim is to help people in need and work towards a hunger-free society. "
            "Every Sunday, our members come together to distribute food among underprivileged people, "
            "children in orphanages, elderly people, and homeless individuals.\n\n"
            "Along with hunger relief, we organize cleanliness drives, health and blood donation camps, "
            "and educational initiatives. We also celebrate festivals, birthdays, and special occasions "
            "with underprivileged communities by sharing food, clothes, sweets, and gifts. "
            "During winter, we distribute blankets to people sleeping on the streets.\n\n"
            "Our mission is to spread kindness, serve humanity, and bring smiles to those who need them most."
        )
    )
    our_story_text_mr = models.TextField(
        default=(
            "स्वयंसेवक फाउंडेशनची सुरुवात एका साध्या पण दृढ विश्वासाने झाली: "
            "मानवता हीच खरी सेवा आहे.\n\n"
            "गरजू व्यक्तींना मदत करणे आणि भूकमुक्त समाजाच्या दिशेने कार्य करणे हे आमचे मुख्य ध्येय आहे. "
            "दर रविवारी आमचे सदस्य एकत्र येऊन गरजू नागरिक, अनाथालयातील बालके, वृद्धाश्रमातील ज्येष्ठ आणि "
            "बेघर व्यक्तींना अन्नवाटप करतात.\n\n"
            "अन्नदानाच्या सोबतच आम्ही स्वच्छता मोहिमा, आरोग्य आणि रक्तदान शिबिरे, तसेच शैक्षणिक उपक्रम राबवतो. "
            "आम्ही सण, वाढदिवस आणि विशेष प्रसंग वंचित घटकांसोबत अन्न, वस्त्र, मिठाई आणि भेटवस्तू वाटून साजरे करतो. "
            "हिवाळ्यात रस्त्यावर झोपणाऱ्या निराधारांना उबदार ब्लँकेट्सचे वाटप केले जाते.\n\n"
            "दयाळूपणा पसरवणे, मानवतेची सेवा करणे आणि ज्यांना सर्वाधिक गरज आहे त्यांच्या चेहऱ्यावर हास्य फुलवणे "
            "हेच आमचे ध्येय आहे."
        )
    )

    # Official Mission
    mission_text = models.TextField(
        default=(
            "Our mission is to extend a helping hand to every needy person in society "
            "and serve humanity with compassion, kindness, and selfless dedication.\n\n"
            "Through our initiatives, Swayamsevak Foundation strives to spread humanity, "
            "bring smiles to people's faces, and make a meaningful difference in society."
        )
    )
    mission_text_mr = models.TextField(
        default=(
            "समाजातील प्रत्येक गरजू घटकाकडे मदतीचा हात पुढे करणे आणि करुणा, दयाळूपणा तसेच "
            "निःस्वार्थ समर्पणाने मानवतेची सेवा करणे हे आमचे ध्येय आहे.\n\n"
            "विविध समाजोपयोगी उपक्रमांच्या माध्यमातून स्वयंसेवक फाउंडेशन समाजात मानवता पसरवून "
            "लोकांच्या चेहऱ्यावर हास्य फुलवण्याचा आणि सकारात्मक बदल घडवण्याचा निरंतर प्रयत्न करते."
        )
    )

    # Official Vision
    vision_text = models.TextField(
        default=(
            "Our vision is to build a compassionate and hunger-free society where no one sleeps hungry, "
            "everyone lives with dignity, and every individual has the opportunity to lead a better life.\n\n"
            "We aspire to create a positive impact through hunger relief, education, healthcare, "
            "environmental protection, and community welfare. We envision a society where people support "
            "one another, celebrate happiness together, and work towards a better future for all."
        )
    )
    vision_text_mr = models.TextField(
        default=(
            "एक दयाळू, संवेदनशील आणि भूकमुक्त समाज निर्माण करणे जिथे कोणीही उपाशी झोपणार नाही, "
            "प्रत्येकजण सन्मानाने जगेल आणि प्रत्येकाला उत्तम जीवन जगण्याची संधी लाभेल, हे आमचे स्वप्न आहे.\n\n"
            "अन्नदान, शिक्षण, आरोग्यसेवा, पर्यावरण संरक्षण आणि समाजकल्याण यांच्या माध्यमातून "
            "सकारात्मक प्रभाव निर्माण करण्याची आमची आकांक्षा आहे."
        )
    )

    # Support / Contribution Transparency Note
    support_note = models.TextField(
        default=(
            "Direct online automated payment gateway (UPI/Cards) is currently in preparation "
            "pending official NGO institutional documentation verification. "
            "To support our regular food drives, winter blanket distribution, or child welfare activities, "
            "you can contribute in-kind, join as a volunteer, or contact our founder directly."
        )
    )
    support_note_mr = models.TextField(
        default=(
            "अधिकृत एनजीओ बँक व संस्थात्मक पडताळणी प्रक्रियेत असल्यामुळे थेट ऑनलाइन पेमेंट गेटवे लवकरच जोडले जाईल. "
            "आमच्या रविवार अन्नदान, हिवाळी ब्लँकेट वाटप किंवा बालकल्याण उपक्रमांना मदत करण्यासाठी आपण प्रत्यक्ष साहित्य, "
            "अन्नधान्य स्वरूपात मदत करू शकता किंवा थेट फाऊंडेशनशी संपर्क साधू शकता."
        )
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Foundation Setting"
        verbose_name_plural = "Foundation Settings"

    def __str__(self):
        return f"{self.name} - Configuration"

    @property
    def logo_url(self):
        """Returns uploaded logo URL or falls back to static transparent logo."""
        if self.logo and hasattr(self.logo, 'name') and self.logo.name:
            try:
                if self.logo.storage.exists(self.logo.name):
                    return self.logo.url
            except Exception:
                pass
        return '/static/images/logo.png'

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class ServiceArea(models.Model):
    """
    The 7 official key service areas of Swayamsevak Foundation.
    """
    title = models.CharField(max_length=200)
    title_mr = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField()
    short_description_mr = models.TextField()
    icon_bootstrap = models.CharField(
        max_length=100,
        default="bi-heart-fill",
        help_text="Bootstrap icon class name, e.g., bi-heart-fill, bi-people-fill, bi-hospital"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Key Service Area"
        verbose_name_plural = "Key Service Areas"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}. {self.title}"


class ActivityCategory(models.Model):
    """
    The 11 official activity categories of Swayamsevak Foundation:
    1. Food Donation
    2. Clothes Donation
    3. Blood Donation Camp
    4. Health Checkup Camp
    5. Vruddhashram Visits
    6. Anathashram Visits
    7. Cleanliness Drives
    8. Environment & Tree Plantation
    9. Children's Activities
    10. Awareness Campaigns
    11. Other Social Service Activities
    """
    name = models.CharField(max_length=150, help_text="Category name in English")
    name_mr = models.CharField(max_length=150, help_text="Category name in Marathi")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True)
    description_mr = models.TextField(blank=True)
    icon_bootstrap = models.CharField(
        max_length=100,
        default="bi-grid-fill",
        help_text="Bootstrap icon name, e.g., bi-egg-fried, bi-droplet-fill"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Activity Category"
        verbose_name_plural = "Activity Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def icon(self):
        return self.icon_bootstrap

    def __str__(self):
        return f"{self.order}. {self.name} ({self.name_mr})"


class Activity(models.Model):
    """
    Regular activities and service drives organized by the foundation.
    """
    STATUS_CHOICES = (
        ('regular', 'Regular Ongoing Drive'),
        ('seasonal', 'Seasonal / Special Occasion'),
        ('planned', 'Upcoming / Scheduled'),
    )

    title = models.CharField(max_length=255)
    title_mr = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(
        ActivityCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        help_text="Category among the 11 official activity categories"
    )
    service_area = models.ForeignKey(
        ServiceArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities'
    )
    date = models.DateField(null=True, blank=True, help_text="Activity date if specific")
    venue = models.CharField(
        max_length=255,
        default="TV Center, Chhatrapati Sambhajinagar",
        blank=True
    )
    schedule_frequency = models.CharField(
        max_length=150,
        default="Every Sunday",
        help_text="E.g. Every Sunday, During Winter, Festivals, Regular"
    )
    schedule_frequency_mr = models.CharField(
        max_length=150,
        default="दर रविवारी"
    )
    description = models.TextField()
    description_mr = models.TextField()
    image = models.ImageField(
        upload_to='activities/',
        blank=True,
        null=True,
        help_text="Upload authentic activity photograph (optional)"
    )
    placeholder_label = models.CharField(
        max_length=255,
        default="Authentic Foundation Activity Photo Placeholder",
        help_text="Display label when real photograph is awaited"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='regular'
    )
    video_url = models.URLField(
        max_length=300,
        blank=True,
        help_text="Optional YouTube / video link"
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Controls public visibility on website"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Foundation Activity"
        verbose_name_plural = "Foundation Activities"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Volunteer(models.Model):
    """
    Volunteer registration records submitted by the community.
    """
    AVAILABILITY_CHOICES = (
        ('every_sunday', 'Every Sunday (Food Drive)'),
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

    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved / Enrolled'),
        ('contacted', 'Contacted by Team'),
        ('inactive', 'Inactive'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='volunteer_record'
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city_area = models.CharField(
        max_length=150,
        help_text="Area / Locality in Chhatrapati Sambhajinagar or City"
    )
    preferred_service_area = models.ForeignKey(
        ServiceArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='volunteers'
    )
    availability = models.CharField(
        max_length=50,
        choices=AVAILABILITY_CHOICES,
        default='every_sunday'
    )
    blood_group = models.CharField(
        max_length=20,
        choices=BLOOD_GROUP_CHOICES,
        default='unknown'
    )
    occupation = models.CharField(
        max_length=100,
        blank=True,
        help_text="Student, Professional, Healthcare, etc."
    )
    motivation = models.TextField(
        help_text="Why do you wish to volunteer with Swayamsevak Foundation?"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes by Foundation staff"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Volunteer Registration"
        verbose_name_plural = "Volunteer Registrations"

    def __str__(self):
        return f"{self.full_name} ({self.phone}) - {self.get_status_display()}"


class SupportInquiry(models.Model):
    """
    Support & Contribution pledges submitted by well-wishers and donors.
    """
    SUPPORT_TYPE_CHOICES = (
        ('sunday_food', 'Sunday Hunger Relief Food Distribution'),
        ('winter_blankets', 'Winter Blanket Distribution Drive'),
        ('orphanage_care', 'Orphanage Children Support & Essentials'),
        ('old_age_home', 'Senior Citizens Old-Age Home Support'),
        ('gaushala_feed', 'Gaushala Animal Feed & Welfare'),
        ('hospital_patient', 'Government Hospital Patient Assistance'),
        ('blood_drive', 'Blood Donation Camp Support'),
        ('other', 'Other Community Initiative'),
    )

    MODE_CHOICES = (
        ('in_kind', 'In-Kind Contribution (Food, Blankets, Clothes, Gifts)'),
        ('sponsor_food', 'Sponsor Sunday Meal Distribution'),
        ('join_service', 'Direct Physical Service & Assistance'),
        ('discuss_founder', 'Discuss directly with Founder / President'),
    )

    STATUS_CHOICES = (
        ('new', 'New Support Pledge'),
        ('contacted', 'Contacted / Followed Up'),
        ('completed', 'Completed / Fulfilled'),
        ('archived', 'Archived'),
    )

    supporter_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    city = models.CharField(
        max_length=150,
        default="Chhatrapati Sambhajinagar"
    )
    support_type = models.CharField(
        max_length=50,
        choices=SUPPORT_TYPE_CHOICES,
        default='sunday_food'
    )
    preferred_mode = models.CharField(
        max_length=50,
        choices=MODE_CHOICES,
        default='in_kind'
    )
    message = models.TextField(
        help_text="Details of how you would like to support"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new'
    )
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Support Pledge / Inquiry"
        verbose_name_plural = "Support Pledges & Inquiries"

    def __str__(self):
        return f"{self.supporter_name} - {self.get_support_type_display()} ({self.get_status_display()})"


class ContactInquiry(models.Model):
    """
    General inquiries submitted through the contact page.
    """
    STATUS_CHOICES = (
        ('new', 'New Message'),
        ('read', 'Read'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    )

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name}: {self.subject} ({self.created_at.strftime('%d-%m-%Y')})"


class GalleryItem(models.Model):
    """
    Visual showcase of foundation activities with real uploads or labeled placeholders.
    """
    title = models.CharField(max_length=200)
    title_mr = models.CharField(max_length=200)
    service_area = models.ForeignKey(
        ServiceArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gallery_items'
    )
    image = models.ImageField(
        upload_to='gallery/',
        null=True,
        blank=True,
        help_text="Upload authentic photograph when available"
    )
    placeholder_label = models.CharField(
        max_length=255,
        default="Authentic Foundation Activity Photo Placeholder",
        help_text="Clearly labeled placeholder text"
    )
    caption = models.CharField(max_length=300)
    caption_mr = models.CharField(max_length=300)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return self.title


class GalleryMedia(models.Model):
    """
    Administrator-managed photos and videos for Swayamsevak Foundation.
    Associated with activities and events.
    Displays empty states when authentic media is unavailable (no fake placeholders).
    """
    MEDIA_TYPE_CHOICES = (
        ('photo', 'Photograph'),
        ('video', 'Video'),
    )

    title = models.CharField(max_length=200)
    title_mr = models.CharField(max_length=200, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default='photo')
    image = models.ImageField(
        upload_to='gallery/',
        null=True,
        blank=True,
        help_text="Upload authentic photograph (JPG, PNG, WebP under 10MB)"
    )
    video_url = models.URLField(
        max_length=300,
        blank=True,
        help_text="YouTube or external embed video URL"
    )
    activity = models.ForeignKey(
        Activity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='gallery_media'
    )
    event = models.ForeignKey(
        'Event',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='gallery_media'
    )
    category = models.ForeignKey(
        ActivityCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='gallery_media'
    )
    caption = models.CharField(max_length=300, blank=True)
    caption_mr = models.CharField(max_length=300, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Gallery Media"
        verbose_name_plural = "Gallery Media Items"

    def __str__(self):
        return f"[{self.get_media_type_display()}] {self.title}"


class UserProfile(models.Model):
    """
    Role-based user profile extending Django's auth.User.
    Supports three distinct roles: Admin, Coordinator, and Volunteer.
    """
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('coordinator', 'Coordinator'),
        ('volunteer', 'Volunteer'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved / Active'),
        ('suspended', 'Suspended'),
        ('deactivated', 'Deactivated'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='volunteer'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(
        max_length=150,
        blank=True,
        default="Chhatrapati Sambhajinagar"
    )
    interests = models.TextField(
        blank=True,
        help_text="Key areas of interest or skills (e.g. food distribution, teaching, health camps)"
    )
    availability = models.CharField(
        max_length=50,
        blank=True,
        default="every_sunday"
    )
    blood_group = models.CharField(
        max_length=20,
        blank=True,
        default="unknown"
    )
    occupation = models.CharField(max_length=100, blank=True)
    privacy_consent = models.BooleanField(
        default=True,
        help_text="Consent to privacy policy and volunteer terms"
    )
    assigned_activities = models.ManyToManyField(
        Activity,
        blank=True,
        related_name='assigned_coordinators',
        help_text="Activities this coordinator is authorized to manage"
    )
    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_user_profiles'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()} - {self.get_status_display()})"

    @property
    def is_admin_role(self):
        return self.role == 'admin' or self.user.is_superuser

    @property
    def is_coordinator_role(self):
        return self.role == 'coordinator'

    @property
    def is_volunteer_role(self):
        return self.role == 'volunteer'

    @property
    def is_active_and_approved(self):
        return self.status == 'approved' and self.user.is_active

    @classmethod
    def get_profile_for_user(cls, user):
        """
        Safe helper to fetch or initialize profile for any user (including superusers).
        """
        profile, created = cls.objects.get_or_create(
            user=user,
            defaults={
                'role': 'admin' if user.is_superuser else 'volunteer',
                'status': 'approved' if user.is_superuser else 'pending',
                'phone': '',
                'city': 'Chhatrapati Sambhajinagar',
                'privacy_consent': True,
            }
        )
        if user.is_superuser and profile.role != 'admin':
            profile.role = 'admin'
            profile.status = 'approved'
            profile.save()
        return profile


class Event(models.Model):
    """
    Specific on-ground volunteer events, scheduled drives, or camp sessions.
    """
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    title = models.CharField(max_length=255)
    title_mr = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    activity = models.ForeignKey(
        Activity,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='events'
    )
    service_area = models.ForeignKey(
        ServiceArea,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='events'
    )
    coordinator = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='coordinated_events',
        help_text="Designated coordinator leading this event"
    )
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(
        max_length=255,
        default="TV Center, Chhatrapati Sambhajinagar"
    )
    description = models.TextField()
    description_mr = models.TextField(blank=True)
    max_volunteers = models.PositiveIntegerField(
        default=25,
        help_text="Maximum capacity of volunteers for this session"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming'
    )
    venue = models.CharField(
        max_length=255,
        default="TV Center, Chhatrapati Sambhajinagar",
        blank=True
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Publicly display on events and programs page"
    )
    registration_enabled = models.BooleanField(
        default=True,
        help_text="Allow volunteer self-registration"
    )
    registration_deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Registration cutoff date and time"
    )
    reminders_enabled = models.BooleanField(
        default=True,
        help_text="Enable automated reminders for registered volunteers"
    )
    is_closed = models.BooleanField(
        default=False,
        help_text="Explicitly mark event registration as closed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date', 'start_time']
        verbose_name = "Foundation Event"
        verbose_name_plural = "Foundation Events"

    def save(self, *args, **kwargs):
        if not self.venue and self.location:
            self.venue = self.location
        if not self.location and self.venue:
            self.location = self.venue
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.event_date}")
            unique_slug = base_slug
            num = 1
            while Event.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.event_date.strftime('%d-%m-%Y')})"

    @property
    def registered_count(self):
        return self.registrations.filter(status__in=['registered', 'attended']).count()

    @property
    def is_full(self):
        return self.registered_count >= self.max_volunteers

    @property
    def can_register(self):
        """Checks if a volunteer can register for this event."""
        if not self.is_published or not self.registration_enabled or self.is_closed:
            return False
        if self.status != 'upcoming':
            return False
        if self.is_full:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        return True


class EventRegistration(models.Model):
    """
    Tracks volunteer registrations and attendance for events.
    """
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('absent', 'Absent'),
        ('cancelled', 'Cancelled'),
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    attendance_marked_at = models.DateTimeField(null=True, blank=True)
    attendance_marked_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='marked_attendances'
    )
    volunteer_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('event', 'volunteer')
        ordering = ['-registered_at']
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.volunteer.username} -> {self.event.title} ({self.get_status_display()})"


class ActivityReport(models.Model):
    """
    Field reports submitted by coordinators for admin approval.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    coordinator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submitted_reports'
    )
    title = models.CharField(max_length=255)
    summary = models.TextField(
        help_text="Detailed summary of activities conducted, items distributed, and outcomes"
    )
    volunteers_present_count = models.PositiveIntegerField(
        default=0,
        help_text="Actual number of volunteers who participated"
    )
    beneficiaries_served_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of people/animals directly served"
    )
    challenges_notes = models.TextField(
        blank=True,
        help_text="Challenges faced, logistics issues, or suggestions"
    )
    photo_1 = models.ImageField(
        upload_to='activity_reports/',
        null=True,
        blank=True,
        help_text="Authentic activity photograph 1"
    )
    photo_2 = models.ImageField(
        upload_to='activity_reports/',
        null=True,
        blank=True,
        help_text="Authentic activity photograph 2"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_feedback = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_reports'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Coordinator Activity Report"
        verbose_name_plural = "Coordinator Activity Reports"

    def __str__(self):
        return f"Report: {self.title} by {self.coordinator.username} ({self.get_status_display()})"


class Announcement(models.Model):
    """
    Official announcements and notifications targeted to volunteers and coordinators.
    Also supports public impact stories when marked as story and published.
    """
    TARGET_CHOICES = (
        ('all', 'All Users / Public'),
        ('volunteer', 'Volunteers Only'),
        ('coordinator', 'Coordinators Only'),
    )

    PRIORITY_CHOICES = (
        ('normal', 'Normal'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent Announcement'),
    )

    TYPE_CHOICES = (
        ('announcement', 'Official Announcement'),
        ('story', 'Community Impact Story'),
    )

    title = models.CharField(max_length=255)
    title_mr = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True, default='')
    announcement_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='announcement'
    )
    content = models.TextField()
    content_mr = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='announcements/',
        null=True,
        blank=True,
        help_text="Optional authentic image for announcement or impact story"
    )
    target_role = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default='all'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    event = models.ForeignKey(
        Event,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='announcements'
    )
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True, help_text="Publicly display on stories/announcements page")
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Announcement & Story"
        verbose_name_plural = "Announcements & Stories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Announcement.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.title}"


class AuditLog(models.Model):
    """
    Tracks significant administrative and operational actions for accountability.
    """
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='audit_entries'
    )
    action = models.CharField(max_length=100)
    target_repr = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        user_name = self.user.username if self.user else "System"
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} | {user_name} | {self.action} | {self.target_repr}"

    @classmethod
    def log_action(cls, user, action, target_repr, details="", ip_address=None):
        return cls.objects.create(
            user=user if (user and user.is_authenticated) else None,
            action=action,
            target_repr=str(target_repr)[:255],
            details=details,
            ip_address=ip_address
        )


class LoginAttempt(models.Model):
    """
    Database-backed login attempt tracker to mitigate brute-force attacks.
    """
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15

    username_or_email = models.CharField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    failed_attempts = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)
    locked_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('username_or_email', 'ip_address')
        verbose_name = "Login Attempt Tracker"
        verbose_name_plural = "Login Attempt Trackers"

    def __str__(self):
        return f"{self.username_or_email} ({self.ip_address}): {self.failed_attempts} fails"

    @classmethod
    def is_locked(cls, identifier, ip_address):
        """
        Check if the identifier or IP is currently locked out.
        """
        now = timezone.now()
        attempt = cls.objects.filter(
            username_or_email=identifier.lower().strip(),
            ip_address=ip_address
        ).first()

        if attempt and attempt.locked_until:
            if attempt.locked_until > now:
                remaining_seconds = int((attempt.locked_until - now).total_seconds())
                return True, int(remaining_seconds / 60) + 1
            else:
                # Lockout expired, reset
                attempt.failed_attempts = 0
                attempt.locked_until = None
                attempt.save()
        return False, 0

    @classmethod
    def record_failure(cls, identifier, ip_address):
        """
        Increment failed attempt counter and apply lockout if threshold exceeded.
        """
        now = timezone.now()
        attempt, created = cls.objects.get_or_create(
            username_or_email=identifier.lower().strip(),
            ip_address=ip_address,
            defaults={'failed_attempts': 0}
        )
        attempt.failed_attempts += 1
        attempt.last_attempt = now

        if attempt.failed_attempts >= cls.MAX_FAILED_ATTEMPTS:
            attempt.locked_until = now + timezone.timedelta(minutes=cls.LOCKOUT_DURATION_MINUTES)

        attempt.save()
        return attempt

    @classmethod
    def record_success(cls, identifier, ip_address):
        """
        Reset failed attempts upon successful login.
        """
        cls.objects.filter(
            username_or_email=identifier.lower().strip(),
            ip_address=ip_address
        ).delete()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Ensure every User has an associated UserProfile.
    Superusers automatically receive Admin role and Approved status.
    """
    if created:
        role = 'admin' if instance.is_superuser else 'volunteer'
        status = 'approved' if instance.is_superuser else 'pending'
        UserProfile.objects.create(
            user=instance,
            role=role,
            status=status,
            privacy_consent=True
        )
    else:
        if hasattr(instance, 'profile'):
            if instance.is_superuser and instance.profile.role != 'admin':
                instance.profile.role = 'admin'
                instance.profile.status = 'approved'
                instance.profile.save()


class DonationRecord(models.Model):
    """
    Transparent support and in-kind donation records managed by admins.
    """
    DONATION_TYPE_CHOICES = (
        ('in_kind_food', 'Food & Ration Supplies (Sunday Drive)'),
        ('in_kind_blankets', 'Warm Blankets (Winter Relief)'),
        ('in_kind_clothes', 'Clothes & Essentials'),
        ('in_kind_educational', 'Educational Supplies (Orphanage)'),
        ('in_kind_medical', 'Medicines & Health Camp Supplies'),
        ('animal_feed', 'Animal Feed / Gaushala Support'),
        ('monetary_pledge', 'Monetary Pledge (Receipt Awaited)'),
        ('other', 'Other Community Support'),
    )

    STATUS_CHOICES = (
        ('pledged', 'Pledged by Supporter'),
        ('received', 'Received & Verified'),
        ('distributed', 'Distributed to Beneficiaries'),
        ('cancelled', 'Cancelled'),
    )

    supporter_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=150, default="Chhatrapati Sambhajinagar")
    donation_type = models.CharField(max_length=50, choices=DONATION_TYPE_CHOICES, default='in_kind_food')
    quantity_or_amount = models.CharField(max_length=200, help_text="e.g. 100 food packets, 25 blankets, or ₹5000 pledge")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pledged')
    receipt_number = models.CharField(max_length=100, blank=True)
    is_public = models.BooleanField(default=False, help_text="Display on verified donor roll if permitted")
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donation / Contribution Record"
        verbose_name_plural = "Donation & Contribution Records"

    def __str__(self):
        return f"{self.supporter_name} - {self.get_donation_type_display()} ({self.get_status_display()})"


class ImpactStatistic(models.Model):
    """
    Verified impact statistics entered and published by authorized administrators.
    Never fabricated: displays empty state or verified stats only.
    """
    METRIC_CHOICES = (
        ('years_of_service', 'Total Years of Service'),
        ('activities_conducted', 'Total Activities Conducted'),
        ('volunteers_involved', 'Total Volunteers Involved'),
        ('meals_distributed', 'Total Meals Distributed'),
        ('people_reached', 'Total People Reached / Benefited'),
        ('clothes_distributed', 'Total Clothes or Essential Items Distributed'),
        ('children_reached', 'Total Children Reached'),
        ('elderly_reached', 'Total Elderly People Reached'),
        ('cleanliness_drives', 'Total Cleanliness Drives'),
        ('trees_planted', 'Total Trees Planted'),
        ('custom', 'Custom Metric'),
    )

    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified & Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    )

    metric_key = models.CharField(
        max_length=50,
        choices=METRIC_CHOICES,
        default='custom',
        help_text="Standardized metric category"
    )
    title = models.CharField(max_length=150, help_text="Statistic title in English")
    title_mr = models.CharField(max_length=150, help_text="Statistic title in Marathi")
    numeric_value = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Numeric count (for calculations & counter animations)"
    )
    metric_value = models.CharField(
        max_length=50,
        blank=True,
        help_text="Formatted display string (e.g. '50+', '5,000+', '100%')"
    )
    unit_label = models.CharField(max_length=100, blank=True, help_text="e.g. Sunday Drives Conducted, Meals Served")
    unit_label_mr = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, help_text="Context / methodology notes in English")
    description_mr = models.TextField(blank=True, help_text="Context in Marathi")
    reporting_period = models.CharField(
        max_length=150,
        blank=True,
        help_text="e.g. 'January 2024 - Present' or 'Annual 2025-26'"
    )
    last_updated_date = models.DateField(null=True, blank=True, help_text="Date metric was last updated/audited")
    icon_bootstrap = models.CharField(max_length=100, default="bi-heart-fill")
    order = models.PositiveIntegerField(default=1)
    internal_verification_notes = models.TextField(
        blank=True,
        help_text="PRIVATE internal audit notes and proof source. Never exposed publicly."
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending',
        help_text="Only 'verified' records can appear publicly"
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Only published by admin when verified"
    )
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='verified_statistics'
    )
    verified_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Impact Statistic"
        verbose_name_plural = "Impact Statistics"

    def __str__(self):
        val = self.display_value
        return f"{val} {self.unit_label} ({self.title}) [{self.get_verification_status_display()}]"

    @property
    def display_value(self):
        """Returns the formatted metric value, falling back to numeric_value formatted."""
        if self.metric_value:
            return self.metric_value
        if self.numeric_value is not None:
            return f"{self.numeric_value:,}+"
        return ""

    @property
    def is_verified_and_approved(self):
        return self.verification_status == 'verified' and self.is_published

    @classmethod
    def get_calculated_years_of_service(cls):
        """Calculate verified years of service from foundation establishment (January 2024)."""
        now = timezone.now()
        years = now.year - 2024
        if now.month < 1:
            years -= 1
        return max(1, years)


class Achievement(models.Model):
    """
    Genuine achievements, awards, and recognitions conferred to Swayamsevak Foundation.
    Verified and approved by authorized administrators. Never fabricated.
    """
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified & Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    )

    title = models.CharField(max_length=255, help_text="Title in English")
    title_mr = models.CharField(max_length=255, blank=True, help_text="Title in Marathi")
    description = models.TextField(help_text="Description in English")
    description_mr = models.TextField(blank=True, help_text="Description in Marathi")
    date_received = models.DateField(help_text="Date of award or recognition")
    awarding_organization = models.CharField(
        max_length=255,
        help_text="Conferring organization, department, or institution"
    )
    awarding_organization_mr = models.CharField(max_length=255, blank=True)
    supporting_media = models.FileField(
        upload_to='achievements/',
        null=True,
        blank=True,
        validators=[validate_achievement_media],
        help_text="Official certificate, citation document, or photo (under 5MB: JPG, PNG, WEBP, PDF)"
    )
    order = models.PositiveIntegerField(default=1)
    internal_verification_notes = models.TextField(
        blank=True,
        help_text="PRIVATE internal proof, audit trail, or citation notes. Never exposed publicly."
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Controls public visibility on website"
    )
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='verified_achievements'
    )
    verified_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-date_received']
        verbose_name = "Achievement & Recognition"
        verbose_name_plural = "Achievements & Recognitions"

    def __str__(self):
        return f"{self.title} ({self.awarding_organization})"

    @property
    def is_verified_and_approved(self):
        return self.verification_status == 'verified' and self.is_published

    @property
    def is_pdf(self):
        if self.supporting_media:
            return self.supporting_media.name.lower().endswith('.pdf')
        return False


class Collaboration(models.Model):
    """
    Confirmed partner organizations, civic authorities, and institutional collaborations.
    Never fabricated or implied without authorization.
    """
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified & Approved'),
        ('rejected', 'Rejected'),
        ('archived', 'Archived'),
    )

    organization_name = models.CharField(max_length=255, help_text="Partner organization name in English")
    organization_name_mr = models.CharField(max_length=255, blank=True, help_text="Partner organization name in Marathi")
    collaboration_purpose = models.TextField(help_text="Purpose and scope of joint humanitarian effort in English")
    collaboration_purpose_mr = models.TextField(blank=True, help_text="Purpose in Marathi")
    activities_conducted = models.TextField(blank=True, help_text="Joint activities conducted in English")
    activities_conducted_mr = models.TextField(blank=True, help_text="Joint activities in Marathi")
    collaboration_period = models.CharField(
        max_length=150,
        help_text="e.g. 'January 2024 - Present', 'June 2025'"
    )
    partner_logo = models.ImageField(
        upload_to='collaborations/',
        null=True,
        blank=True,
        validators=[validate_image_file],
        help_text="Authorized partner logo or drive photo (under 5MB: JPG, PNG, WEBP)"
    )
    partner_website = models.URLField(blank=True, help_text="Official website of partner organization (optional)")
    order = models.PositiveIntegerField(default=1)
    internal_verification_notes = models.TextField(
        blank=True,
        help_text="PRIVATE internal confirmation/agreement notes. Never exposed publicly."
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Controls public visibility on website"
    )
    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='verified_collaborations'
    )
    verified_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Important Collaboration"
        verbose_name_plural = "Important Collaborations"

    def __str__(self):
        return f"{self.organization_name} ({self.collaboration_period})"

    @property
    def is_verified_and_approved(self):
        return self.verification_status == 'verified' and self.is_published



class ReminderLog(models.Model):
    """
    Audit log of event reminders dispatched or queued for volunteers.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminder_logs')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_reminder_logs')
    reminder_type = models.CharField(
        max_length=50,
        choices=(
            ('email', 'Email Notification'),
            ('in_app', 'In-App Announcement'),
            ('sms', 'SMS (Pending Gateway)'),
        ),
        default='in_app'
    )
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('sent', 'Sent'),
            ('failed', 'Failed'),
            ('queued', 'Queued'),
        ),
        default='sent'
    )
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Reminder Log"
        verbose_name_plural = "Reminder Logs"

    def __str__(self):
        return f"Reminder: {self.event.title} -> {self.recipient.username} ({self.status})"


# Model aliases for architectural compliance
FoundationSettings = FoundationSetting
AdminAuditLog = AuditLog
VolunteerApplication = Volunteer
Enquiry = ContactInquiry
Recognition = Achievement
PartnerCollaboration = Collaboration


