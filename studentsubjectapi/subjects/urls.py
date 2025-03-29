from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import FilterStudentsView, ProgramListView, SoftwareEngineeringStudentsCoursesView, StudentListView, SubjectListView

urlpatterns = [

    path('programs/', ProgramListView.as_view(), name='programs-list'),
    path('students/list/', StudentListView.as_view(), name='students-list'),
    path('students/', FilterStudentsView.as_view(), name='filter-students-list'),
    path('subjects/list/', SubjectListView.as_view(), name='subjects-list'),
    # path('students/<int:student_id>/subjects/', FilterSubjectsView.as_view(), name='student-subjects'),
    path('subjects/', SoftwareEngineeringStudentsCoursesView.as_view(), name='software-engineering-students-courses'),

    # path('subjects/filter/', FilterSubjectsView.as_view(), name='filter-subjects'),
    # path('students/<str:student_id>/subjects/', SubjectListViewByStudent.as_view(), name='student-subjects'),
]

# Static file serving for passport images (media files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

