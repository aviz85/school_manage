# Generated by Django 4.2.16 on 2024-09-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_student_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='employee_id',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]