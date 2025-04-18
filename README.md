Student & Subjects API (Django + DRF)
A RESTful API built with Django and Django REST Framework, using a relational database MySQL to manage student and academic program data.

Features
Endpoint 1 (/api/students):
MODIFIED LINK: http://ec2-51-20-63-133.eu-north-1.compute.amazonaws.com/api/students/

Returns a JSON response with 10+ student records, including name and enrolled_program.

Uses Django ORM models and DRF serializers.

Endpoint 2 (/api/subjects):
MODIFIED LINK: http://ec2-51-20-63-133.eu-north-1.compute.amazonaws.com/api/subjects/

Returns a structured JSON list of subjects in the Software Engineering program, grouped by academic year (Year 1–4).

Tech Stack
Backend: Django 4.x + Django REST Framework

Database: MySQL

Deployment: AWS Ubuntu (Gunicorn)
