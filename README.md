# School Management System - Server Side (Part 1)

## Overview

This is the initial phase of a school management system built using the Django framework. In this stage, we've set up the basic data models and configured the Django admin interface. This serves as the foundation for future development of the school management system.

## Current Implementation

- Basic data models for the school system
- Django admin interface configuration

## Models

- UserProfile: Extends the built-in User model with user types
- Student: Stores student-specific information
- Teacher: Stores teacher-specific information
- Course: Represents academic courses
- Enrollment: Manages student enrollments in courses

## Installation and Setup

1. Clone the repository:
   - Open Cursor software
   - In the bottom panel, open the terminal
   - Type the following command:
     ```
     git clone https://github.com/aviz85/school_manage.git
     ``` 

2. Open the project folder:
   Use Cursor's "Open Folder" option to open the `school_manage` folder.

3. Checkout the `server-1` branch:
   In the terminal, run:
   ```
   git checkout server-1
   ```

4. Create a virtual environment:
   ```
   python -m venv venv
   ```

5. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

6. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

7. Apply database migrations:
   ```
   python manage.py migrate
   ```

8. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to set up your admin username and password.

9. (Optional) Populate the database with demo data:
   ```
   python manage.py populate_db
   ```
   This command will create fake data for demonstration purposes.

10. Run the development server:
    ```
    python manage.py runserver
    ```

11. Access the admin panel:
    Open a web browser and go to `http://127.0.0.1:8000/admin/`
    Log in using the superuser credentials you created in step 7.

## Project Structure

- `core/`: Main application containing models and admin configurations
- `school_manage/`: Project settings and configuration
- `manage.py`: Django's command-line utility for administrative tasks

## Next Steps

This phase lays the groundwork for the school management system. In future phases, we'll be adding views, templates, and implementing actual features to create a functional application.

## Contributing

We welcome contributions to this project. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.