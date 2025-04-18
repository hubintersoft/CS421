ASSIGMENT 1:
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
Backend: Django + Django REST Framework

Database: MySQL

Deployment: AWS Ubuntu (Gunicorn)


ASSIGMENT 2:
0. Types of backup schemes
a)Full Backup: It create a complete copy of all data.
Execution: Copies all data from the source to the backup destination, creating a complete snapshot. 
Advantages: Provides the most reliable restoration point, as the entire data set is available. 
Disadvantages: Requires the most storage space and time to execute. 

b)Differential Backup: It copy changes since the last full backup but include all data changed since then. 
Execution: Copies all changes made since the last full backup.
Advantages: Restores more quickly than incremental backups because only the changes since the last full backup need to be applied.
Disadvantages: Can consume more storage space than incremental backups because it includes all changes since the last full backup. 

c)Incremental Backup: It copy only changes since the last full backup
Execution: Copies only changes made since the last backup, whether full or incremental.
Advantages: Requires the least storage space and time to execute, especially after a full backup.
Disadvantages: Restoration can take longer as all incremental backups from the full backup point need to be applied. 

