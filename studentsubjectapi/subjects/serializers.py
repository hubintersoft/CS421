from rest_framework import serializers
from .models import Program, Student, Subject, Enrollment

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['program_id', 'program_name', 'program_year']

class StudentSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    program_name = serializers.CharField(source='program.program_name', read_only=True)  

    class Meta:
        model = Student
        fields = ['student_id', 'student_name', 'program', 'program_name']

class SubjectSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())

    class Meta:
        model = Subject
        fields = ['course_id', 'course_name', 'program', 'year', 'semester']

    def validate(self, data):
        """
        Custom validation to ensure that course_id is unique.
        """
        if Subject.objects.filter(course_id=data['course_id']).exists():
            raise serializers.ValidationError("A subject with this course ID already exists.")
        return data

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True)

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']



    
# class SubjectSerializer(serializers.ModelSerializer):
#     program_name = serializers.CharField(source='program.program_name', read_only=True) 
#     student_name = serializers.CharField(source='student.student_name', read_only=True)

#     class Meta:
#         model = Subject
#         # fields = ['course_id', 'course_name', 'program_name', 'student_name', 'year', 'semester']
#         fields = ['course_id', 'course_name', 'program', 'program_name', 'student', 'student_name', 'year', 'semester']


