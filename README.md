# Deigratia Montessori School Management System

A comprehensive school management system built with Django, designed to handle all aspects of school administration including student management, teacher portals, course management, assignments, attendance tracking, and more.

## 🚀 Features

### Core Functionality
- **User Management**: Students, Teachers, Parents, and Admin accounts
- **Course Management**: Subjects, classrooms, schedules, and materials
- **Assignment System**: Create, distribute, and grade assignments with quiz functionality
- **Attendance Tracking**: Digital attendance with reporting and notifications
- **Communication Tools**: Announcements, messages, and notifications
- **Fee Management**: Student fees, payments, and receipt generation
- **Payroll System**: Staff salary management and payslip generation
- **Appointment Booking**: Parent-teacher meeting scheduling
- **Website Integration**: Public website with admissions and information

### Advanced Features
- **Dashboard Analytics**: Performance metrics and insights
- **Report Generation**: Academic reports and report cards
- **Media Management**: Cloud storage integration with Backblaze B2
- **SEO Optimization**: Meta tags, sitemaps, and structured data
- **High Performance**: Redis caching for 2000+ concurrent users
- **Mobile Responsive**: Works on all devices

## 🛠️ Technology Stack

- **Backend**: Django 5.1.6, Python 3.8+
- **Database**: MySQL/TiDB Cloud with SSL
- **Cache**: Redis with django-redis
- **Storage**: Backblaze B2 for media files
- **Frontend**: Bootstrap 4, jQuery, HTML5/CSS3
- **Deployment**: Production-ready with environment variables

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0+ or TiDB Cloud account
- Redis server
- Backblaze B2 account (for media storage)
- Git

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ricas2410/deigratia.git
cd deigratia
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Update database credentials, API keys, etc.
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create cache table
python manage.py createcachetable
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

## ⚙️ Configuration

### Environment Variables

Key environment variables to configure in `.env`:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com

# Database
DB_HOST=your-database-host
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password

# Backblaze B2 Storage
B2_APPLICATION_KEY_ID=your-key-id
B2_APPLICATION_KEY=your-application-key
B2_BUCKET_NAME=your-bucket-name

# Redis
REDIS_URL=redis://localhost:6379/1

# Site Configuration
SITE_NAME=Your School Name
CANONICAL_URL_BASE=https://yourschool.com
```

### Redis Setup

#### Windows (using Chocolatey)
```powershell
choco install redis-64
redis-server
```

#### Docker
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

#### Ubuntu/Debian
```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
   - Set `DEBUG=False`
   - Configure strong `SECRET_KEY`
   - Set proper `ALLOWED_HOSTS`
   - Configure SSL settings

2. **Database**
   - Use production database (MySQL/PostgreSQL)
   - Enable SSL connections
   - Configure connection pooling

3. **Caching**
   - Set up Redis server
   - Configure cache settings for high traffic

4. **Media Storage**
   - Configure Backblaze B2 buckets
   - Set proper permissions

5. **Security**
   - Enable HTTPS
   - Configure security headers
   - Set up proper firewall rules

### Performance Optimization

The system is optimized for **2000+ concurrent users** with:

- **Redis Caching**: Multi-level caching strategy
- **Database Optimization**: Connection pooling and query optimization
- **Template Caching**: Cached template loaders
- **Static File Optimization**: CDN-ready with cache busting
- **Session Management**: Redis-based sessions

## 📊 Monitoring

### Performance Monitoring
```bash
# Monitor system performance
python manage.py monitor_performance --interval 10 --duration 300
```

### Health Checks
```bash
# Run system checks
python manage.py check

# Test database connection
python manage.py dbshell
```

## 🔐 Security Features

- **User Authentication**: Django's built-in authentication system
- **Permission System**: Role-based access control
- **CSRF Protection**: Cross-site request forgery protection
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping
- **Security Headers**: Comprehensive security headers
- **SSL/HTTPS**: Production SSL configuration

## 📱 API Documentation

The system includes RESTful APIs for:
- User management
- Course data
- Assignment submission
- Attendance tracking
- Communication features

API documentation is available at `/api/docs/` when running the server.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@deigratiaschool.com
- Documentation: [Wiki](https://github.com/Ricas2410/deigratia/wiki)

## 🙏 Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- Redis for high-performance caching
- Backblaze B2 for reliable storage
- All contributors and testers

---

**Deigratia Montessori School Management System** - Empowering education through technology.
