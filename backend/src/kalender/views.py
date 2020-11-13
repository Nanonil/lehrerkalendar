from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from datetime import date as dateTime
from datetime import timedelta
import datetime

from .tables import kalenderTable, dayTabele, searchTable
from .constants import hours, headings, dayHeadings, searchHeadings
from .forms import DatepickerForm, ClassForm
from .models import *


# Create your views here.

def kalender_view(request):
    context = {}
    user = auth.get_user(request=request)
    currentTeacher = Teacher.objects.filter(TeacherName=user.get_username())
    if not is_user_logged_in(user):
        # Redirect User to login page
        return redirect("/login")

    try:
        defaultDate = dateTime.fromisoformat(request.POST["weekDate"])
    except:
        defaultDate = dateTime.today()

    # get all data for the table
    calendarWeek = datetime.date(defaultDate.year, defaultDate.month, defaultDate.day).isocalendar()[1]
    scheudle = Schedule.objects.filter(TeacherID=currentTeacher[0].id, CalendarWeek=calendarWeek, Year=defaultDate.year)

    monday = Lesson.objects.filter(DayID=scheudle[0].Monday.id)
    tuesday = Lesson.objects.filter(DayID=scheudle[0].Tuesday.id)
    wednesday = Lesson.objects.filter(DayID=scheudle[0].Wednesday.id)
    thursday = Lesson.objects.filter(DayID=scheudle[0].Thursday.id)
    friday = Lesson.objects.filter(DayID=scheudle[0].Friday.id)
    # create the Table
    table = []
    counter = 0
    for hour in hours:
        aHour = {}

        aHour.update({"time": hour.split(" ")[1]})
        aHour.update({"stunden": hour.split(" ")[0]})
        aHour.update({"stundenstripped": hour.split(" ")[0].replace(".", "")})

        try:
            aHour.update({"montag": monday[counter].Subject})
        except:
            aHour.update({"montag": "neu"})

        try:
            aHour.update({"dienstag": tuesday[counter].Subject})
        except:
            aHour.update({"dienstag": "neu"})

        try:
            aHour.update({"mittwoch": wednesday[counter].Subject})
        except:
            aHour.update({"mittwoch": "neu"})

        try:
            aHour.update({"donnerstag": thursday[counter].Subject})
        except:
            aHour.update({"donnerstag": "neu"})

        try:
            aHour.update({"freitag": friday[counter].Subject})
        except:
            aHour.update({"freitag": "neu"})
        counter += 1
        table.append(aHour)
    tableHead = {"stunden": headings[0], "montag": headings[1], "dienstag": headings[2], "mittwoch": headings[3],
                 "donnerstag": headings[4], "freitag": headings[5]}

    schoolClasses = Schoolclass.objects.all()
    classes = []
    for schoolClass in schoolClasses:
        classes.append(schoolClass.ClassName)

    context.update({
        "table": table,
        "tableHead": tableHead,
        "tableDates": get_week_days(defaultDate),
        "date": str(defaultDate),
        "classes": classes
    })
    return render(request, "html/calendar.html", context)


def login_redirect_view(request):
    return redirect("/login")


def login_view(request):
    if request.method == 'POST':
        print('This is a post')
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        # If User is not available user will be None
        if user is not None:
            auth.login(request, user)
            assure_that_user_is_in_custom_db(user)

            return redirect("/home")
        else:
            return redirect("/login_error")
    else:
        print('This was not a post')
        return render(request, "login.html", {})


def home_view(request):
    user = auth.get_user(request=request)
    if not is_user_logged_in(user):
        return redirect("/login")
    return render(request, "html/home.html", {})


def neue_stunde_view(request):
    allClasses = Schoolclass.objects.all()
    hours = request.POST['hours']
    date = request.POST['date']
    isNew = False

    try:
        request.POST["hasSubject"]
        isNew = False
    except:
        isNew = True

    if isNew:
        allClassNames = []
        for schoolClass in allClasses:
            allClassNames.append(schoolClass.ClassName)

        context = {
            'date': date,
            'hour': hours,
            'klassenList': allClassNames
        }
        return render(request, "html/createLesson.html", context)
    else:
        return redirect("/kalender/stunde/" + str(Period.objects.filter(timeSpan=hours)[0].id))


def neue_stunde_save(request):
    dayID = Day.objects.filter(DateOfDay=request.POST["date"])[0]
    classID = Schoolclass.objects.filter(ClassName=request.POST["klassen"])[0]
    subject = request.POST["fach"]
    periodID = Period.objects.filter(timeSpan=request.POST["hour"])[0]
    content = ""
    note = ""
    neueStunde = Lesson(DayID=dayID, ClassID=classID, Subject=subject, PeriodID=periodID, Content=content, Note=note)
    neueStunde.save()

    return redirect("/kalender/stunde/" + str(neueStunde.id))


