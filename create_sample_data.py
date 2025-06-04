#!/usr/bin/env python3
"""
Comprehensive sample data creation script for Deigratia Montessori School.
Creates realistic demo data including users, courses, announcements, materials, etc.
"""

import os
import django
from datetime import timedelta, date
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricas_school_manager.settings')
django.setup()

from users.models import CustomUser, Teacher, Student, Parent
from communications.models import Announcement
from website.models import Testimonial

# Sample data constants
SAMPLE_IMAGES = {
    'profile': [
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
        'https://images.unsplash.com/photo-1494790108755-2616b612b5bc?w=150&h=150&fit=crop&crop=face',
        'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face',
        'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face',
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
        'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face',
    ],
    'materials': [
        'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400&h=300&fit=crop',
        'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400&h=300&fit=crop',
    ],
    'school': [
        'https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=600&h=400&fit=crop',
    ]
}

def create_teachers():
    """Create sample teachers."""
    print("👨‍🏫 Creating sample teachers...")
    
    teachers_data = [
        {
            'email': 'teacher@mail.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'phone': '+233 24 111 1111',
            'employee_id': 'TCH001',
            'department': 'Primary Education',
            'qualification': 'B.Ed in Early Childhood Education, Montessori Certification'
        },
        {
            'email': 'mary.asante@mail.com',
            'first_name': 'Mary',
            'last_name': 'Asante',
            'phone': '+233 24 111 1112',
            'employee_id': 'TCH002',
            'department': 'Mathematics',
            'qualification': 'M.Ed in Mathematics Education'
        },
        {
            'email': 'john.mensah@mail.com',
            'first_name': 'John',
            'last_name': 'Mensah',
            'phone': '+233 24 111 1113',
            'employee_id': 'TCH003',
            'department': 'Science',
            'qualification': 'B.Sc in Biology, Teaching Certificate'
        },
        {
            'email': 'grace.osei@mail.com',
            'first_name': 'Grace',
            'last_name': 'Osei',
            'phone': '+233 24 111 1114',
            'employee_id': 'TCH004',
            'department': 'Language Arts',
            'qualification': 'B.A in English, Montessori Training'
        },
        {
            'email': 'kwame.boateng@mail.com',
            'first_name': 'Kwame',
            'last_name': 'Boateng',
            'phone': '+233 24 111 1115',
            'employee_id': 'TCH005',
            'department': 'Creative Arts',
            'qualification': 'B.F.A in Visual Arts, Teaching Certificate'
        }
    ]
    
    created_count = 0
    for teacher_data in teachers_data:
        try:
            # Create user
            user = CustomUser.objects.create(
                email=teacher_data['email'],
                password=make_password('teacher123'),
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name'],
                role='TEACHER',
                phone_number=teacher_data['phone'],
                is_active=True,
                is_verified=True
            )
            
            # Create teacher profile
            Teacher.objects.create(
                user=user,
                employee_id=teacher_data['employee_id'],
                department=teacher_data['department'],
                qualification=teacher_data['qualification']
            )
            
            created_count += 1
            print(f"   ✅ Created teacher: {teacher_data['first_name']} {teacher_data['last_name']}")
            
        except Exception as e:
            print(f"   ⚠️ Teacher {teacher_data['email']} might already exist: {e}")
    
    print(f"✅ Created {created_count} teachers!")

