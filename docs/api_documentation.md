# School Management System API Endpoints

## Authentication Endpoints

1. **Obtain Token**
   - URL: `/api/token/`
   - Method: POST
   - Description: Authenticate user and receive access and refresh tokens
   - Request Body:
     ```json
     {
       "username": "string",
       "password": "string"
     }
     ```
   - Response:
     ```json
     {
       "access": "string",
       "refresh": "string"
     }
     ```

2. **Refresh Token**
   - URL: `/api/token/refresh/`
   - Method: POST
   - Description: Obtain a new access token using a refresh token
   - Request Body:
     ```json
     {
       "refresh": "string"
     }
     ```
   - Response:
     ```json
     {
       "access": "string"
     }
     ```

## Student Endpoints

3. **List Students**
   - URL: `/api/students/`
   - Method: GET
   - Description: Retrieve a list of all students
   - Authentication: Required

4. **Create Student**
   - URL: `/api/students/`
   - Method: POST
   - Description: Create a new student
   - Authentication: Required
   - Request Body:
     ```json
     {
       "user_profile": "integer",
       "student_id": "string",
       "date_of_birth": "date",
       "grade": "integer"
     }
     ```

5. **Retrieve Student**
   - URL: `/api/students/{id}/`
   - Method: GET
   - Description: Retrieve details of a specific student
   - Authentication: Required

6. **Update Student**
   - URL: `/api/students/{id}/`
   - Method: PUT/PATCH
   - Description: Update details of a specific student
   - Authentication: Required

7. **Delete Student**
   - URL: `/api/students/{id}/`
   - Method: DELETE
   - Description: Delete a specific student
   - Authentication: Required

## Teacher Endpoints

8. **List Teachers**
   - URL: `/api/teachers/`
   - Method: GET
   - Description: Retrieve a list of all teachers
   - Authentication: Required

9. **Create Teacher**
   - URL: `/api/teachers/`
   - Method: POST
   - Description: Create a new teacher
   - Authentication: Required
   - Request Body:
     ```json
     {
       "user_profile": "integer",
       "employee_id": "string",
       "subject": "string"
     }
     ```

10. **Retrieve Teacher**
    - URL: `/api/teachers/{id}/`
    - Method: GET
    - Description: Retrieve details of a specific teacher
    - Authentication: Required

11. **Update Teacher**
    - URL: `/api/teachers/{id}/`
    - Method: PUT/PATCH
    - Description: Update details of a specific teacher
    - Authentication: Required

12. **Delete Teacher**
    - URL: `/api/teachers/{id}/`
    - Method: DELETE
    - Description: Delete a specific teacher
    - Authentication: Required

## Course Endpoints

13. **List Courses**
    - URL: `/api/courses/`
    - Method: GET
    - Description: Retrieve a list of all courses
    - Authentication: Required

14. **Create Course**
    - URL: `/api/courses/`
    - Method: POST
    - Description: Create a new course
    - Authentication: Required
    - Request Body:
      ```json
      {
        "name": "string",
        "code": "string",
        "teacher": "integer",
        "students": ["integer"]
      }
      ```

15. **Retrieve Course**
    - URL: `/api/courses/{id}/`
    - Method: GET
    - Description: Retrieve details of a specific course
    - Authentication: Required

16. **Update Course**
    - URL: `/api/courses/{id}/`
    - Method: PUT/PATCH
    - Description: Update details of a specific course
    - Authentication: Required

17. **Delete Course**
    - URL: `/api/courses/{id}/`
    - Method: DELETE
    - Description: Delete a specific course
    - Authentication: Required

## Enrollment Endpoints

18. **List Enrollments**
    - URL: `/api/enrollments/`
    - Method: GET
    - Description: Retrieve a list of all enrollments
    - Authentication: Required

19. **Create Enrollment**
    - URL: `/api/enrollments/`
    - Method: POST
    - Description: Create a new enrollment
    - Authentication: Required
    - Request Body:
      ```json
      {
        "student": "integer",
        "course": "integer",
        "date_enrolled": "date"
      }
      ```

20. **Retrieve Enrollment**
    - URL: `/api/enrollments/{id}/`
    - Method: GET
    - Description: Retrieve details of a specific enrollment
    - Authentication: Required

21. **Update Enrollment**
    - URL: `/api/enrollments/{id}/`
    - Method: PUT/PATCH
    - Description: Update details of a specific enrollment
    - Authentication: Required

22. **Delete Enrollment**
    - URL: `/api/enrollments/{id}/`
    - Method: DELETE
    - Description: Delete a specific enrollment
    - Authentication: Required

## Grade Endpoints

23. **List Grades**
    - URL: `/api/grades/`
    - Method: GET
    - Description: Retrieve a list of all grades
    - Authentication: Required

24. **Create Grade**
    - URL: `/api/grades/`
    - Method: POST
    - Description: Create a new grade
    - Authentication: Required
    - Request Body:
      ```json
      {
        "enrollment": "integer",
        "grade": "number",
        "date_graded": "date"
      }
      ```

25. **Retrieve Grade**
    - URL: `/api/grades/{id}/`
    - Method: GET
    - Description: Retrieve details of a specific grade
    - Authentication: Required

26. **Update Grade**
    - URL: `/api/grades/{id}/`
    - Method: PUT/PATCH
    - Description: Update details of a specific grade
    - Authentication: Required

27. **Delete Grade**
    - URL: `/api/grades/{id}/`
    - Method: DELETE
    - Description: Delete a specific grade
    - Authentication: Required

Note: All endpoints require authentication. Include the access token in the Authorization header as `Bearer <token>` for all requests except the token obtain and refresh endpoints.