# QuizCertify – Online Quiz and Certificate System

QuizCertify is a web-based application developed using Django that allows users to take Python quizzes, view their scores, and receive certificates after passing the quiz.

## 🌐 Live Demo

https://quizcertify.onrender.com

## ✨ Features

- Online Python MCQ quiz
- User details form before starting the quiz
- Automatic score calculation
- Pass or fail result
- Certificate generation in PDF format
- Certificate delivery through email
- Unique Certificate ID
- QR code-based certificate verification
- Django admin login and dashboard
- Manage quiz questions and certificates
- Store quiz attempts and certificate records in the database

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS
- **Backend:** Python, Django
- **Database:** SQLite
- **PDF Generation:** ReportLab
- **QR Code:** Python QR Code library
- **Email Service:** Brevo API
- **Deployment:** Render
- **Version Control:** Git and GitHub

## ⚙️ How It Works

1. The user opens the QuizCertify website.
2. The user enters their name, mobile number, and email address.
3. The user answers the Python MCQ questions.
4. The system calculates the score automatically.
5. Users scoring 7 or more out of 10 pass the quiz.
6. Successful participants receive a PDF certificate by email.
7. Each certificate contains a unique ID and QR code.
8. Anyone can scan the QR code to verify the certificate.
9. The administrator can manage questions and view quiz attempts and certificates.

## 💻 Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/pranav-code01/QuizCertify.git
   ```

2. Open the project folder:

   ```bash
   cd QuizCertify
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open `http://127.0.0.1:8000/` in your browser.

## 👨‍💻 Developer

**Pranav Pandurang Hilal**

- GitHub: https://github.com/pranav-code01

## 📌 Project Purpose

This project was developed for learning and practical experience in Python, Django web development, database management, email integration, PDF generation, and deployment.

