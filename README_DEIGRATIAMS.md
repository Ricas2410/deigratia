# 🎓 Deigratia Montessori School Management System

A comprehensive Django-based school management system designed specifically for Montessori education, featuring modern web technologies and user-friendly interfaces.

## 🌟 Features

### 👥 User Management
- **Multi-role Authentication**: Admin, Teachers, Students, Parents
- **Secure Login System**: Email-based authentication with role-based access
- **Profile Management**: Comprehensive user profiles with photo uploads

### 📚 Academic Management
- **Course Management**: Subjects, classes, and curriculum tracking
- **Assignment System**: Create, distribute, and grade assignments
- **Grade Management**: Comprehensive grading and report card system
- **Attendance Tracking**: Daily attendance with detailed reporting

### 💬 Communication Hub
- **Messaging System**: Internal messaging between users
- **Announcements**: Targeted announcements for different user groups
- **Event Management**: School events and calendar integration
- **Notifications**: Real-time notification system

### 💰 Financial Management
- **Fee Management**: Student fee tracking and payment processing
- **Payment Integration**: Secure payment gateway integration
- **Financial Reporting**: Comprehensive financial reports

### 🌐 Public Website
- **Modern Design**: Responsive website with Montessori-focused design
- **Content Management**: Easy-to-manage website content
- **Testimonials**: Parent and student testimonials
- **News & Events**: Public announcements and event listings

### 📊 Dashboard & Analytics
- **Role-based Dashboards**: Customized dashboards for each user type
- **Analytics**: Comprehensive reporting and analytics
- **Data Visualization**: Charts and graphs for better insights

## 🚀 Technology Stack

- **Backend**: Django 5.1.6 (Python)
- **Database**: PostgreSQL (Neon Cloud)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Cache**: Redis (Production) / Local Memory (Development)
- **File Storage**: Backblaze B2 (Optional)
- **Email**: SMTP integration
- **Deployment**: Production-ready configuration

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/deigratiams/deigratia-school-management.git
   cd deigratia-school-management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database and other settings
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python setup_initial_data.py
   python create_sample_data.py
   ```

6. **Run the application**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 🔑 Default Login Credentials

### Admin Access
- **Email**: admin@deigratiamontessori.edu.gh
- **Password**: admin123

### Sample Users
- **Teachers**: teacher@mail.com / teacher123
- **Students**: student@mail.com / student123
- **Parents**: parent@mail.com / parent123

## 📁 Project Structure

```
deigratia-school-management/
├── ricas_school_manager/     # Main Django project
├── users/                    # User management app
├── courses/                  # Academic management
├── assignments/              # Assignment system
├── attendance/               # Attendance tracking
├── communications/           # Messaging & announcements
├── fees/                     # Financial management
├── website/                  # Public website
├── dashboard/                # Dashboard & analytics
├── static/                   # Static files
├── templates/                # HTML templates
├── media/                    # User uploads
├── setup_initial_data.py     # Initial setup script
├── create_sample_data.py     # Sample data script
└── requirements.txt          # Python dependencies
```

## 🔒 Security Features

- **Environment Variables**: All sensitive data in environment variables
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM protection
- **Secure Headers**: Security middleware enabled
- **Password Hashing**: Secure password storage
- **Role-based Access**: Comprehensive permission system

## 🌍 Production Deployment

The application is production-ready with:
- **SSL Support**: HTTPS configuration
- **Database Optimization**: Connection pooling and optimization
- **Caching**: Redis caching for high performance
- **Static Files**: Optimized static file serving
- **Error Handling**: Comprehensive error handling and logging

## 📖 Documentation

- **Setup Guide**: Complete installation and configuration guide
- **User Manual**: Comprehensive user documentation
- **API Documentation**: REST API endpoints documentation
- **Deployment Guide**: Production deployment instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏫 About Deigratia Montessori School

Deigratia Montessori School is committed to providing quality Montessori education that nurtures young minds through child-centered learning approaches, fostering independence, creativity, and lifelong learning.

## 📞 Support

For support and questions:
- **Email**: info@deigratiamontessori.edu.gh
- **Website**: https://deigratiamontessori.edu.gh
- **GitHub Issues**: [Create an issue](https://github.com/deigratiams/deigratia-school-management/issues)

---

**Made with ❤️ for Montessori Education**
