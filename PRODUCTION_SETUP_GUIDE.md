# Ricas School Management System - Production Setup Guide

## Overview
This guide will help you migrate from SQLite to MySQL (TiDB Cloud) and set up Backblaze B2 storage with Redis caching for 2000 concurrent users.

## Prerequisites
- Python virtual environment activated
- Access to TiDB Cloud database
- Backblaze B2 account with API keys

## Step 1: Install Redis

### Option A: Using Chocolatey (Recommended for Windows)
```powershell
# Install Chocolatey if not installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Redis
choco install redis-64 -y

# Start Redis
redis-server
```

### Option B: Using Docker
```powershell
docker run -d -p 6379:6379 --name redis redis:alpine
```

### Option C: Using WSL2 (Ubuntu)
```bash
sudo apt update
sudo apt install redis-server -y
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

## Step 2: Verify Current Configuration

The following configurations have been updated in `settings.py`:

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': '8yAv64zJkqvMmPm.root',
        'PASSWORD': 'JBiAxnIzpPjj094r',
        'HOST': 'gateway01.eu-central-1.prod.aws.tidbcloud.com',
        'PORT': '4000',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'ssl_mode': 'REQUIRED',
        },
    }
}
```

### Backblaze B2 Configuration
```python
B2_APPLICATION_KEY_ID = '05c3fdb889e3'
B2_APPLICATION_KEY = '005d9356855b1722ad320013f088234798ebf9dc68'
B2_BUCKET_NAME = 'ricas-school-media'
DEFAULT_FILE_STORAGE = 'shared_utils.storage_backends.B2MediaStorage'
```

### Redis Caching Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        # Optimized for 2000 concurrent users
    }
}
```

## Step 3: Manual Migration Steps

### 3.1 Backup Current Data
```powershell
# Create backup directory
mkdir migration_backup

# Copy SQLite database
copy db.sqlite3 migration_backup\db.sqlite3.backup

# Copy media files
xcopy media migration_backup\media /E /I

# Export data (run this in Django shell)
python manage.py shell
```

In Django shell:
```python
from django.core.management import call_command
import sys

# Export data
with open('migration_backup/data_export.json', 'w') as f:
    call_command('dumpdata', 
                '--natural-foreign', 
                '--natural-primary',
                '--exclude=contenttypes',
                '--exclude=auth.permission',
                '--exclude=sessions',
                '--exclude=admin.logentry',
                stdout=f)
print("Data exported successfully!")
exit()
```

### 3.2 Test Database Connection
```powershell
python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricas_school_manager.settings'); django.setup(); from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print('Database connected!')"
```

### 3.3 Run Fresh Migrations
```powershell
# Create fresh migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create cache table
python manage.py createcachetable
```

### 3.4 Create Superuser
```powershell
python manage.py createsuperuser
```

### 3.5 Load Basic Data
```powershell
python manage.py shell
```

In Django shell:
```python
from django.contrib.sites.models import Site
from users.models import SchoolSettings

# Configure site
site, created = Site.objects.get_or_create(
    id=1,
    defaults={'domain': 'ricasschool.com', 'name': 'Ricas School'}
)

# Create school settings
settings, created = SchoolSettings.objects.get_or_create(
    defaults={
        'school_name': 'Ricas School Management System',
        'school_address': 'Ghana',
        'school_phone': '+233-XXX-XXXX',
        'school_email': 'info@ricasschool.com',
    }
)

print("Basic data configured!")
exit()
```

## Step 4: Configure Backblaze B2 Buckets

1. **Login to Backblaze B2 Console**
2. **Create Buckets:**
   - `ricas-school-media` (for media files)
   - `ricas-school-static` (for static files)
3. **Set Bucket Permissions:** Public
4. **Note the Bucket URLs** for later use

## Step 5: Test the Setup

### 5.1 Test Database
```powershell
python manage.py check --database default
```

### 5.2 Test Redis
```powershell
python -c "import redis; r = redis.Redis(); r.ping(); print('Redis working!')"
```

### 5.3 Test Media Upload
```powershell
python manage.py shell
```

In Django shell:
```python
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Test file upload
test_file = ContentFile(b"test content", name="test.txt")
saved_path = default_storage.save("test.txt", test_file)
print(f"File saved to: {saved_path}")

# Test file URL
url = default_storage.url(saved_path)
print(f"File URL: {url}")

# Cleanup
default_storage.delete(saved_path)
print("Test completed!")
exit()
```

### 5.4 Run Development Server
```powershell
python manage.py runserver
```

## Step 6: Performance Monitoring

### 6.1 Monitor System Performance
```powershell
python manage.py monitor_performance --interval 10 --duration 300
```

### 6.2 Check Cache Performance
```powershell
python manage.py shell
```

In Django shell:
```python
from django.core.cache import cache
import time

# Test cache performance
start = time.time()
cache.set('test_key', 'test_value', 60)
value = cache.get('test_key')
end = time.time()

print(f"Cache response time: {(end - start) * 1000:.2f}ms")
print(f"Cache working: {value == 'test_value'}")
exit()
```

## Step 7: Production Deployment Checklist

### 7.1 Security Settings
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Enable SSL/HTTPS
- [ ] Configure security headers

### 7.2 Performance Settings
- [ ] Redis running and configured
- [ ] Database connection pooling enabled
- [ ] Static files collected
- [ ] Media files uploading to B2
- [ ] Caching middleware active

### 7.3 Monitoring
- [ ] Error logging configured
- [ ] Performance monitoring active
- [ ] Database monitoring
- [ ] Redis monitoring

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check SSL configuration
   - Verify credentials
   - Test network connectivity

2. **Redis Connection Errors**
   - Ensure Redis is running
   - Check port 6379 availability
   - Verify Redis configuration

3. **B2 Upload Errors**
   - Verify API keys
   - Check bucket permissions
   - Test bucket accessibility

4. **Migration Errors**
   - Reset migrations if needed
   - Check for model conflicts
   - Verify database schema

### Performance Optimization

1. **Database Optimization**
   - Enable query caching
   - Use database indexes
   - Optimize slow queries

2. **Cache Optimization**
   - Monitor cache hit ratios
   - Adjust cache timeouts
   - Use appropriate cache levels

3. **Media Optimization**
   - Compress images
   - Use CDN for static files
   - Optimize file uploads

## Support

For issues or questions:
1. Check Django logs: `logs/django.log`
2. Monitor system performance
3. Review error messages
4. Test individual components

## Next Steps

1. **Data Migration**: Import your existing data carefully
2. **User Training**: Train staff on new system
3. **Monitoring**: Set up continuous monitoring
4. **Backup**: Configure automated backups
5. **Scaling**: Monitor and scale as needed
