"""
Management command to seed verified official Swayamsevak Foundation data.
Ensures zero fictitious data is invented while pre-populating all official facts.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import (
    FoundationSetting,
    ServiceArea,
    ActivityCategory,
    Activity,
    GalleryItem,
    GalleryMedia,
    UserProfile,
    Event,
    EventRegistration,
    Announcement,
    DonationRecord,
    ImpactStatistic,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds official Swayamsevak Foundation details, 7 service areas, and regular activities."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Swayamsevak Foundation official data...")

        # 1. Foundation Setting Singleton
        setting, created = FoundationSetting.objects.get_or_create(id=1)
        setting.name = "Swayamsevak Foundation"
        setting.logo = "logos/logo.png"
        setting.tagline_mr = "स्वावलंबनातून समाजसेवा"
        setting.tagline_en = "Social Service through Self-Reliance"
        setting.established_date = "January 2024"
        setting.city = "Chhatrapati Sambhajinagar, Maharashtra, India"
        setting.founder_president = "Om Vinod Dhadbale"
        setting.phone = "9852827771"
        setting.email = "swayamsevakfoundation24@gmail.com"
        setting.address = "TV Center, Chhatrapati Sambhajinagar, 431001"
        setting.languages_supported = "English and Marathi"
        setting.instagram_url = "https://www.instagram.com/swayamsevak_foundation/"
        setting.youtube_url = "https://youtube.com/@swayamsevakfoundation"
        setting.whatsapp_group_url = "https://chat.whatsapp.com/B4roMDAWjr4BMUCVspUgQE"
        setting.facebook_status = "Pending"
        setting.belief = "Humanity is the greatest service."
        setting.belief_mr = "मानवता हीच खरी सेवा आहे."
        setting.our_story_title = "Our Story – Why We Started"
        setting.our_story_title_mr = "आमची गोष्ट – आम्ही का सुरुवात केली"
        setting.our_story_text = (
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
        setting.our_story_text_mr = (
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
        setting.mission_text = (
            "Our mission is to extend a helping hand to every needy person in society "
            "and serve humanity with compassion, kindness, and selfless dedication.\n\n"
            "Our key areas of service include:\n"
            "• Supporting orphanage children by providing help, care, and essential support.\n"
            "• Serving senior citizens in old-age homes.\n"
            "• Providing food and care for animals in cow shelters (Gaushalas).\n"
            "• Assisting needy patients in government hospitals.\n"
            "• Promoting blood donation and supporting initiatives that help save lives.\n"
            "• Conducting social awareness campaigns.\n"
            "• Organizing community welfare and social service activities.\n\n"
            "Through these initiatives, Swayamsevak Foundation strives to spread humanity, "
            "bring smiles to people's faces, and make a meaningful difference in society.\n\n"
            "Our belief: Humanity is the greatest service."
        )
        setting.mission_text_mr = (
            "समाजातील प्रत्येक गरजू घटकाकडे मदतीचा हात पुढे करणे आणि करुणा, दयाळूपणा तसेच "
            "निःस्वार्थ समर्पणाने मानवतेची सेवा करणे हे आमचे ध्येय आहे.\n\n"
            "आमच्या सेवेची मुख्य क्षेत्रे:\n"
            "• अनाथालयातील बालकांना मदत, काळजी आणि आवश्यक आधार देणे.\n"
            "• वृद्धाश्रमातील ज्येष्ठ नागरिकांची सेवा करणे.\n"
            "• गोशाळांमधील मुक्या जनावरांना चारा आणि देखभाल पुरवणे.\n"
            "• शासकीय रुग्णालयांतील गरजू रुग्णांना साहाय्य करणे.\n"
            "• रक्तदानाला प्रोत्साहन देणे आणि जीवन वाचवणाऱ्या उपक्रमांना पाठबळ देणे.\n"
            "• सामाजिक जनजागृती मोहिमा राबवणे.\n"
            "• समाजकल्याण आणि जनहितकारी उपक्रमांचे आयोजन करणे.\n\n"
            "या उपक्रमांच्या माध्यमातून स्वयंसेवक फाउंडेशन समाजात मानवता पसरवून लोकांच्या "
            "चेहऱ्यावर हास्य फुलवण्याचा आणि सकारात्मक बदल घडवण्याचा निरंतर प्रयत्न करते.\n\n"
            "आमचा विश्वास: मानवता हीच खरी सेवा आहे."
        )
        setting.vision_text = (
            "Our vision is to build a compassionate and hunger-free society where no one sleeps hungry, "
            "everyone lives with dignity, and every individual has the opportunity to lead a better life.\n\n"
            "We aspire to create a positive impact through hunger relief, education, healthcare, "
            "environmental protection, and community welfare. We envision a society where people support "
            "one another, celebrate happiness together, and work towards a better future for all."
        )
        setting.vision_text_mr = (
            "एक दयाळू, संवेदनशील आणि भूकमुक्त समाज निर्माण करणे जिथे कोणीही उपाशी झोपणार नाही, "
            "प्रत्येकजण सन्मानाने जगेल आणि प्रत्येकाला उत्तम जीवन जगण्याची संधी लाभेल, हे आमचे स्वप्न आहे.\n\n"
            "अन्नदान, शिक्षण, आरोग्यसेवा, पर्यावरण संरक्षण आणि समाजकल्याण यांच्या माध्यमातून "
            "सकारात्मक प्रभाव निर्माण करण्याची आमची आकांक्षा आहे. आम्ही अशा समाजाची कल्पना करतो जिथे लोक "
            "एकमेकांना आधार देतील, आनंद एकत्र साजरा करतील आणि सर्वांच्या उज्ज्वल भविष्यासाठी कार्य करतील."
        )
        setting.save()
        self.stdout.write(self.style.SUCCESS("[OK] Foundation settings initialized."))

        # 2. Seven Official Service Areas (Exact 7 from prompt)
        service_areas_data = [
            {
                "title": "Supporting Orphanage Children",
                "title_mr": "अनाथालयातील बालकांना आधार व मदत",
                "slug": "orphanage-children-support",
                "short_description": "Providing compassionate care, nutritional support, clothing, books, and essential items to children residing in orphanages.",
                "short_description_mr": "अनाथालयातील बालकांना मायेची ऊब, पोषण आहार, कपडे, पुस्तके आणि जीवनावश्यक साहित्याचा आधार देणे.",
                "icon_bootstrap": "bi-emoji-smile-fill",
                "order": 1,
            },
            {
                "title": "Serving Senior Citizens in Old-Age Homes",
                "title_mr": "वृद्धाश्रमातील ज्येष्ठ नागरिकांची सेवा",
                "slug": "senior-citizens-old-age-homes",
                "short_description": "Extending emotional companionship, respect, nutritious food, and health assistance to elders living in old-age homes.",
                "short_description_mr": "वृद्धाश्रमात राहणाऱ्या आदरणीय ज्येष्ठ नागरिकांना भावनिक आधार, आदर, सकस आहार आणि आरोग्य साहाय्य पुरवणे.",
                "icon_bootstrap": "bi-people-fill",
                "order": 2,
            },
            {
                "title": "Animal Care & Feeding in Cow Shelters (Gaushalas)",
                "title_mr": "गोशाळांमधील जनावरांना चारा व सेवा",
                "slug": "gaushala-animal-care",
                "short_description": "Providing green fodder, nutritious feed, water facilities, and medical care for cattle and animals in local Gaushalas.",
                "short_description_mr": "गोशाळांमधील मुक्या जनावरांसाठी हिरवा चारा, पौष्टिक खाद्य आणि देखभाल सेवांची व्यवस्था करणे.",
                "icon_bootstrap": "bi-shield-shaded",
                "order": 3,
            },
            {
                "title": "Assisting Needy Patients in Government Hospitals",
                "title_mr": "शासकीय रुग्णालयांतील गरजू रुग्णांना साहाय्य",
                "slug": "government-hospital-patient-support",
                "short_description": "Guiding underprivileged patients, providing essential meal packets to patient attendants, and supporting emergency medical supplies.",
                "short_description_mr": "शासकीय रुग्णालयात उपचारासाठी येणाऱ्या गरजू रुग्णांना आणि त्यांच्या नातेवाईकांना भोजन व औषधोपचारासाठी साहाय्य करणे.",
                "icon_bootstrap": "bi-hospital-fill",
                "order": 4,
            },
            {
                "title": "Blood Donation Drives & Life-Saving Support",
                "title_mr": "रक्तदान शिबिरे व आपत्कालीन मदत",
                "slug": "blood-donation-initiatives",
                "short_description": "Organizing voluntary blood donation camps and maintaining an active volunteer donor network to save lives in critical emergencies.",
                "short_description_mr": "स्वयंस्फूर्त रक्तदान शिबिरे आयोजित करणे आणि आणीबाणीच्या वेळी रुग्णांचे प्राण वाचवण्यासाठी रक्तदात्यांचे जाळे सक्रिय ठेवणे.",
                "icon_bootstrap": "bi-droplet-fill",
                "order": 5,
            },
            {
                "title": "Social Awareness Campaigns",
                "title_mr": "सामाजिक जनजागृती मोहिमा",
                "slug": "social-awareness-campaigns",
                "short_description": "Conducting civic cleanliness drives, environmental preservation campaigns, road safety awareness, and youth development outreach.",
                "short_description_mr": "स्वच्छता मोहीम, पर्यावरण संवर्धन, नागरी कर्तव्ये आणि सामाजिक जबाबदारीबद्दल नागरिकांमध्ये जनजागृती निर्माण करणे.",
                "icon_bootstrap": "bi-megaphone-fill",
                "order": 6,
            },
            {
                "title": "Community Welfare & Social Service Activities",
                "title_mr": "समाजकल्याण व लोकहितकारी उपक्रम",
                "slug": "community-welfare-activities",
                "short_description": "Organizing winter blanket drives for homeless individuals, distributing clothes and sweets during festivals, and grassroots relief.",
                "short_description_mr": "रस्त्यावरील बेघर व्यक्तींसाठी हिवाळी ब्लँकेट वाटप, सणासुदीला अन्न-वस्त्र वाटप आणि सर्वसमावेशक समाजकल्याण कार्य.",
                "icon_bootstrap": "bi-globe-central-south",
                "order": 7,
            },
        ]

        service_area_map = {}
        for area_info in service_areas_data:
            area, _ = ServiceArea.objects.update_or_create(
                slug=area_info['slug'],
                defaults=area_info
            )
            service_area_map[area_info['slug']] = area

        self.stdout.write(self.style.SUCCESS("[OK] 7 Key Service Areas initialized."))

        # 3. The 11 Official Activity Categories
        categories_data = [
            {
                "order": 1,
                "name": "Food Donation",
                "name_mr": "अन्नदान",
                "slug": "food-donation",
                "icon_bootstrap": "bi-egg-fried",
                "description": "Weekly food distribution, hunger relief drives for the needy, homeless, and underprivileged.",
                "description_mr": "गरजू, बेघर आणि वंचित घटकांसाठी साप्ताहिक अन्नदान व भूकमुक्ती उपक्रम.",
            },
            {
                "order": 2,
                "name": "Clothes Donation",
                "name_mr": "वस्त्रदान",
                "slug": "clothes-donation",
                "icon_bootstrap": "bi-bag-heart-fill",
                "description": "Distributing clean clothing, winter warm wear, and essentials to families and homeless people.",
                "description_mr": "गरजू कुटुंबे आणि रस्त्यांवरील बेघरांना कपडे व उबदार साहित्याचे वाटप.",
            },
            {
                "order": 3,
                "name": "Blood Donation Camp",
                "name_mr": "रक्तदान शिबिर",
                "slug": "blood-donation-camp",
                "icon_bootstrap": "bi-droplet-fill",
                "description": "Organizing voluntary blood donation drives in coordination with government hospitals to save lives.",
                "description_mr": "जीवन वाचवण्यासाठी शासकीय रुग्णालयांच्या सहकार्याने आयोजित स्वयंस्फूर्त रक्तदान शिबिरे.",
            },
            {
                "order": 4,
                "name": "Health Checkup Camp",
                "name_mr": "आरोग्य तपासणी शिबिर",
                "slug": "health-checkup-camp",
                "icon_bootstrap": "bi-heart-pulse-fill",
                "description": "Free general health screenings, basic diagnostic checkups, and medical consultations.",
                "description_mr": "गरजूंसाठी मोफत आरोग्य तपासणी, मूलभूत निदान आणि वैद्यकीय सल्ला शिबिरे.",
            },
            {
                "order": 5,
                "name": "Vruddhashram Visits",
                "name_mr": "वृद्धाश्रम भेट व सेवा",
                "slug": "vruddhashram-visits",
                "icon_bootstrap": "bi-person-heart",
                "description": "Spending quality time, serving meals, and offering emotional warmth and care to senior citizens in old-age homes.",
                "description_mr": "वृद्धाश्रमातील ज्येष्ठ नागरिकांना मायेची ऊब देणे, संवाद साधणे आणि भोजन सेवा पुरवणे.",
            },
            {
                "order": 6,
                "name": "Anathashram Visits",
                "name_mr": "अनाथालय भेट व मदत",
                "slug": "anathashram-visits",
                "icon_bootstrap": "bi-people-fill",
                "description": "Extending care, nutritional meals, stationery, festival sweets, and companionship to children in orphanages.",
                "description_mr": "अनाथालयातील बालकांना शैक्षणिक साहित्य, पोषण आहार आणि सणांचे आनंदक्षण देणे.",
            },
            {
                "order": 7,
                "name": "Cleanliness Drives",
                "name_mr": "स्वच्छता मोहीम",
                "slug": "cleanliness-drives",
                "icon_bootstrap": "bi-trash3-fill",
                "description": "Promoting public hygiene and Swachh Bharat community sanitation drives across public spots and parks.",
                "description_mr": "सार्वजनिक ठिकाणी स्वच्छता, परिसर स्वच्छता आणि नागरिकांमध्ये स्वच्छतेचा संदेश रुजवणे.",
            },
            {
                "order": 8,
                "name": "Environment & Tree Plantation",
                "name_mr": "पर्यावरण व वृक्षारोपण",
                "slug": "environment-tree-plantation",
                "icon_bootstrap": "bi-tree-fill",
                "description": "Planting native trees, protecting green cover, and environmental protection campaigns in Chhatrapati Sambhajinagar.",
                "description_mr": "झाडे लावणे, संवर्धन करणे आणि पर्यावरण संरक्षणासाठी जनजागृती करणे.",
            },
            {
                "order": 9,
                "name": "Children's Activities",
                "name_mr": "बालकांसाठी उपक्रम",
                "slug": "childrens-activities",
                "icon_bootstrap": "bi-emoji-smile-fill",
                "description": "Educational workshops, creative drawing sessions, book distributions, and joy activities for underprivileged kids.",
                "description_mr": "वंचित बालकांसाठी शैक्षणिक मार्गदर्शन, चित्रकला, दप्तर-पुस्तके वाटप आणि आनंददायी उपक्रम.",
            },
            {
                "order": 10,
                "name": "Awareness Campaigns",
                "name_mr": "सामाजिक जनजागृती",
                "slug": "awareness-campaigns",
                "icon_bootstrap": "bi-megaphone-fill",
                "description": "Educating citizens on health, organ/blood donation, safety, social harmony, and civic compassion.",
                "description_mr": "आरोग्य, रक्तदान, सामाजिक एकता आणि जबाबदार नागरिकत्वाबाबत प्रबोधन मोहिमा.",
            },
            {
                "order": 11,
                "name": "Other Social Service Activities",
                "name_mr": "इतर समाजसेवा उपक्रम",
                "slug": "other-social-service-activities",
                "icon_bootstrap": "bi-globe2",
                "description": "Winter blanket distributions, cow shelter (Gaushala) feed assistance, hospital patient assistance, and festival celebrations.",
                "description_mr": "हिवाळी ब्लँकेट वाटप, गोशाळा चारा सेवा, रुग्ण साहाय्य आणि विशेष सणोत्सव सेवा उपक्रम.",
            },
        ]

        category_map = {}
        for cat_info in categories_data:
            cat, _ = ActivityCategory.objects.update_or_create(
                slug=cat_info['slug'],
                defaults=cat_info
            )
            category_map[cat_info['slug']] = cat

        self.stdout.write(self.style.SUCCESS("[OK] 11 Activity Categories initialized."))

        # 4. Official Regular Activities
        activities_data = [
            {
                "title": "Every Sunday Food Distribution Drive",
                "title_mr": "दर रविवारी अन्नदान उपक्रम",
                "slug": "sunday-food-distribution-drive",
                "service_slug": "community-welfare-activities",
                "schedule_frequency": "Every Sunday Morning & Afternoon",
                "schedule_frequency_mr": "दर रविवारी सकाळी व दुपारी",
                "description": (
                    "Every Sunday, our members come together to distribute freshly cooked, nutritious food among "
                    "underprivileged people, children in orphanages, elderly people, and homeless individuals "
                    "across Chhatrapati Sambhajinagar."
                ),
                "description_mr": (
                    "दर रविवारी आमचे स्वयंसेवक एकत्र येऊन छत्रपती संभाजीनगरमधील गरजू व्यक्ती, अनाथालयातील बालके, "
                    "वृद्धाश्रमातील ज्येष्ठ आणि रस्त्यावरील बेघर लोकांना सकस व ताजे अन्न वाटप करतात."
                ),
                "status": "regular",
                "order": 1,
            },
            {
                "title": "Winter Blanket Distribution for Homeless Individuals",
                "title_mr": "बेघर निराधारांसाठी हिवाळी ब्लँकेट वाटप मोहीम",
                "slug": "winter-blanket-distribution",
                "service_slug": "community-welfare-activities",
                "schedule_frequency": "Seasonal Winter Drive (Annual)",
                "schedule_frequency_mr": "दर हिवाळ्यात वार्षिक मोहीम",
                "description": (
                    "During chilly winter nights, foundation volunteers traverse streets, railway station areas, "
                    "bus stands, and flyovers to distribute warm blankets directly to individuals sleeping exposed to the cold."
                ),
                "description_mr": (
                    "कडाक्याच्या थंडीत रस्त्यांच्या कडेला, बसस्थानक आणि रेल्वे स्थानक परिसरात झोपणाऱ्या बेघर व्यक्तींना "
                    "थंडीपासून संरक्षणासाठी थेट उबदार ब्लँकेट्सचे वाटप केले जाते."
                ),
                "status": "seasonal",
                "order": 2,
            },
            {
                "title": "Voluntary Blood Donation & Health Support Camps",
                "title_mr": "स्वयंस्फूर्त रक्तदान व आरोग्य साहाय्य शिबिरे",
                "slug": "blood-donation-health-camps",
                "service_slug": "blood-donation-initiatives",
                "schedule_frequency": "Regular Scheduled Drives",
                "schedule_frequency_mr": "नियमित नियोजित शिबिरे",
                "description": (
                    "Organizing voluntary blood donation camps in collaboration with government hospital blood banks "
                    "to support patients undergoing surgeries, trauma care, and severe illness."
                ),
                "description_mr": (
                    "शासकीय रुग्णालयांमधील गरजू रुग्णांना वेळेवर रक्त मिळावे म्हणून स्वयंसेवक फाउंडेशनतर्फे नियमित "
                    "रक्तदान शिबिरे आयोजित केली जातात."
                ),
                "status": "regular",
                "order": 3,
            },
            {
                "title": "Cleanliness & Environmental Awareness Drives",
                "title_mr": "स्वच्छता मोहीम आणि पर्यावरण जनजागृती",
                "slug": "cleanliness-environmental-drives",
                "service_slug": "social-awareness-campaigns",
                "schedule_frequency": "Periodic Community Drives",
                "schedule_frequency_mr": "नियतकालिक सामाजिक मोहीम",
                "description": (
                    "Foundation teams mobilize young volunteers for public cleanliness drives in public spaces, "
                    "promoting waste segregation, hygiene awareness, and civic duty."
                ),
                "description_mr": (
                    "सार्वजनिक ठिकाणांची स्वच्छता, कचरा व्यवस्थापन आणि आरोग्याविषयी जनजागृतीसाठी तरुण स्वयंसेवकांना "
                    "एकत्रित करून स्वच्छता मोहीम राबवली जाते."
                ),
                "status": "regular",
                "order": 4,
            },
            {
                "title": "Festival & Birthday Celebrations with Orphanage Children",
                "title_mr": "अनाथालयातील बालकांसोबत सण आणि वाढदिवस साजरा करणे",
                "slug": "festival-celebrations-with-children",
                "service_slug": "orphanage-children-support",
                "schedule_frequency": "Festivals & Special Occasions",
                "schedule_frequency_mr": "सण, वाढदिवस व विशेष प्रसंग",
                "description": (
                    "Sharing joy, festival sweets, new clothes, stationary kits, and thoughtful gifts with "
                    "underprivileged children and orphans to ensure everyone experiences happiness during celebrations."
                ),
                "description_mr": (
                    "दिवाळी, सण, तसेच वाढदिवसाचे औचित्य साधून अनाथालयातील बालकांना खाऊ, नवीन कपडे, शैक्षणिक साहित्य "
                    "आणि भेटवस्तू देऊन त्यांच्या चेहऱ्यावर हास्य फुलवले जाते."
                ),
                "status": "regular",
                "order": 5,
            },
            {
                "title": "Fodder & Care Drive at Local Gaushalas",
                "title_mr": "स्थानिक गोशाळांमध्ये चारा व देखभाल सेवा",
                "slug": "gaushala-feed-and-care-drive",
                "service_slug": "gaushala-animal-care",
                "schedule_frequency": "Regular Monthly Service",
                "schedule_frequency_mr": "नियमित मासिक सेवा",
                "description": (
                    "Delivering fresh green fodder, dry feed, and water trough assistance to sheltered cattle in "
                    "Chhatrapati Sambhajinagar cow shelters."
                ),
                "description_mr": (
                    "छत्रपती संभाजीनगर परिसरातील गोशाळांमधील जनावरांसाठी हिरवा चारा, ढेप आणि पिण्याच्या पाण्याची "
                    "व्यवस्था करण्यात स्वयंसेवक सक्रिय सहभाग घेतात."
                ),
                "status": "regular",
                "order": 6,
            },
        ]

        activity_category_map = {
            "sunday-food-distribution-drive": "food-donation",
            "winter-blanket-distribution": "clothes-donation",
            "blood-donation-health-camps": "blood-donation-camp",
            "cleanliness-hygiene-drives": "cleanliness-drives",
            "festival-celebrations-with-children": "childrens-activities",
            "gaushala-feed-and-care-drive": "other-social-service-activities",
        }

        for act_info in activities_data:
            s_slug = act_info.pop('service_slug')
            act_info['service_area'] = service_area_map.get(s_slug)
            c_slug = activity_category_map.get(act_info['slug'], 'other-social-service-activities')
            act_info['category'] = category_map.get(c_slug)
            act_info['is_published'] = True
            act_info['venue'] = "TV Center, Chhatrapati Sambhajinagar"
            Activity.objects.update_or_create(
                slug=act_info['slug'],
                defaults=act_info
            )

        self.stdout.write(self.style.SUCCESS("[OK] Official Regular Activities initialized."))

        # 4. Official Gallery Items with Labeled Placeholders
        gallery_data = [
            {
                "title": "Sunday Food Distribution Drive",
                "title_mr": "रविवार अन्नदान उपक्रम",
                "caption": "Volunteers distributing warm meals to needy individuals across TV Center and city spots.",
                "caption_mr": "टीव्ही सेंटर व शहर परिसरातील गरजू नागरिकांना अन्नवाटप करताना स्वयंसेवक.",
                "service_slug": "community-welfare-activities",
                "order": 1,
            },
            {
                "title": "Orphanage Children Care & Gifting",
                "title_mr": "अनाथालय बालकांसाठी खाऊ व शैक्षणिक साहित्य वाटप",
                "caption": "Sharing smiles, educational stationery, and sweets with children.",
                "caption_mr": "मुलांसोबत आनंद वाटताना, शैक्षणिक साहित्य व मिठाईचे वाटप.",
                "service_slug": "orphanage-children-support",
                "order": 2,
            },
            {
                "title": "Winter Blanket Distribution at Night",
                "title_mr": "रात्रीच्या वेळी उबदार ब्लँकेट्सचे वाटप",
                "caption": "Reaching out to street sleepers during cold winter nights.",
                "caption_mr": "कडाक्याच्या थंडीत रस्त्यावर झोपणाऱ्या बांधवांना पांघरुणे वाटप.",
                "service_slug": "community-welfare-activities",
                "order": 3,
            },
            {
                "title": "Voluntary Blood Donation Camp",
                "title_mr": "स्वयंस्फूर्त रक्तदान शिबिर",
                "caption": "Life-saving blood donation initiative supporting government hospitals.",
                "caption_mr": "शासकीय रुग्णालयांतील रुग्णांच्या मदतीसाठी जीवनदायी रक्तदान शिबिर.",
                "service_slug": "blood-donation-initiatives",
                "order": 4,
            },
            {
                "title": "Cleanliness Drive in Public Areas",
                "title_mr": "सार्वजनिक ठिकाणी स्वच्छता मोहीम",
                "caption": "Youth volunteers actively participating in Swachhata service.",
                "caption_mr": "स्वच्छता अभियानात उत्साहाने सहभागी झालेले युवा स्वयंसेवक.",
                "service_slug": "social-awareness-campaigns",
                "order": 5,
            },
            {
                "title": "Gaushala Fodder Distribution",
                "title_mr": "गोशाळेत हिरवा चारा वाटप",
                "caption": "Serving mute animals with fresh green fodder and care.",
                "caption_mr": "गोशाळेतील जनावरांसाठी चारा आणि प्रेमाने केलेली सेवा.",
                "service_slug": "gaushala-animal-care",
                "order": 6,
            },
        ]

        for g in gallery_data:
            s_slug = g.pop('service_slug')
            GalleryItem.objects.update_or_create(
                title=g['title'],
                defaults={
                    'title_mr': g['title_mr'],
                    'caption': g['caption'],
                    'caption_mr': g['caption_mr'],
                    'service_area': service_area_map.get(s_slug),
                    'placeholder_label': "Authentic Foundation Activity Photo Placeholder",
                    'is_featured': True,
                    'order': g['order'],
                }
            )

        self.stdout.write(self.style.SUCCESS("[OK] Gallery items initialized with authentic placeholders."))

        # 5. Accounts: Admin, Coordinator, and Volunteer
        # Admin
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'swayamsevakfoundation24@gmail.com', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('admin123')
        admin_user.save()
        admin_profile = UserProfile.get_profile_for_user(admin_user)
        admin_profile.role = 'admin'
        admin_profile.status = 'approved'
        admin_profile.phone = '9852827771'
        admin_profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Administrator account initialized (admin / admin123)."))

        # Coordinator
        coord_user, _ = User.objects.get_or_create(
            username='coordinator',
            defaults={'email': 'coordinator@swayamsevak.org', 'first_name': 'Ramesh', 'last_name': 'Kulkarni'}
        )
        coord_user.set_password('coord123')
        coord_user.save()
        coord_profile = UserProfile.get_profile_for_user(coord_user)
        coord_profile.role = 'coordinator'
        coord_profile.status = 'approved'
        coord_profile.phone = '9852827772'
        coord_profile.city = 'Chhatrapati Sambhajinagar'
        coord_profile.save()
        # Assign coordinator to activities
        sunday_act = Activity.objects.filter(slug='sunday-food-distribution-drive').first()
        if sunday_act:
            coord_profile.assigned_activities.add(sunday_act)
        blanket_act = Activity.objects.filter(slug='winter-blanket-distribution').first()
        if blanket_act:
            coord_profile.assigned_activities.add(blanket_act)
        self.stdout.write(self.style.SUCCESS("[OK] Coordinator account initialized (coordinator / coord123)."))

        # Active Volunteer
        vol_user, _ = User.objects.get_or_create(
            username='volunteer',
            defaults={'email': 'volunteer@swayamsevak.org', 'first_name': 'Pooja', 'last_name': 'Deshmukh'}
        )
        vol_user.set_password('vol123')
        vol_user.save()
        vol_profile = UserProfile.get_profile_for_user(vol_user)
        vol_profile.role = 'volunteer'
        vol_profile.status = 'approved'
        vol_profile.phone = '9852827773'
        vol_profile.city = 'CIDCO, Chhatrapati Sambhajinagar'
        vol_profile.blood_group = 'O+'
        vol_profile.availability = 'every_sunday'
        vol_profile.interests = 'Food distribution and children education support'
        vol_profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Approved Volunteer account initialized (volunteer / vol123)."))

        # Pending Volunteer (for admin review testing)
        pending_user, _ = User.objects.get_or_create(
            username='rahul_new',
            defaults={'email': 'rahul.new@example.com', 'first_name': 'Rahul', 'last_name': 'Jadhav'}
        )
        pending_user.set_password('rahul123')
        pending_user.save()
        pending_profile = UserProfile.get_profile_for_user(pending_user)
        pending_profile.role = 'volunteer'
        pending_profile.status = 'pending'
        pending_profile.phone = '9852827774'
        pending_profile.city = 'TV Center, Chhatrapati Sambhajinagar'
        pending_profile.blood_group = 'B+'
        pending_profile.availability = 'every_sunday'
        pending_profile.interests = 'Sunday food drives and cleanliness campaigns'
        pending_profile.save()
        self.stdout.write(self.style.SUCCESS("[OK] Pending Volunteer account initialized (rahul_new / rahul123)."))

        # 6. Events
        from datetime import date, timedelta
        next_sunday = date.today() + timedelta(days=(6 - date.today().weekday()) % 7 or 7)
        following_sunday = next_sunday + timedelta(days=7)

        from core.models import Event, EventRegistration, Announcement

        event1, _ = Event.objects.update_or_create(
            slug='sunday-food-drive-tv-center',
            defaults={
                'title': 'Sunday Food Distribution Drive – TV Center',
                'title_mr': 'रविवार अन्नदान उपक्रम – टीव्ही सेंटर परिसर',
                'activity': sunday_act,
                'service_area': sunday_act.service_area if sunday_act else None,
                'coordinator': coord_user,
                'event_date': next_sunday,
                'start_time': '09:30:00',
                'end_time': '13:00:00',
                'location': 'TV Center Shivaji Chowk, Chhatrapati Sambhajinagar',
                'description': 'Gathering at TV Center to package and distribute fresh hot meals to needy individuals, orphanages, and street dwellers.',
                'description_mr': 'गरजू व्यक्ती आणि अनाथालयातील बालकांना सकस अन्नवाटप करण्यासाठी स्वयंसेवकांचा एकत्र येण्याचा उपक्रम.',
                'max_volunteers': 30,
                'status': 'upcoming'
            }
        )

        event2, _ = Event.objects.update_or_create(
            slug='winter-blanket-night-drive-railway-station',
            defaults={
                'title': 'Winter Warmth Blanket Night Drive',
                'title_mr': 'हिवाळी उबदार ब्लँकेट रात्रीचे वाटप',
                'activity': blanket_act,
                'service_area': blanket_act.service_area if blanket_act else None,
                'coordinator': coord_user,
                'event_date': following_sunday,
                'start_time': '20:30:00',
                'end_time': '23:30:00',
                'location': 'Railway Station & Bus Stand Areas, Chhatrapati Sambhajinagar',
                'description': 'Night drive distributing warm winter blankets directly to homeless people sleeping exposed to chilly conditions.',
                'description_mr': 'कडाक्याच्या थंडीत रस्त्यावर झोपणाऱ्या बेघर नागरिकांना उबदार ब्लँकेट्सचे थेट वाटप.',
                'max_volunteers': 20,
                'status': 'upcoming'
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Foundation Events initialized."))

        # 7. Sample Event Registration
        reg, _ = EventRegistration.objects.update_or_create(
            event=event1,
            volunteer=vol_user,
            defaults={'status': 'registered', 'volunteer_notes': 'Available with vehicle if transport is required.'}
        )
        self.stdout.write(self.style.SUCCESS("[OK] Sample Event Registration linked."))

        # 8. Announcements
        Announcement.objects.update_or_create(
            title="Sunday Drive Assembly Instructions",
            defaults={
                'title_mr': "रविवार अन्नदान मोहिमेसाठी उपस्थिती सूचना",
                'content': "All registered volunteers are requested to assemble at TV Center sharp at 09:15 AM. Wear comfortable attire and carry your water bottles.",
                'content_mr': "सर्व नोंदणीकृत स्वयंसेवकांनी सकाळी ९:१५ वाजता टीव्ही सेंटर येथे वेळेवर उपस्थित राहावे.",
                'target_role': 'volunteer',
                'priority': 'normal',
                'event': event1,
                'is_active': True,
                'created_by': admin_user
            }
        )
        Announcement.objects.update_or_create(
            title="Coordinator Briefing on Winter Drive Logistics",
            defaults={
                'title_mr': "हिवाळी मोहिमेबाबत समन्वयकांची पूर्वतयारी",
                'content': "Please verify blanket stock inventory and route checkpoints before Friday evening.",
                'target_role': 'coordinator',
                'priority': 'high',
                'event': event2,
                'is_active': True,
                'created_by': admin_user
            }
        )
        self.stdout.write(self.style.SUCCESS("[OK] Announcements initialized."))

        self.stdout.write(self.style.SUCCESS("==> All foundation roles, events, and records successfully seeded!"))
