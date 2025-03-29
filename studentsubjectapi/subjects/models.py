from django.db import models


class Program(models.Model):
    program_id = models.CharField(max_length=255, unique=True)
    program_name = models.CharField(max_length=255, unique=True)
    program_year = models.IntegerField(choices=[(i, f"Year {i}") for i in range(2, 5)], default=3)

    def __str__(self):
        return self.program_name

class Student(models.Model):
    student_id = models.CharField(max_length=255, unique=True)
    student_name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_name

class Subject(models.Model):
    YEAR_CHOICES = [(i, f"Year {i}") for i in range(1, 5)]
    SEMESTER_CHOICES = [(1, "Semester 1"), (2, "Semester 2")]

    course_id = models.CharField(max_length=255, unique=True)
    course_name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)

    def __str__(self):
        return self.course_name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

    
# from django.db import models

# class Program(models.Model):
#     program_id = models.CharField(max_length=255, unique=True)
#     program_name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.program_name

# class Student(models.Model):
#     student_id = models.CharField(max_length=255, unique=True)
#     student_name = models.CharField(max_length=255)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.student_name

# class Subject(models.Model):
#     YEAR_CHOICES = [(i, f"Year {i}") for i in range(1, 5)]
#     SEMESTER_CHOICES = [(1, "Semester 1"), (2, "Semester 2")]

#     course_id = models.CharField(max_length=255, unique=True)
#     course_name = models.CharField(max_length=255)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE,)  
#     year = models.IntegerField(choices=YEAR_CHOICES)
#     semester = models.IntegerField(choices=SEMESTER_CHOICES)

#     def __str__(self):
#         return self.course_name
    


