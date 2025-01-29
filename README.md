# Course Manager - Project Overview

**Course Manager** is an application designed to streamline the management of online courses, especially tailored for trainers, admins, and users. The application allows users to sign up, login, and manage their profiles while giving trainers a platform to handle courses, enrollments, and payments. The admin users can manage the entire system, including overseeing trainers, courses, and payments, providing a comprehensive solution for course management.

## Features

### Authentication

- **Signup**: Users can create accounts with basic information like name, email, and password.
- **Login**: Users (including trainers and admins) can log in using their email and password. Admins have access to manage the platform, while trainers can manage their courses.
- **Logout**: Users can log out from their accounts.

### Admin Dashboard

- **Analytics**: The admin dashboard provides key statistics, such as the number of users, trainers, courses, and payments.
- **Course Management**: Admins can create, edit, and delete courses, as well as assign courses to trainers.
- **Trainer Management**: Admins can view, edit, and delete trainers' profiles, as well as assign them courses.
- **Payment Management**: Admins can view and manage payments made by trainers for courses.

### Trainer Dashboard

- **Profile Management**: Trainers can view and update their profiles.
- **Course Enrollment**: Trainers can view, enroll, and manage the courses they teach. They can mark courses as completed and manage student enrollments.
- **Payments**: Trainers can make payments for courses they want to take and track their payment status.
- **Store**: Trainers can browse all available courses for purchase.

### User Roles

- **Admin**: Has full control over the platform, including course creation, trainer management, and payments.
- **Trainer**: Can manage their own profile, enroll in courses, manage their courses, and handle payment transactions for courses they wish to enroll in.
- **User**: Regular users can browse available courses and purchase them.

## Tech Stack

- **Backend**: Django,
- **Database**: SQLite
- **Authentication**: Custom user authentication using Django’s built-in authentication system with custom user models.
- **Frontend**: HTML5, CSS3, and JavaScript for rendering the user interface.

## How It Works

### Signup & Login Process

- The user signs up with basic details (first name, last name, email, password).
- Upon logging in, trainers are authenticated, and if they are not authorized as trainers, they receive an error message.
- After successful login, users are directed to their respective dashboards (trainers to the trainer dashboard, admins to the admin dashboard).

### Admin Features

- Admin users can manage the system entirely from their dashboard. They can add or remove trainers, manage courses, track payments, and see overall system statistics like active users, courses, and payments.

### Trainer Features

- Trainers can create and manage their profiles, enroll in courses, and complete courses they are teaching. They can also make payments to enroll in courses they wish to take.
- The trainer’s dashboard also allows trainers to mark courses as completed and manage enrollments.

### Payment Handling

- Payments are linked to course enrollments. A trainer can make payments for courses either when they are enrolling or purchasing. The payment status is recorded (Pending, Paid) and can be tracked by admins and trainers alike.

## Project Setup

1. **Clone the Repository**:
2. **Create env**:
   Make sure you create `python -m venv env`.
3. **Install Dependencies**:
   Make sure you have `pip` installed. Then run:
4. **Migrate Database**:
   The app uses Django’s ORM to interact with the database. Run the following commands to set up the database:
5. **Create a Superuser**:
   To access the admin dashboard, create a superuser:

The app will be available at `http://127.0.0.1:8000`.
