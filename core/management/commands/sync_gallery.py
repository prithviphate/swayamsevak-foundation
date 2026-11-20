"""
Django management command to automatically synchronize images from
`static/images/gallery/` and `media/gallery/` into the `GalleryMedia` database records.
This allows the user to simply copy photos into `static/images/gallery/` and run:
    python manage.py sync_gallery
to have them immediately published, categorized, and animated on the website.
"""

import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import GalleryMedia, ActivityCategory, Activity


class Command(BaseCommand):
    help = "Synchronizes photos from static/images/gallery/ and media/gallery/ into GalleryMedia records."

    def handle(self, *args, **options):
        self.stdout.write("Scanning gallery folders for foundation activity photos...")

        static_gallery_dir = Path(settings.BASE_DIR) / 'static' / 'images' / 'gallery'
        media_gallery_dir = Path(settings.MEDIA_ROOT) / 'gallery'

        static_gallery_dir.mkdir(parents=True, exist_ok=True)
        media_gallery_dir.mkdir(parents=True, exist_ok=True)

        # Collect image files from both locations
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        synced_files = set()

        # Step 1: Sync static -> media
        for f in static_gallery_dir.iterdir():
            if f.is_file() and f.suffix.lower() in valid_extensions:
                dest = media_gallery_dir / f.name
                if not dest.exists() or dest.stat().st_size != f.stat().st_size:
                    shutil.copy2(f, dest)
                synced_files.add(f.name)

        # Step 2: Sync media -> static
        for f in media_gallery_dir.iterdir():
            if f.is_file() and f.suffix.lower() in valid_extensions:
                dest = static_gallery_dir / f.name
                if not dest.exists() or dest.stat().st_size != f.stat().st_size:
                    shutil.copy2(f, dest)
                synced_files.add(f.name)

        if not synced_files:
            self.stdout.write(self.style.WARNING("No images found in static/images/gallery/ or media/gallery/."))
            return

        self.stdout.write(f"Found {len(synced_files)} photo(s). Registering in GalleryMedia...")

        categories = {cat.slug: cat for cat in ActivityCategory.objects.all()}

        order_idx = 1
        for filename in sorted(synced_files):
            name_lower = filename.lower()
            rel_image_path = f"gallery/{filename}"

            # Auto-detect context from filename keywords
            if any(k in name_lower for k in ['mashal', 'yatra', 'shiv']):
                title = "Shiv Janmotsav Grand Mashal Yatra"
                title_mr = "शिवजन्मोत्सव भव्य-दिव्य मशाल यात्रा"
                category = categories.get('other-social-service-activities') or categories.get('awareness-campaigns')
                caption = "Grand Mashal Yatra from Mondha Naka to Kranti Chowk organized by Swayamsevak Foundation."
                caption_mr = "मोंढा नाका ते क्रांती चौक स्वयंसेवक फाऊंडेशन, छत्रपती संभाजीनगर आयोजित भव्य-दिव्य मशाल यात्रा."
            elif any(k in name_lower for k in ['food', 'annadan', 'meal']):
                title = "Sunday Hunger Relief Food Distribution Drive"
                title_mr = "दर रविवारी अन्नदान उपक्रम"
                category = categories.get('food-donation')
                caption = "Nutritious meal distribution to needy individuals and families in Chhatrapati Sambhajinagar."
                caption_mr = "छत्रपती संभाजीनगर येथे गरजू नागरिकांसाठी दर रविवारी राबवला जाणारा अन्नदान उपक्रम."
            elif any(k in name_lower for k in ['blood', 'rakt']):
                title = "Voluntary Blood Donation Camp"
                title_mr = "स्वयंस्फूर्त रक्तदान शिबिर"
                category = categories.get('blood-donation-camp')
                caption = "Lifesaving voluntary blood donation drive organized in association with local healthcare teams."
                caption_mr = "रुग्णांचे प्राण वाचवण्यासाठी आयोजित स्वयंस्फूर्त रक्तदान शिबिर."
            elif any(k in name_lower for k in ['health', 'checkup', 'medical']):
                title = "Free Community Health Checkup Camp"
                title_mr = "मोफत आरोग्य तपासणी शिबिर"
                category = categories.get('health-checkup-camp')
                caption = "Free diagnostic screening, medical consultation, and basic medicine support."
                caption_mr = "गरजू नागरिकांसाठी मोफत आरोग्य तपासणी, औषधोपचार आणि मार्गदर्शन शिबिर."
            elif any(k in name_lower for k in ['blanket', 'cloth', 'kapde', 'vastra']):
                title = "Winter Blanket & Clothes Distribution Drive"
                title_mr = "हिवाळी ब्लँकेट व वस्त्रदान मोहीम"
                category = categories.get('clothes-donation')
                caption = "Warm clothing and winter blankets distributed to homeless persons and underprivileged families."
                caption_mr = "रस्त्यांवरील बेघर आणि गरजू कुटुंबांसाठी उबदार ब्लँकेट्स व कपड्यांचे वाटप."
            elif any(k in name_lower for k in ['clean', 'swachh']):
                title = "Cleanliness & Environment Drive"
                title_mr = "स्वच्छता व पर्यावरण संवर्धन मोहीम"
                category = categories.get('cleanliness-drives')
                caption = "Community cleanliness drive and waste clearance by foundation volunteers."
                caption_mr = "परिसर स्वच्छता आणि जनजागृतीसाठी स्वयंसेवकांनी राबवलेली स्वच्छता मोहीम."
            elif any(k in name_lower for k in ['tree', 'plant', 'vriksh']):
                title = "Tree Plantation & Greenery Initiative"
                title_mr = "वृक्षारोपण व पर्यावरण संवर्धन"
                category = categories.get('environment-tree-plantation')
                caption = "Plantation and nurturing of saplings across city areas and public spaces."
                caption_mr = "परिसरात हिरवळ वाढवण्यासाठी स्वयंसेवकांमार्फत वृक्षारोपण उपक्रम."
            elif any(k in name_lower for k in ['child', 'anath', 'balak']):
                title = "Orphanage Children Support & Happiness Drive"
                title_mr = "अनाथालय बालके भेट व स्नेह उपक्रम"
                category = categories.get('childrens-activities') or categories.get('anathashram-visits')
                caption = "Distributing educational kits, snacks, and celebrating joyous occasions with children."
                caption_mr = "अनाथालयातील बालकांसोबत सण साजरे करणे व शैक्षणिक साहित्य वाटप करणे."
            elif any(k in name_lower for k in ['vruddh', 'elder', 'senior']):
                title = "Old Age Home Support & Senior Citizen Care"
                title_mr = "वृद्धाश्रम भेट व ज्येष्ठ नागरिक सेवा"
                category = categories.get('vruddhashram-visits')
                caption = "Spending quality time, offering emotional warmth and nutrition to senior citizens."
                caption_mr = "वृद्धाश्रमातील ज्येष्ठांशी संवाद, मायेची ऊब आणि स्नेहभोजन सेवा."
            elif any(k in name_lower for k in ['gau', 'cow', 'animal']):
                title = "Gaushala Fodder & Animal Welfare Drive"
                title_mr = "गोशाळा चारा व प्राणी कल्याण उपक्रम"
                category = categories.get('other-social-service-activities')
                caption = "Providing fresh fodder, water facilities, and medical care for cattle and stray animals."
                caption_mr = "गोशाळेत हिरवा चारा पुरवणे आणि मुक्या जनावरांची देखभाल करणे."
            else:
                base_name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
                title = f"Foundation Activity - {base_name}"
                title_mr = f"संस्था उपक्रम - {base_name}"
                category = categories.get('other-social-service-activities')
                caption = "Social service initiative conducted by Swayamsevak Foundation, Chhatrapati Sambhajinagar."
                caption_mr = "स्वयंसेवक फाऊंडेशन, छत्रपती संभाजीनगर यांच्यामार्फत आयोजित समाजसेवा उपक्रम."

            media_item, created = GalleryMedia.objects.update_or_create(
                image=rel_image_path,
                defaults={
                    'title': title,
                    'title_mr': title_mr,
                    'media_type': 'photo',
                    'category': category,
                    'caption': caption,
                    'caption_mr': caption_mr,
                    'is_featured': True,
                    'is_published': True,
                    'order': order_idx,
                }
            )
            order_idx += 1
            status_text = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"[{status_text}] {title} ({filename})"))

        self.stdout.write(self.style.SUCCESS(f"Successfully synchronized {len(synced_files)} gallery photo(s)!"))