def create_students():
    """Create sample students."""
    print("👨‍🎓 Creating sample students...")
    
    students_data = [
        {
            'email': 'student@mail.com',
            'first_name': 'Ama',
            'last_name': 'Kwarteng',
            'student_id': 'STU001',
            'pin': '12345',
            'date_of_birth': date(2015, 3, 15),
            'grade': 'Primary 3',
            'section': 'A'
        },
        {
            'email': 'kofi.asante@mail.com',
            'first_name': 'Kofi',
            'last_name': 'Asante',
            'student_id': 'STU002',
            'pin': '23456',
            'date_of_birth': date(2014, 7, 22),
            'grade': 'Primary 4',
            'section': 'B'
        },
        {
            'email': 'akosua.mensah@mail.com',
            'first_name': 'Akosua',
            'last_name': 'Mensah',
            'student_id': 'STU003',
            'pin': '34567',
            'date_of_birth': date(2016, 1, 10),
            'grade': 'Primary 2',
            'section': 'A'
        },
        {
            'email': 'kweku.osei@mail.com',
            'first_name': 'Kweku',
            'last_name': 'Osei',
            'student_id': 'STU004',
            'pin': '45678',
            'date_of_birth': date(2015, 9, 5),
            'grade': 'Primary 3',
            'section': 'B'
        },
        {
            'email': 'abena.boateng@mail.com',
            'first_name': 'Abena',
            'last_name': 'Boateng',
            'student_id': 'STU005',
            'pin': '56789',
            'date_of_birth': date(2013, 11, 18),
            'grade': 'Primary 5',
            'section': 'A'
        }
    ]
    
    created_count = 0
    for student_data in students_data:
        try:
            # Create user
            user = CustomUser.objects.create(
                email=student_data['email'],
                password=make_password('student123'),
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                role='STUDENT',
                is_active=True,
                is_verified=True
            )
            
            # Create student profile
            Student.objects.create(
                user=user,
                student_id=student_data['student_id'],
                pin=student_data['pin'],
                date_of_birth=student_data['date_of_birth'],
                section=student_data['section'],
                status='ACTIVE'
            )
            
            created_count += 1
            print(f"   ✅ Created student: {student_data['first_name']} {student_data['last_name']}")
            
        except Exception as e:
            print(f"   ⚠️ Student {student_data['email']} might already exist: {e}")
    
    print(f"✅ Created {created_count} students!")

def create_parents():
    """Create sample parents."""
    print("👨‍👩‍👧‍👦 Creating sample parents...")
    
    parents_data = [
        {
            'email': 'parent@mail.com',
            'first_name': 'Robert',
            'last_name': 'Kwarteng',
            'phone': '+233 24 222 2221',
            'occupation': 'Engineer',
            'relationship': 'Father',
            'children_emails': ['student@mail.com']
        },
        {
            'email': 'elizabeth.asante@mail.com',
            'first_name': 'Elizabeth',
            'last_name': 'Asante',
            'phone': '+233 24 222 2222',
            'occupation': 'Doctor',
            'relationship': 'Mother',
            'children_emails': ['kofi.asante@mail.com']
        },
        {
            'email': 'samuel.mensah@mail.com',
            'first_name': 'Samuel',
            'last_name': 'Mensah',
            'phone': '+233 24 222 2223',
            'occupation': 'Teacher',
            'relationship': 'Father',
            'children_emails': ['akosua.mensah@mail.com']
        }
    ]
    
    created_count = 0
    for parent_data in parents_data:
        try:
            # Create user
            user = CustomUser.objects.create(
                email=parent_data['email'],
                password=make_password('parent123'),
                first_name=parent_data['first_name'],
                last_name=parent_data['last_name'],
                role='PARENT',
                phone_number=parent_data['phone'],
                is_active=True,
                is_verified=True
            )
            
            # Create parent profile
            parent = Parent.objects.create(
                user=user,
                occupation=parent_data['occupation'],
                relationship=parent_data['relationship']
            )
            
            # Link children
            for child_email in parent_data['children_emails']:
                try:
                    child_user = CustomUser.objects.get(email=child_email)
                    child_student = Student.objects.get(user=child_user)
                    parent.children.add(child_student)
                except:
                    pass
            
            created_count += 1
            print(f"   ✅ Created parent: {parent_data['first_name']} {parent_data['last_name']}")
            
        except Exception as e:
            print(f"   ⚠️ Parent {parent_data['email']} might already exist: {e}")
    
    print(f"✅ Created {created_count} parents!")