# Just an empty dummy view to assign when no view is implemented yet for the element
def dummy_view(request):
    return "dummy"


# Helper methods
def is_user_logged_in(user):
    if user.is_anonymous:
        return False
    else:
        return True


def assure_that_user_is_in_custom_db(user):
    teachers = Teacher.objects.all()

    if len(teachers) == 0:
        teacher = Teacher(TeacherName=user.get_username())
        teacher.save()
    else:
        for teacher in teachers:
            if teacher == user.get_username():
                return
            teacher = Teacher(TeacherName=user.get_username())


def stunden_view(request, *args, **kwargs):
    hourID = kwargs['hour']
    lesson = Lesson.objects.get(id=hourID)
    context = {
        "fach": lesson.Subject,
        "klasse": lesson.ClassID.ClassName,
        "inhalt": lesson.Content,
        "notiz": lesson.Note
    }

    return render(request, "html/hour.html", context)


def tages_view(request, *args, **kwargs):
    list = []
    allLessons = Lesson.objects.all()
    allLessonsAtDate = []
    currentDayId = Day.objects.filter(DateOfDay=request.POST["date"])[0].id
    for lesson in allLessons:
        if lesson.DayID.id == currentDayId:
            allLessonsAtDate.append(lesson)



    for hour in hours:
        for lesson in allLessonsAtDate:
            if lesson.PeriodID.id == Period.objects.filter(timeSpan=hour.split(" ")[1])[0].id:
                thisLesson = lesson
        aRow = {dayHeadings[0]: hour.split(" ")[0], dayHeadings[1]: thisLesson.Subject,
                dayHeadings[2]: thisLesson.Content, dayHeadings[3]: thisLesson.Note}
        list.append(aRow)

    table = dayTabele(list)
    return render(request, "html/day.html", {'table': table})


def test_view(request):
    return redirect('/kalender')


def save_students_view(request):
    return redirect('/kalender')


def schueler_view(request, *args, **kwargs):
    context = {
        "students": [
            {
                "name": "Nils",
                "rating1": "1",
                "rating2": "2",
                "rating3": "3",
                "rating4": "4",
                "rating5": "5",

            }
        ]
    }
    return render(request, "html/students.html", context)


def search_view(request, *args, **kwargs):
    form = ClassForm()

    context = {
        "form": form,
        "table": searchTable([])
    }

    if request.GET:
        classId = request.GET['Klasse']
        lessons = Lesson.objects.filter(ClassID=classId).order_by('-DayID__DateOfDay')
        data = []
        for lesson in lessons:
            data.append(
                {searchHeadings[0]: Day.objects.get(id=lesson.DayID.id).DateOfDay, searchHeadings[1]: lesson.Subject,
                 searchHeadings[2]: lesson.Content, searchHeadings[3]: lesson.Note})
        table = searchTable(data)
        context['table'] = table

    return render(request, 'html/search.html', context)


def get_week_days(today):
    if today.weekday() == 0:
        return [(today + timedelta(days=0)).isoformat(),
                (today + timedelta(days=1)).isoformat(),
                (today + timedelta(days=2)).isoformat(),
                (today + timedelta(days=3)).isoformat(),
                (today + timedelta(days=4)).isoformat()
                ]
    elif today.weekday() == 1:
        return [(today + timedelta(days=-1)).isoformat(),
                (today + timedelta(days=0)).isoformat(),
                (today + timedelta(days=1)).isoformat(),
                (today + timedelta(days=2)).isoformat(),
                (today + timedelta(days=3)).isoformat(),
                ]
    elif today.weekday() == 2:
        return [(today + timedelta(days=-2)).isoformat(),
                (today + timedelta(days=-1)).isoformat(),
                (today + timedelta(days=0)).isoformat(),
                (today + timedelta(days=1)).isoformat(),
                (today + timedelta(days=2)).isoformat(),
                ]
    elif today.weekday() == 3:
        return [(today + timedelta(days=-3)).isoformat(),
                (today + timedelta(days=-2)).isoformat(),
                (today + timedelta(days=-1)).isoformat(),
                (today + timedelta(days=0)).isoformat(),
                (today + timedelta(days=1)).isoformat(),
                ]
    elif today.weekday() == 4:
        return [(today + timedelta(days=-4)).isoformat(),
                (today + timedelta(days=-3)).isoformat(),
                (today + timedelta(days=-2)).isoformat(),
                (today + timedelta(days=-1)).isoformat(),
                (today + timedelta(days=0)).isoformat(),
                ]
