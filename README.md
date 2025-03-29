Student & Subjects API (Django + DRF)
A RESTful API built with Django and Django REST Framework, using a relational database SQLite to manage student and academic program data.

Features
Endpoint 1 (/students):

Returns a JSON response with 10+ student records, including name and enrolled_program.

Uses Django ORM models and DRF serializers.

Endpoint 2 (/subjects):

Returns a structured JSON list of subjects in the Software Engineering program, grouped by academic year (Year 1–4).

Tech Stack
Backend: Django 4.x + Django REST Framework

Database: SQLite

Deployment: AWS Ubuntu (Gunicorn)
