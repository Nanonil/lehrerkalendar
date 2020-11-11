from django.contrib import admin
from .models import Teacher, Day, Schoolclass, Students, Lesson, StudentGrading, Schedule, Period

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Day)
admin.site.register(Schoolclass)
admin.site.register(Students)
admin.site.register(Lesson)
admin.site.register(StudentGrading)
admin.site.register(Schedule)
admin.site.register(Period)