def create_announcements():
    """Create sample announcements."""
    print("📢 Creating sample announcements...")

    announcements_data = [
        {
            'title': 'Welcome to New Academic Year 2024/2025',
            'content': 'We are excited to welcome all students and parents to the new academic year. Classes begin on Monday, September 9th, 2024. Please ensure all school fees are paid and uniforms are ready.',
            'target_type': 'ALL'
        },
        {
            'title': 'Parent-Teacher Conference Scheduled',
            'content': 'Our quarterly parent-teacher conference is scheduled for October 15-16, 2024. Please book your appointment slots through the parent portal or contact the school office.',
            'target_type': 'PARENTS'
        },
        {
            'title': 'Science Fair 2024 - Call for Participation',
            'content': 'Students from Primary 3-6 are invited to participate in our annual Science Fair. Registration deadline is November 1st, 2024. Exciting prizes await!',
            'target_type': 'STUDENTS'
        },
        {
            'title': 'School Closure - Independence Day',
            'content': 'The school will be closed on March 6th, 2025 in observance of Ghana Independence Day. Classes will resume on March 7th, 2025.',
            'target_type': 'ALL'
        },
        {
            'title': 'New Montessori Materials Arrived',
            'content': 'We have received new Montessori learning materials for our sensorial and mathematics programs. Teachers, please schedule training sessions.',
            'target_type': 'TEACHERS'
        }
    ]

    created_count = 0
    admin_user = CustomUser.objects.filter(role='ADMIN').first()

    for announcement_data in announcements_data:
        try:
            Announcement.objects.create(
                title=announcement_data['title'],
                content=announcement_data['content'],
                target_type=announcement_data['target_type'],
                created_by=admin_user,
                expires_at=timezone.now() + timedelta(days=30)
            )
            created_count += 1
            print(f"   ✅ Created announcement: {announcement_data['title']}")
        except Exception as e:
            print(f"   ⚠️ Announcement might already exist: {e}")

    print(f"✅ Created {created_count} announcements!")

def create_testimonials():
    """Create sample testimonials."""
    print("💬 Creating sample testimonials...")

    testimonials_data = [
        {
            'name': 'Mrs. Akosua Darko',
            'role': 'Parent',
            'content': 'Deigratia Montessori School has been a blessing to our family. My daughter has grown tremendously in confidence and independence. The teachers are caring and professional.'
        },
        {
            'name': 'Mr. Kwame Asiedu',
            'role': 'Parent',
            'content': 'The Montessori approach at Deigratia has helped my son develop a love for learning. He comes home excited about school every day. Highly recommended!'
        },
        {
            'name': 'Dr. Grace Ofosu',
            'role': 'Educational Consultant',
            'content': 'As an educational consultant, I am impressed by the quality of education at Deigratia. The school truly embodies the Montessori philosophy.'
        },
        {
            'name': 'Mrs. Esi Mensah',
            'role': 'Former Parent',
            'content': 'Both my children attended Deigratia and are now excelling in secondary school. The foundation they received here was exceptional.'
        }
    ]

    created_count = 0
    for testimonial_data in testimonials_data:
        try:
            Testimonial.objects.create(
                name=testimonial_data['name'],
                role=testimonial_data['role'],
                content=testimonial_data['content'],
                is_featured=True
            )
            created_count += 1
            print(f"   ✅ Created testimonial: {testimonial_data['name']}")
        except Exception as e:
            print(f"   ⚠️ Testimonial might already exist: {e}")

    print(f"✅ Created {created_count} testimonials!")

def main():
    """Main function to create all sample data."""
    print("🎯 Creating comprehensive sample data for Deigratia Montessori School...")
    print("=" * 70)

    try:
        create_teachers()
        create_students()
        create_parents()
        create_announcements()
        create_testimonials()

        print("\n" + "=" * 70)
        print("✅ Sample data creation completed!")
        print("\n📊 Summary:")
        print(f"   👨‍🏫 Teachers: {Teacher.objects.count()}")
        print(f"   👨‍🎓 Students: {Student.objects.count()}")
        print(f"   👨‍👩‍👧‍👦 Parents: {Parent.objects.count()}")
        print(f"   👥 Total Users: {CustomUser.objects.count()}")
        print(f"   📢 Announcements: {Announcement.objects.count()}")
        print(f"   💬 Testimonials: {Testimonial.objects.count()}")

        print("\n🔑 Login Credentials:")
        print("   👨‍🏫 Teachers: teacher@mail.com / teacher123")
        print("   👨‍🎓 Students: student@mail.com / student123")
        print("   👨‍👩‍👧‍👦 Parents: parent@mail.com / parent123")

    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

    return True

if __name__ == '__main__':
    main()
