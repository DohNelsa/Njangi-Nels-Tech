# Ngangi Platform

A comprehensive Django-based online platform for managing community savings groups (ngangi). This platform facilitates member management, savings tracking, meeting management, announcements, loans, and withdrawals with role-based access control.

## Features

### Core Modules

1. **Member Management**
   - Register and manage members (name, contact, role)
   - Member profiles with detailed information
   - Role-based access (Leader, Treasurer, Secretary, Member)
   - Active/inactive member status

2. **Savings/Contributions**
   - Record member contributions with date and amount
   - Track individual member account balances
   - Display current balance (contributions - withdrawals)
   - Transaction history and logs

3. **Meeting Management**
   - Schedule meetings with date, time, and location
   - Publish agenda and meeting minutes
   - Track attendance for each meeting
   - Bulk attendance recording

4. **Announcements/Updates**
   - News feed/bulletin section
   - Priority-based announcements (Low, Normal, High, Urgent)
   - Pinned announcements
   - Community updates (savings status, meeting summaries)
   - Expiration dates for announcements

5. **Loans/Withdrawals**
   - Loan requests with purpose and interest rates
   - Loan approval workflow
   - Loan repayment tracking
   - Withdrawal requests with approval system
   - Balance validation before withdrawals

6. **Dashboard/Admin View**
   - Overview of total savings, contributions, and loans
   - Upcoming meetings
   - Pending approvals (withdrawals and loans)
   - Recent transactions and announcements
   - Member statistics

7. **Security & Transparency**
   - Comprehensive transaction logs
   - Role-based access control
   - Exportable reports (Excel format)
   - Audit trail for all transactions
   - Admin vs Member views

8. **Mobile/Access Considerations**
   - Responsive Bootstrap 5 design
   - Mobile-friendly UI
   - Offline detection indicator
   - Simple, intuitive interface
   - Optimized for low-connectivity areas

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd "Nja platform"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser** (admin account)
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the platform**
   - Open your browser and go to: `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`
   - Login with the superuser credentials you created

## Project Structure

```
ngangi_platform/
├── manage.py
├── requirements.txt
├── README.md
├── ngangi_platform/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── members/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── contributions/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── meetings/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── announcements/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── loans/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── dashboard/
│   ├── views.py
│   ├── urls.py
│   └── reports.py
├── templates/
│   ├── base.html
│   ├── registration/
│   │   └── login.html
│   └── dashboard/
│       └── index.html
└── static/
    └── (static files)
```

## Usage Guide

### For Administrators (Leaders/Treasurers)

1. **Creating Members**
   - Navigate to Members → Create Member
   - Fill in member details and assign role
   - Members can register themselves, but need admin approval

2. **Recording Contributions**
   - Go to Contributions → Create Contribution
   - Select member, enter amount and date
   - Transaction is automatically logged

3. **Managing Meetings**
   - Create meetings with agenda
   - Record attendance after meeting
   - Update meeting minutes

4. **Approving Requests**
   - Review pending withdrawals and loans in Dashboard
   - Approve or reject requests with notes

5. **Generating Reports**
   - Export contributions, members, and transaction logs
   - Reports available in Excel format

### For Members

1. **Viewing Account Balance**
   - Go to Dashboard → My Profile
   - View contributions and current balance

2. **Requesting Withdrawals**
   - Go to Contributions → Create Withdrawal
   - Enter amount and reason
   - Wait for admin approval

3. **Applying for Loans**
   - Go to Loans → Create Loan
   - Fill in loan details and purpose
   - Wait for admin approval

4. **Viewing Announcements**
   - Check Announcements section for updates
   - View pinned announcements

## Configuration

### Database

By default, the project uses SQLite. To use PostgreSQL or MySQL:

1. Update `DATABASES` in `ngangi_platform/settings.py`
2. Install appropriate database adapter:
   ```bash
   pip install psycopg2  # For PostgreSQL
   pip install mysqlclient  # For MySQL
   ```

### Static Files

For production, collect static files:
```bash
python manage.py collectstatic
```

### Security Settings

Before deploying to production:

1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Update `ALLOWED_HOSTS`
4. Configure proper database
5. Set up HTTPS
6. Configure static file serving

## Technologies Used

- **Django 4.2+**: Web framework
- **Bootstrap 5**: Frontend framework
- **Crispy Forms**: Form styling
- **SQLite**: Default database (easily switchable)
- **OpenPyXL**: Excel report generation
- **Pillow**: Image handling

## Future Enhancements

- Service Worker for offline functionality
- SMS notifications
- Email notifications
- Mobile app (React Native/Flutter)
- Advanced analytics and charts
- PDF report generation
- Multi-language support
- Document uploads for loans

## Support

For issues or questions, please contact the development team.

## License

This project is proprietary software for community use.

## Contributing

This is a community project. Contributions are welcome through proper channels.


