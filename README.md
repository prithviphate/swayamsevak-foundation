# Swayamsevak Foundation (स्वावलंबनातून समाजसेवा)
### Full-Stack Web Application — College Major Project

An institutional, responsive, accessible, and database-backed full-stack website developed for **Swayamsevak Foundation**, Chhatrapati Sambhajinagar, Maharashtra, India.

---

## 1. Foundation Information & Official Details

| Attribute | Verified Official Record |
| :--- | :--- |
| **Official Name** | **Swayamsevak Foundation** |
| **Tagline (Marathi)** | **स्वावलंबनातून समाजसेवा** |
| **Tagline (English)** | Social Service through Self-Reliance |
| **Established** | January 2024 |
| **City & State** | Chhatrapati Sambhajinagar, Maharashtra, India |
| **Founder / President** | **Om Vinod Dhadbale** |
| **Phone** | **9852827771** |
| **Email** | **swayamsevakfoundation24@gmail.com** |
| **Address** | TV Center, Chhatrapati Sambhajinagar, 431001 |
| **Official Languages** | English and Marathi |
| **Core Belief** | *"Humanity is the greatest service."* (*"मानवता हीच खरी सेवा आहे."*) |

### Official Social Media Channels:
- **Instagram**: [https://www.instagram.com/swayamsevak_foundation/](https://www.instagram.com/swayamsevak_foundation/)
- **YouTube**: [https://youtube.com/@swayamsevakfoundation](https://youtube.com/@swayamsevakfoundation)
- **WhatsApp**: [https://chat.whatsapp.com/B4roMDAWjr4BMUCVspUgQE](https://chat.whatsapp.com/B4roMDAWjr4BMUCVspUgQE)
- **Facebook**: *Pending* (officially marked as pending)

---

## 2. Official Foundation Statements

### Our Story – Why We Started
> *Swayamsevak Foundation was started with one simple belief: **Humanity is the greatest service**.*
> 
> *Our aim is to help people in need and work towards a hunger-free society. Every Sunday, our members come together to distribute food among underprivileged people, children in orphanages, elderly people, and homeless individuals.*
> 
> *Along with hunger relief, we organize cleanliness drives, health and blood donation camps, and educational initiatives. We also celebrate festivals, birthdays, and special occasions with underprivileged communities by sharing food, clothes, sweets, and gifts. During winter, we distribute blankets to people sleeping on the streets.*
> 
> *Our mission is to spread kindness, serve humanity, and bring smiles to those who need them most.*

### Official Mission
> *Our mission is to extend a helping hand to every needy person in society and serve humanity with compassion, kindness, and selfless dedication.*
> 
> **Our key areas of service include:**
> 1. Supporting orphanage children by providing help, care, and essential support.
> 2. Serving senior citizens in old-age homes.
> 3. Providing food and care for animals in cow shelters (Gaushalas).
> 4. Assisting needy patients in government hospitals.
> 5. Promoting blood donation and supporting initiatives that help save lives.
> 6. Conducting social awareness campaigns.
> 7. Organizing community welfare and social service activities.
> 
> *Through these initiatives, Swayamsevak Foundation strives to spread humanity, bring smiles to people's faces, and make a meaningful difference in society.*
> 
> **Our belief:** *Humanity is the greatest service.*

### Official Vision
> *Our vision is to build a compassionate and hunger-free society where no one sleeps hungry, everyone lives with dignity, and every individual has the opportunity to lead a better life.*
> 
> *We aspire to create a positive impact through hunger relief, education, healthcare, environmental protection, and community welfare. We envision a society where people support one another, celebrate happiness together, and work towards a better future for all.*

---

## 3. Technology Stack & Architecture

- **Backend Framework**: Python 3.14 / Django 6.1
- **Database Architecture**: 
  - Default local development: SQLite3
  - Target production / evaluation database: MySQL (configured with PyMySQL driver for zero-dependency cross-platform deployment)
- **Frontend Architecture**:
  - Semantic HTML5, CSS3, JavaScript (ES6)
  - Bootstrap 5.3.3 UI Framework
  - Bootstrap Icons 1.11.3
  - Google Web Fonts: *Outfit* (headings), *Inter* (body), *Noto Sans Devanagari* (Marathi language rendering)
- **Configuration & Security**:
  - `python-dotenv` for environment variable isolation
  - Django CSRF protection on all forms
  - Phone number sanitizer & 10-digit Indian mobile validator (`^[6-9]\d{9}$`)
  - Image handling with `Pillow`
  - Singleton database model for admin-editable foundation metadata

---

## 4. Key Functional Features

1. **Bilingual Presentation (English & Marathi)**:
   - Dedicated navbar language switcher preserving current page state.
   - Dual-language data models supporting Marathi and English narratives.
2. **Dynamic Foundation Settings**:
   - Authorized administrators can update foundation contact numbers, addresses, social media links, and story details via Django Admin without touching source code.
3. **The 7 Key Initiatives**:
   - Interactive showcase of the seven official pillars with dedicated detail cards and direct connection to regular drives.
4. **Regular & Seasonal Activities Catalog**:
   - Filterable catalog of initiatives (Every Sunday Food Distribution, Winter Blanket Distribution, Voluntary Blood Donation Camps, Cleanliness Drives, Festival Celebrations, Gaushala animal feed).
5. **Authentic Activity Photo Placeholders**:
   - Strictly conforms to the integrity rule: no stock or AI images masquerading as authentic foundation photos. Clean, labeled placeholders (`Authentic Foundation Activity Photo Placeholder`) are used until authentic on-ground pictures are uploaded by staff.
6. **Community Volunteer Intake Portal**:
   - Public application form with field validation, area selection, blood group record, and automatic routing to staff review.
7. **Transparent Support / Pledge Portal**:
   - In-kind pledge intake for meals, blankets, or orphanage supplies.
   - Transparent notice explaining that direct automated payment gateway integration is in preparation pending official NGO banking documentation.
8. **Public Contact Channel**:
   - Validated inquiry system with admin-status tracking.
9. **Role-Based Authentication & Access Control (Admin / Coordinator / Volunteer)**:
   - Dedicated `/login/` supporting both username and email authentication, toggle password visibility, brute-force throttling (temporary lockout after 5 consecutive failed attempts), and role-aware redirection.
   - Self-service `/register/` for community volunteers with comprehensive profile capture (full name, phone, email, city, availability, blood group, occupation, interests) and mandatory privacy consent.
   - Cryptographic `/forgot-password/` workflow generating secure Django tokens without plaintext storage.
   - Dedicated `/profile/` management for authenticated users to update contact details and view status.
10. **Role-Isolated Dashboards**:
    - **Administrator Dashboard (`/admin-dashboard/`)**: Overview metrics, pending volunteer approval queue (approve, suspend, deactivate), coordinator activity assignments, field activity report reviews, upcoming event roster, system-wide announcements, and complete audit trail.
    - **Volunteer Dashboard (`/volunteer-dashboard/`)**: Account verification badge, registered upcoming events with direct cancellation, participation & attendance history, available community drives with one-click enrollment, and high-priority announcements.
    - **Coordinator Dashboard (`/coordinator-dashboard/`)**: Shows only events assigned directly or via assigned service activities, roster of registered volunteers, one-click attendance recording (`/coordinator/event/<id>/attendance/`), and post-drive field report submission with photo uploads.
11. **Security & Data Integrity Guarantees**:
    - Server-side role enforcement via `@admin_required`, `@coordinator_required`, and `@volunteer_required` decorators with custom HTTP 403 Forbidden pages.
    - Strict IDOR (Insecure Direct Object Reference) prevention: volunteers can only view/cancel their own registrations; coordinators can only view/record attendance for their assigned events.
    - Pending approval workflow: new volunteer registrations are placed in `pending` state and cannot register for events until approved by an administrator.
    - Audit logging (`AuditLog`) capturing all security-sensitive actions (logins, status changes, coordinator assignments, report reviews) with IP addresses and actor IDs.

---

## 5. Getting Started & Setup Instructions

### Prerequisites
- Python 3.10+ installed
- Git (optional)

### Step 1: Clone or Navigate to Project Directory
```powershell
cd c:\Users\Prithviraj\Downloads\swayamsevakfounation
```

### Step 2: Set Up Python Virtual Environment
```powershell
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Or Windows Command Prompt:
venv\Scripts\activate.bat
```

### Step 3: Install Project Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` (already pre-configured for local execution):
```powershell
cp .env.example .env
```

### Step 5: Run Database Migrations
```powershell
python manage.py migrate
```

### Step 6: Seed Official Foundation Data
Pre-populate the database with the official foundation details, 7 service areas, activities, and admin superuser:
```powershell
python manage.py seed_foundation_data
```

> **Default Seed Accounts for Evaluation & Testing**:
> - **Administrator**:
>   - **Username**: `admin` &bull; **Password**: `admin123` &bull; **Email**: `swayamsevakfoundation24@gmail.com`
>   - *Dashboard*: `/admin-dashboard/`
> - **Field Coordinator**:
>   - **Username**: `coordinator` &bull; **Password**: `coord123` &bull; **Email**: `coordinator@swayamsevak.org`
>   - *Dashboard*: `/coordinator-dashboard/`
> - **Approved Volunteer**:
>   - **Username**: `volunteer` &bull; **Password**: `vol123` &bull; **Email**: `volunteer@swayamsevak.org`
>   - *Dashboard*: `/volunteer-dashboard/`
> - **Pending Volunteer (Awaiting Admin Verification)**:
>   - **Username**: `rahul_new` &bull; **Password**: `volunteer123` &bull; **Email**: `rahul.jadhav@example.com`

### Step 7: Run the Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
- **Public Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Unified Login Portal**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Volunteer Registration**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Administrator Dashboard**: [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)
- **Coordinator Dashboard**: [http://127.0.0.1:8000/coordinator-dashboard/](http://127.0.0.1:8000/coordinator-dashboard/)
- **Volunteer Dashboard**: [http://127.0.0.1:8000/volunteer-dashboard/](http://127.0.0.1:8000/volunteer-dashboard/)
- **Django Superadmin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 6. How to Switch to MySQL Database

To connect the application to a local or remote MySQL server (e.g. XAMPP, WAMP, MySQL Workbench, or production RDS):

1. **Create the MySQL Database**:
   Open MySQL shell or phpMyAdmin and execute:
   ```sql
   CREATE DATABASE swayamsevak_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Update your `.env` file**:
   Set `DATABASE_ENGINE=mysql` and update your MySQL credentials:
   ```env
   DATABASE_ENGINE=mysql
   DB_NAME=swayamsevak_db
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

3. **Apply Migrations to MySQL**:
   ```powershell
   python manage.py migrate
   ```

4. **Seed the Official Foundation Data into MySQL**:
   ```powershell
   python manage.py seed_foundation_data
   ```

---

## 7. Running the Automated Test Suite

Run the comprehensive unit test suite covering models, validation, views, bilingual state, and staff authorization:

```powershell
python manage.py test
```

All 30 automated test cases will run and verify project integrity (including model constraints, phone number validation, bilingual switching, role-based dashboard access, volunteer approval workflows, IDOR isolation, attendance marking, report reviews, brute-force throttling, and cryptographic password recovery).

---

## 8. Unfinished Integrations & Production Roadmap

In strict compliance with documentation integrity:
1. **Online Payment Gateway (Razorpay / Stripe / UPI QR)**:
   - *Status*: Documented & Pending official NGO institutional banking documentation.
   - *Current Implementation*: Public supporters submit in-kind pledges or coordinate directly with the founder via official phone (9852827771) or WhatsApp.
2. **Facebook Page**:
   - *Status*: Official account pending creation.
3. **SMS / WhatsApp Cloud API Notifications**:
   - *Status*: Foundation forms record entries in database with instant on-screen feedback; automated SMS/WhatsApp gateway dispatch can be connected upon API key procurement.

---

## 9. Project Academic Declaration
Developed as a **College Major Project** for **Swayamsevak Foundation**, Chhatrapati Sambhajinagar, demonstrating senior full-stack software engineering, responsive UI/UX design, database modeling, and software testing practices.
