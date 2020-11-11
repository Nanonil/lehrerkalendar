from django.db import models

# Create your models here.
#Example
#class <table_name>(models.Model):
  #<coloumn_name> = models.<field_type>(<restrictions>)

class Teacher(models.Model):
    TeacherName = models.CharField(max_length=80) # Names will be limited to 80 characters

class Day(models.Model):
	DateOfDay = models.DateField()
	Weekday = models.IntegerField() # int from 1 to 5; 1 for Monday, 2 Tuesday, ..., 5 Friday

class Schoolclass(models.Model):
	ClassName = models.CharField(max=5) # Class Names are always 5 characters long (eg "FIA85")

class Students(models.Model):
	StudentName = models.CharField(max_length=80) # Names will be limited to 80 characters
	ClassID = models.ForeignKey(Schoolclass, on_delete=models.CASCADE)

class Period(models.Model):
    timeSpan = models.CharField(max_length=13) # eg "07:45 - 08:30"

class Lesson(models.Model):
	DayID = models.ForeignKey(Day, on_delete=models.CASCADE)
	ClassID = models.ForeignKey(Schoolclass, on_delete=models.CASCADE)
	Subject = models.CharField(max_length=50)
	PeriodID = models.ForeignKey(Period, on_delete=models.CASCADE) # int from 1 to 15; 1 '07:45-8:30'
	Content = models.TextField()
	Note = models.TextField()

class StudentGrading(models.Model):
	StudentID = models.ForeignKey(Students, on_delete=models.CASCADE)
	TeacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	DayID = models.ForeignKey(Day, on_delete=models.CASCADE)
	Grading = models.IntegerField() # int from 1 to 5
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['StudentID', 'TeacherID', 'DayID'], name='StudentGradingUnique')
		]

class Schedule(models.Model):
	TeacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	CalendarWeek = models.IntegerField()
	Year = models.IntegerField()
	Monday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Tuesday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Wednesday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Thursday = models.ForeignKey(Day, on_delete=models.CASCADE)
	Friday = models.ForeignKey(Day, on_delete=models.CASCADE)
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['TeacherID', 'CalendarWeek', 'Year'], name='UniqueSchedule')
		]