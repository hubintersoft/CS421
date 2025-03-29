from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Enrollment, Program, Student, Subject
from .serializers import EnrollmentSerializer, ProgramSerializer, StudentSerializer, SubjectSerializer

class ProgramListView(APIView):
    def get(self, request):
        programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.get('programs', request.data)  # Handle nested and direct data
        
        if isinstance(data, list):  # Multiple programs
            serializer = ProgramSerializer(data=data, many=True)
        else:  # Single program
            serializer = ProgramSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentListView(APIView):
    def get(self, request):
        """Retrieve all students"""
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a single or multiple students after validating program existence"""
        data = request.data.get('students', request.data)  # Support both single & bulk insert
        many = isinstance(data, list)

        # Extract all program IDs from request data
        if many:
            program_ids = {student.get('program') for student in data if 'program' in student}
        else:
            program_ids = {data.get('program')} if 'program' in data else set()

        # Ensure all provided program IDs exist
        existing_program_ids = set(Program.objects.values_list('program_id', flat=True))
        invalid_programs = program_ids - existing_program_ids

        if invalid_programs:
            return Response(
                {"error": f"Invalid program IDs: {list(invalid_programs)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serialize and validate data
        serializer = StudentSerializer(data=data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FilterStudentsView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch at least 10 students from the database
        students = Student.objects.all()[:10]
        
        # Serialize the student data
        serializer = StudentSerializer(students, many=True)
        
        # Return the JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubjectListView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Check if the data is a list (multiple subjects) or a single subject
        if isinstance(request.data, list):
            return self.create_multiple_subjects(request)
        else:
            return self.create_single_subject(request)
    
    def create_single_subject(self, request):
        """Handle creation of a single subject"""
        serializer = SubjectSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        program_id = request.data.get('program')
        student_id = request.data.get('student')
        
        if not Program.objects.filter(id=program_id).exists():
            return Response(
                {"program": [f"Program with ID {program_id} does not exist."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not Student.objects.filter(student_id=student_id).exists():
            return Response(
                {"student_id": [f"Student with ID {student_id} does not exist."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course_id = request.data.get('course_id')
        if Subject.objects.filter(course_id=course_id).exists():
            return Response(
                {"course_id": ["A subject with this course ID already exists."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subject = serializer.save()
        student = Student.objects.get(student_id=student_id)
        Enrollment.objects.create(student=student, course=subject)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def create_multiple_subjects(self, request):
        """Handle creation of multiple subjects"""
        response_data = []
        errors = []
        
        for idx, subject_data in enumerate(request.data):
            serializer = SubjectSerializer(data=subject_data)
            
            if not serializer.is_valid():
                errors.append({
                    'index': idx,
                    'errors': serializer.errors
                })
                continue
            
            program_id = subject_data.get('program')
            student_id = subject_data.get('student')
            
            # Validate program exists
            if not Program.objects.filter(id=program_id).exists():
                errors.append({
                    'index': idx,
                    'errors': {"program": [f"Program with ID {program_id} does not exist."]}
                })
                continue
            
            # Validate student exists
            if not Student.objects.filter(student_id=student_id).exists():
                errors.append({
                    'index': idx,
                    'errors': {"student_id": [f"Student with ID {student_id} does not exist."]}
                })
                continue
            
            # Validate course_id is unique
            course_id = subject_data.get('course_id')
            if Subject.objects.filter(course_id=course_id).exists():
                errors.append({
                    'index': idx,
                    'errors': {"course_id": ["A subject with this course ID already exists."]}
                })
                continue
            
            # If all validations pass, save the subject and create enrollment
            try:
                subject = serializer.save()
                student = Student.objects.get(student_id=student_id)
                Enrollment.objects.create(student=student, course=subject)
                response_data.append(serializer.data)
            except Exception as e:
                errors.append({
                    'index': idx,
                    'errors': str(e)
                })
        
        if errors:
            return Response({
                'message': 'Some subjects could not be created',
                'success_count': len(response_data),
                'fail_count': len(errors),
                'errors': errors,
                'created_subjects': response_data
            }, status=status.HTTP_207_MULTI_STATUS if response_data else status.HTTP_400_BAD_REQUEST)
        
        return Response(response_data, status=status.HTTP_201_CREATED)

    
class SoftwareEngineeringStudentsCoursesView(APIView):
    def get(self, request):
        """
        Retrieve all students enrolled in the Software Engineering program (program_id=1),
        along with their courses arranged by academic year and semester.
        """
        # Fetch the Software Engineering program using its fixed program_id
        try:
            software_engineering_program = Program.objects.get(program_id=1)
        except Program.DoesNotExist:
            return Response(
                {"error": "The Software Engineering program does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Query all students in the Software Engineering program
        students = Student.objects.filter(program=software_engineering_program)

        # Organize the response
        response_data = []

        for student in students:
            student_data = {
                "student_name": student.student_name,
                "program": software_engineering_program.program_name,
                "courses": {}
            }

            # Get all enrollments for the student
            enrollments = Enrollment.objects.filter(student=student).select_related('course')

            for enrollment in enrollments:
                course = enrollment.course
                year_key = f"Year {course.year}"
                semester_key = f"Semester {course.semester}"

                # Initialize year and semester keys if they don't exist
                if year_key not in student_data["courses"]:
                    student_data["courses"][year_key] = {}
                if semester_key not in student_data["courses"][year_key]:
                    student_data["courses"][year_key][semester_key] = []

                # Append course details to the corresponding year and semester
                student_data["courses"][year_key][semester_key].append({
                    "course_id": course.course_id,
                    "course_name": course.course_name
                })

            # Add the student's data to the response
            response_data.append(student_data)

        # Return the structured response
        return Response(response_data, status=status.HTTP_200_OK)
    
  
 
    
    
class EnrollmentListView(APIView):
    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if enrollment already exists
        student_id = request.data.get('student')
        course_id = request.data.get('course')
        
        if Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
            return Response(
                {"detail": "This student is already enrolled in this course."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        enrollment = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class SubjectListView(APIView):
#     def get(self, request):
#         subjects = Subject.objects.all()
#         serializer = SubjectSerializer(subjects, many=True)
#         return Response(serializer.data)  

#     def post(self, request):
#         # Handle both direct array and "subjects" key formats
#         data = request.data.get('subjects', request.data)
        
#         if isinstance(data, list):  # Handling multiple subjects
#             # First validate all entries
#             for subject_data in data:
#                 student_id = subject_data.get('student')
#                 program_id = subject_data.get('program')
                
#                 if not student_id or not Student.objects.filter(pk=student_id).exists():
#                     return Response(
#                         {"student": [f"Student with ID {student_id} does not exist."]}, 
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
                
#                 if not program_id or not Program.objects.filter(pk=program_id).exists():
#                     return Response(
#                         {"program": [f"Program with ID {program_id} does not exist."]}, 
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#             serializer = SubjectSerializer(data=data, many=True)
#         else:  # Handling a single subject
#             student_id = data.get('student')
#             program_id = data.get('program')
            
#             if not student_id or not Student.objects.filter(pk=student_id).exists():
#                 return Response(
#                     {"student": ["This field is required and must be a valid student ID."]}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             if not program_id or not Program.objects.filter(pk=program_id).exists():
#                 return Response(
#                     {"program": ["This field is required and must be a valid program ID."]}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             serializer = SubjectSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SubjectListViewByStudent(APIView):
#     def get(self, request, student_id):
#         try:
#             # Verify student exists
#             student = Student.objects.get(student_id=student_id)
            
#             # Get all subjects for this student
#             subjects = Subject.objects.filter(student=student)
            
#             serializer = SubjectSerializer(subjects, many=True)
#             return Response(serializer.data)
            
#         except Student.DoesNotExist:
#             return Response(
#                 {"error": f"Student with ID {student_id} not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Subject.DoesNotExist:
#             return Response(
#                 {"error": f"No subjects found for student with ID {student_id}"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
            
    
# class FilterSubjectsView(APIView):
#     def get(self, request):
#         student_id = request.query_params.get('student_id')
#         program_id = request.query_params.get('program_id')
        
#         subjects = Subject.objects.all()
        
#         if student_id and program_id:
#             subjects = subjects.filter(
#                 student__student_id=student_id,
#                 program__program_id=program_id
#             )
        
#         serializer = SubjectSerializer(subjects, many=True)
#         return Response(serializer.data)
    
  



