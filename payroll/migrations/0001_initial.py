# Generated by Django 5.1.6 on 2025-06-04 00:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deduction_type', models.CharField(choices=[('LOAN', 'Loan Repayment'), ('ADVANCE', 'Salary Advance'), ('LATENESS', 'Lateness'), ('ABSENCE', 'Absence'), ('TAX', 'Additional Tax'), ('OTHER', 'Other')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, help_text='Leave blank for one-time deductions', null=True)),
                ('is_recurring', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Deduction',
                'verbose_name_plural': 'Deductions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transport_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('housing_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('other_allowances', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('gross_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ssnit_deduction', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tax_deduction', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('other_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_deductions', models.DecimalField(decimal_places=2, max_digits=10)),
                ('net_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled')], default='DRAFT', max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payroll',
                'verbose_name_plural': 'Payrolls',
                'ordering': ['-period__start_date', 'staff_salary__user__first_name'],
            },
        ),
        migrations.CreateModel(
            name='PayrollPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('CASH', 'Cash'), ('BANK_TRANSFER', 'Bank Transfer'), ('MOBILE_MONEY', 'Mobile Money'), ('CHECK', 'Check'), ('OTHER', 'Other')], default='BANK_TRANSFER', max_length=20)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payroll Payment',
                'verbose_name_plural': 'Payroll Payments',
                'ordering': ['-payment_date'],
            },
        ),
        migrations.CreateModel(
            name='PayrollPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_locked', models.BooleanField(default=False, help_text='If locked, no changes can be made to payrolls in this period')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payroll Period',
                'verbose_name_plural': 'Payroll Periods',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payslip_number', models.CharField(max_length=50, unique=True)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='payslips/')),
                ('is_emailed', models.BooleanField(default=False)),
                ('emailed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Payslip',
                'verbose_name_plural': 'Payslips',
                'ordering': ['-generated_at'],
            },
        ),
        migrations.CreateModel(
            name='StaffRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_teaching_staff', models.BooleanField(default=True, help_text='Whether this role is for teaching staff')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Staff Role',
                'verbose_name_plural': 'Staff Roles',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StaffSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transport_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('housing_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('other_allowances', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('ssnit_contribution', models.DecimalField(decimal_places=2, default=0, help_text='Standard SSNIT deduction amount', max_digits=10)),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0, help_text='Tax rate as a percentage', max_digits=5)),
                ('effective_date', models.DateField(default=django.utils.timezone.now)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Staff Salary',
                'verbose_name_plural': 'Staff Salaries',
                'ordering': ['-updated_at'],
            },
        ),
    ]
