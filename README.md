# School Management System - Server Side (Part 2)

## Overview

This is the second phase of a school management system built using the Django framework. We've expanded on the initial data models and admin interface by implementing our first feature: adding new students to the system.

## Current Implementation

- Basic data models for the school system
- Django admin interface configuration
- "Add Student" feature

## Models

- UserProfile: Extends the built-in User model with user types
- Student: Stores student-specific information
- Teacher: Stores teacher-specific information
- Course: Represents academic courses
- Enrollment: Manages student enrollments in courses

## New Feature: Add Student

We've implemented a new feature that allows authorized users to add new students to the system. This feature includes:

1. A new view function `add_student` in `core/views.py`
2. A form `StudentForm` in `core/forms.py` for handling student data input
3. A new template `add_student.html` for rendering the form
4. A new URL path in `school_manage/urls.py` to access the feature

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/aviz85/school_manage.git
   ```

2. Open the project folder:
   Use your preferred IDE or text editor to open the `school_manage` folder.

3. Checkout the `server-2` branch:
   ```
   git checkout server-2
   ```

4. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

6. Apply database migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```

8. (Optional) Populate the database with demo data:
   ```
   python manage.py populate_db
   ```

9. Run the development server:
   ```
   python manage.py runserver
   ```

## Testing the Add Student Feature

1. Access the admin panel:
   Open a web browser and go to `http://127.0.0.1:8000/admin/`
   Log in using the superuser credentials you created.

2. Navigate to the Add Student page:
   Go to `http://127.0.0.1:8000/add_student/`

3. Fill out the form with student details:
   - First Name
   - Last Name
   - Email
   - Date of Birth
   - Grade

4. Submit the form to create a new student.

5. Verify the new student:
   - Check the admin panel under the "Students" section
   - Or use the Django shell to query the database:
     ```
     python manage.py shell
     from core.models import Student
     Student.objects.all()
     ```

## Project Structure

- `core/`: Main application containing models, views, forms, and templates
  - `views.py`: Contains the `add_student` view function
  - `forms.py`: Contains the `StudentForm` for adding students
  - `templates/core/add_student.html`: Template for the add student form
- `school_manage/`: Project settings and configuration
  - `urls.py`: Updated with the new URL path for adding students
- `manage.py`: Django's command-line utility for administrative tasks

## Next Steps

In future phases, we'll continue to add more features such as:
- Listing and editing existing students
- Managing courses and enrollments
- Implementing a user authentication system

## Contributing

We welcome contributions to this project. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.