from django.db import models

# Create your models here.
#Example
#class <table_name>(models.Model):
  #<coloumn_name> = models.<field_type>(<restrictions>)

class Teacher(models.Model):
    TeacherName = models.CharField(max_length=80)

class Day(models.Model):
	DateOfDay = models.DateField()
	Weekday = models.IntegerField()

class Schoolclass(models.Model):
	ClassName = models.CharField()

class Students(models.Model):
	StudentName = models.CharField(max_length=80)
	ClassID = models.ForeignKey(Schoolclass, on_delete=models.CASCADE)

class Lesson(models.Model):
	DayID = models.ForeignKey(Day, on_delete=models.CASCADE)
	ClassID = models.ForeignKey(Schoolclass, on_delete=models.CASCADE)
	Subject = models.CharField(max_length=50)
	Period = models.IntegerField()
	Content = models.TextField()
	Note = models.TextField()

class StudentGrading(models.Model):
	StudentID = models.ForeignKey(Students, on_delete=models.CASCADE)
	TeacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	LessonID = models.ForeignKey(Lesson, on_delete=models.CASCADE)
	Grading = models.IntegerField()

class Schedule(models.Model):
	TeacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	CalendarWeek = models.IntegerField()
	Year = models.IntegerField()
	Monday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Tuesday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Wednesday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Thursday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Friday = models.ForeignKey(Day, on_delete=models.CASCADE)