from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from datetime import date as dateTime
from datetime import timedelta
import datetime

from .tables import kalenderTable, dayTabele
from .constants import hours, headings, dayHeadings
from .forms import DatepickerForm
from .models import *


# Create your views here.

def kalender_view(request):
    context = {}
    user = auth.get_user(request=request)
    currentTeacher = Teacher.objects.filter(TeacherName=user.get_username())
    if not is_user_logged_in(user):
        # Redirect User to login page
        return redirect("/login")
    if request.path.__contains__("date"):
        # The User has already choosen a date
        defaultDate = request.GET['date']
    else:
        # The user has not choosen a date yet, so we just put the date of today
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

    context.update({
        "table": table,
        "tableHead": tableHead,
        "tableDates": get_week_days(defaultDate)
    })
    return render(request, "html/calendar.html", context)


def kalender_view_deprached(request, *args, **kwargs):
    # making sure the User is logged in
    user = auth.get_user(request=request)
    currentTeacher = None
    if not is_user_logged_in(user):
        # Redirect User to login page
        return redirect("/login")

    # init all datas
    table = None
    form = {}
    context = {}
    currentTeacher = Teacher.objects.filter(TeacherName=user.get_username())

    # Checking if a date has already been selected
    if request.path.__contains__("date"):
        # The User has already choosen a date
        defaultDate = request.GET['date']
    else:
        # The user has not choosen a date yet, so we just put the date of today
        defaultDate = dateTime.today()

    # Create the Datepicker since we always need it
    form = DatepickerForm(request.POST or None)

    if form.is_valid():
        form.save()

    # Create the Table and get all necessary data
    kalenderRowList = []

    # Get all datas from the database
    calendarWeek = datetime.date(defaultDate.year, defaultDate.month, defaultDate.day).isocalendar()[1]
    scheudle = Schedule.objects.filter(TeacherID=currentTeacher[0].id, CalendarWeek=calendarWeek, Year=defaultDate.year)

    monday = Lesson.objects.filter(DayID=scheudle[0].Monday.id)
    tuesday = Lesson.objects.filter(DayID=scheudle[0].Tuesday.id)
    wednesday = Lesson.objects.filter(DayID=scheudle[0].Wednesday.id)
    thursday = Lesson.objects.filter(DayID=scheudle[0].Thursday.id)
    friday = Lesson.objects.filter(DayID=scheudle[0].Friday.id)

    days = get_week_days(defaultDate)
    counter = 0
    headingsList = {}
    datumList = {}
    for heading in headings:
        if counter == 0:
            headingsList.update({heading: heading})
            datumList.update({heading: "Datum"})
        else:
            headingsList.update({heading: heading})
            datumList.update({heading: str(days[counter - 1])})

        counter += 1
    kalenderRowList.append(datumList)
    kalenderRowList.append(headingsList)

    counter = 1
    for hour in hours:
        aRow = {}

        aRow.update({
            headings[0]: hour
        })

        try:
            aRow.update({
                headings[1]: monday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].Subject + " " +
                             monday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].ClassID.ClassName
            })
        except:
            aRow.update({headings[1]: 'neue Stunde'})

        try:
            aRow.update({
                headings[2]: tuesday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].Subject + " " +
                             tuesday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].ClassID.ClassName
            })
        except:
            aRow.update({headings[2]: 'neue Stunde'})

        try:
            aRow.update({
                headings[3]: wednesday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].Subject + " " +
                             wednesday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].ClassID.ClassName
            })
        except:
            aRow.update({headings[3]: 'neue Stunde'})

        try:
            aRow.update({
                headings[4]: thursday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].Subject + " " +
                             thursday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].ClassID.ClassName})
        except:
            aRow.update({headings[4]: 'neue Stunde'})

        try:
            aRow.update({
                headings[5]: friday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].Subject + " " +
                             friday.filter(PeriodID=Period.objects.filter(id=counter)[0].id)[0].ClassID.ClassName})
        except:
            aRow.update({headings[5]: 'neue Stunde'})

        kalenderRowList.append(aRow)
        counter += 1
    table = kalenderTable(kalenderRowList)
    # Create List of all classes
    classes = []
    classesFromDB = Schoolclass.objects.all()

    for aClass in classesFromDB:
        classes.append(aClass.ClassName)

    # Add date of each day
    dates_of_weekdays = {
        "montag": days[0],
        "diesntag": days[1],
        "mittwoch": days[2],
        "donnerstag": days[3],
        "Freitag": days[4]
    }

    context.update({'classes': classes})
    context.update({'table': table})
    context.update({'form': form})
    context.update({'days': dates_of_weekdays})

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
    return render(request, "html/test.html", {})


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
    context = {
        "fach": "ANW",
        "klasse": "FIA85",
        "inhalt": "moin",
        "notiz": "jo"
    }

    return render(request, "html/hour.html", context)


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


def tages_view(request, *args, **kwargs):
    list = []
    data = [
        {dayHeadings[0]: "1.-2.", dayHeadings[1]: "ANW", dayHeadings[2]: "QS", dayHeadings[3]: "12345"},
        {dayHeadings[0]: "3.-4.", dayHeadings[1]: "ITK", dayHeadings[2]: "Netzwerke", dayHeadings[3]: "12345"},
        {dayHeadings[0]: "5.-6.", dayHeadings[1]: "Deutsch", dayHeadings[2]: "PoB", dayHeadings[3]: "12345"}
    ]

    for row in data:
        list.append(row)
    table = dayTabele(list)
    return render(request, "html/day.html", {'table': table})


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
