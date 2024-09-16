# School Management System - Server Side (Part 3)

## Overview

This is the third phase of a school management system built using the Django framework. We've expanded on the previous implementation by adding user authentication, a messaging system, and improving the overall user interface.

## Current Implementation

- Basic data models for the school system
- Django admin interface configuration
- User authentication (login/logout)
- Add Student feature
- Add Teacher feature
- Messaging system
- Improved UI with a responsive design

## Models

- UserProfile: Extends the built-in User model with user types
- Student: Stores student-specific information
- Teacher: Stores teacher-specific information
- Course: Represents academic courses
- Enrollment: Manages student enrollments in courses
- Message: Handles the messaging system between users

## New Features

1. **User Authentication**
   - Login and logout functionality
   - User-specific views based on user type (Admin, Teacher, Student)

2. **Add Teacher**
   - Allows administrators to add new teachers to the system
   - Automatically generates a unique employee ID for each teacher

3. **Messaging System**
   - Users can send and receive messages
   - Inbox view to display received messages
   - Unread message count displayed in the header

4. **Improved UI**
   - Responsive design using custom CSS
   - Cleaner and more modern look with improved typography and color scheme

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/aviz85/school_manage.git
   ```

2. Open the project folder:
   Use your preferred IDE or text editor to open the `school_manage` folder.

3. Checkout the `server-3` branch:
   ```
   git checkout server-3
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

## Testing the New Features

1. Access the login page:
   Open a web browser and go to `http://127.0.0.1:8000/`

2. Log in using the superuser credentials you created.

3. Explore the dashboard:
   - For admin users: Add new students or teachers
   - For all users: Send and receive messages

4. Test the messaging system:
   - Click on the "Inbox" link in the header
   - Compose a new message
   - Check for unread message notifications

5. Log out and log in as different user types to test role-specific features.

## Project Structure

- `core/`: Main application containing models, views, forms, and templates
  - `views.py`: Contains view functions for various features
  - `forms.py`: Contains forms for adding students and teachers
  - `models.py`: Defines data models including the new Message model
  - `templates/`: Contains HTML templates for different pages
- `school_manage/`: Project settings and configuration
  - `urls.py`: Updated with new URL paths for authentication and messaging
- `manage.py`: Django's command-line utility for administrative tasks

## Next Steps

In future phases, we plan to add more features such as:
- Course management (creation, assignment, enrollment)
- Grade input and reporting
- Advanced user profile management
- API development for potential frontend integration

## Contributing

We welcome contributions to this project. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.