# Ngangi Platform - Project Structure

## Overview
Complete Django-based online platform for managing community savings groups (ngangi) with all requested features.

## Project Structure

### Core Django Project
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `README.md` - Complete setup and usage guide
- `.gitignore` - Git ignore rules
- `setup.py` - Setup automation script

### Main Project Configuration (`ngangi_platform/`)
- `settings.py` - Django settings with all apps configured
- `urls.py` - Main URL routing
- `wsgi.py` / `asgi.py` - WSGI/ASGI configuration

### Applications

#### 1. Members App (`members/`)
**Features:**
- Member registration and management
- Role-based access (Leader, Treasurer, Secretary, Member)
- Member profiles with contact information
- Profile pictures support
- Account balance tracking methods

**Files:**
- `models.py` - Member model with role management
- `views.py` - Member CRUD operations
- `forms.py` - Member registration and editing forms
- `urls.py` - Member URL routing
- `admin.py` - Django admin configuration

#### 2. Contributions App (`contributions/`)
**Features:**
- Record member contributions (date, amount, description)
- Withdrawal requests with approval workflow
- Transaction logging for audit trail
- Account balance calculation
- Transaction history

**Files:**
- `models.py` - Contribution, Withdrawal, TransactionLog models
- `views.py` - Contribution and withdrawal management
- `forms.py` - Contribution and withdrawal forms
- `urls.py` - Contribution URL routing
- `admin.py` - Django admin configuration

#### 3. Meetings App (`meetings/`)
**Features:**
- Schedule meetings with date, time, location
- Agenda and minutes management
- Attendance tracking
- Bulk attendance recording
- Meeting completion status

**Files:**
- `models.py` - Meeting and Attendance models
- `views.py` - Meeting management and attendance recording
- `forms.py` - Meeting and attendance forms
- `urls.py` - Meeting URL routing
- `admin.py` - Django admin configuration

#### 4. Announcements App (`announcements/`)
**Features:**
- Priority-based announcements (Low, Normal, High, Urgent)
- Pinned announcements
- Expiration dates
- Community updates feed
- Meeting summaries integration

**Files:**
- `models.py` - Announcement and CommunityUpdate models
- `views.py` - Announcement and update management
- `forms.py` - Announcement and update forms
- `urls.py` - Announcement URL routing
- `admin.py` - Django admin configuration

#### 5. Loans App (`loans/`)
**Features:**
- Loan requests with purpose and interest rates
- Loan approval workflow (Pending, Approved, Active, Completed, Rejected, Defaulted)
- Loan repayment tracking
- Balance validation
- Loan status management

**Files:**
- `models.py` - Loan and LoanRepayment models
- `views.py` - Loan management and repayment
- `forms.py` - Loan and repayment forms
- `urls.py` - Loan URL routing
- `admin.py` - Django admin configuration

#### 6. Dashboard App (`dashboard/`)
**Features:**
- Admin dashboard with overview statistics
- Member dashboard for individual members
- Total savings, contributions, and loans tracking
- Upcoming meetings display
- Pending approvals summary
- Recent transactions
- Exportable reports (Excel format)

**Files:**
- `views.py` - Dashboard views for admin and members
- `reports.py` - Excel report generation functions
- `urls.py` - Dashboard URL routing

### Templates (`templates/`)
- `base.html` - Base template with mobile-responsive Bootstrap 5 design
- `registration/login.html` - Login page
- `dashboard/index.html` - Main dashboard

### Static Files (`static/`)
- Directory for static files (CSS, JS, images)
- Bootstrap 5 CDN integration
- Custom CSS for mobile optimization
- Offline detection indicator

### Media Files (`media/`)
- Directory for user-uploaded files (profile pictures, etc.)

## Key Features Implemented

### ✅ Core Modules
1. **Member Management** - Complete CRUD with role-based access
2. **Savings/Contributions** - Recording, tracking, and balance calculation
3. **Meeting Management** - Scheduling, agenda, minutes, attendance
4. **Updates/Announcements** - News feed with priority and expiration

### ✅ Additional Features
5. **Dashboard/Admin View** - Overview with statistics and pending approvals
6. **Loans/Withdrawals** - Complete loan management and withdrawal approval
7. **Security & Transparency** - Transaction logs, role-based access, exportable reports
8. **Mobile/Access** - Responsive design, offline detection, mobile-friendly UI

## Security Features
- Role-based access control (Leader, Treasurer, Secretary, Member)
- Transaction logging for all financial operations
- Admin-only access for sensitive operations
- Session management
- CSRF protection
- Password validation

## Database Models
- **Member** - User profiles with roles
- **Contribution** - Savings/contributions records
- **Withdrawal** - Withdrawal requests with approval
- **TransactionLog** - Audit trail for all transactions
- **Meeting** - Meeting scheduling and management
- **Attendance** - Meeting attendance tracking
- **Announcement** - Community announcements
- **CommunityUpdate** - General updates and summaries
- **Loan** - Loan requests and management
- **LoanRepayment** - Loan repayment tracking

## URL Patterns
- `/` - Dashboard
- `/members/` - Member management
- `/contributions/` - Contributions and withdrawals
- `/meetings/` - Meeting management
- `/announcements/` - Announcements and updates
- `/loans/` - Loan management
- `/login/` - User authentication
- `/admin/` - Django admin panel

## Reports Available
- Contributions Report (Excel)
- Members Report (Excel)
- Transaction Logs Report (Excel)

## Technology Stack
- Django 4.2+
- Bootstrap 5
- Crispy Forms
- OpenPyXL (Excel reports)
- Pillow (Image handling)
- SQLite (default database)

## Next Steps
1. Run migrations: `python manage.py makemigrations && python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Run server: `python manage.py runserver`
4. Access at: `http://127.0.0.1:8000`

## Notes
- All views are protected with `@login_required`
- Admin-only views check for admin role
- Mobile-responsive design with offline detection
- Excel reports available for administrators
- Complete audit trail for all transactions


