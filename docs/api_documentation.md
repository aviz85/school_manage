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

## Message Endpoints

28. **List Messages**
    - URL: `/api/messages/`
    - Method: GET
    - Description: Retrieve a list of all messages for the authenticated user
    - Authentication: Required

29. **Create Message**
    - URL: `/api/messages/`
    - Method: POST
    - Description: Create a new message
    - Authentication: Required
    - Request Body:
      ```json
      {
        "recipient": "integer",
        "subject": "string",
        "content": "string"
      }
      ```

30. **Retrieve Message**
    - URL: `/api/messages/{id}/`
    - Method: GET
    - Description: Retrieve details of a specific message
    - Authentication: Required

31. **Update Message**
    - URL: `/api/messages/{id}/`
    - Method: PUT/PATCH
    - Description: Update details of a specific message (limited to sender)
    - Authentication: Required

32. **Delete Message**
    - URL: `/api/messages/{id}/`
    - Method: DELETE
    - Description: Delete a specific message
    - Authentication: Required

33. **Get Inbox Messages**
    - URL: `/api/messages/inbox/`
    - Method: GET
    - Description: Retrieve all messages received by the authenticated user
    - Authentication: Required

34. **Get Sent Messages**
    - URL: `/api/messages/sent/`
    - Method: GET
    - Description: Retrieve all messages sent by the authenticated user
    - Authentication: Required

35. **Get Unread Message Count**
    - URL: `/api/messages/unread_count/`
    - Method: GET
    - Description: Get the count of unread messages for the authenticated user
    - Authentication: Required

36. **Mark Message as Read**
    - URL: `/api/messages/{id}/mark-as-read/`
    - Method: POST
    - Description: Mark a specific message as read
    - Authentication: Required

37. **Verify Message Content**
    - URL: `/api/messages/verify/`
    - Method: POST
    - Description: Verify if the message content adheres to school rules and is appropriate
    - Authentication: Required
    - Request Body:
      ```json
      {
        "content": "string"
      }
      ```
    - Response:
      ```json
      {
        "status": "string",
        "explanation": "string"
      }
      ```
    - Note: The status will be either "APPROVED" or "REJECTED". If rejected, an explanation will be provided.

Note: All message endpoints require authentication. Include the access token in the Authorization header as `Bearer <token>` for all requests.

Note: All endpoints require authentication. Include the access token in the Authorization header as `Bearer <token>` for all requests except the token obtain and refresh endpoints.