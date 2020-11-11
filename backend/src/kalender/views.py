from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from .tables import kalenderTable
from .constants import hours, headings
from .forms import DatepickerForm


# Create your views here.
def kalender_view(request, *args, **kwargs):
    user = auth.get_user(request=request)

    #making sure the User is logged in
    if not is_user_logged_in(user):
        #Redirect User to login page
        return redirect("/login")

    #Checking if a date has already been selected
    if request.path.__contains__("date"):
        date = request.GET['date']
        print(date)


    form = DatepickerForm(request.POST or None)
    if form.is_valid():
        form.save()

    list = []
    headingsList = {}
    for heading in headings:
        headingsList.update({heading: heading})
    list.append(headingsList)

    # Just dummy data
    for hour in hours:
        list.append(
            {headings[0]: hour, headings[1]: 'ANW', headings[2]: '', headings[3]: '', headings[4]: '', headings[5]: ''})

    # Make sure all empty spaces are replaced with 'neue Stunde'
    for row in list:
        for element in row.keys():
            if row[element] == '':
                row[element] = 'neue Stunde'

    table = kalenderTable(list)
    context = {
        'table': table,
        'form': form,
    }
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




#Just an empty dummy view to assign when no view is implemented yet for the element
def dummy_view(request):
    return "dummy"


#Helper methods

def is_user_logged_in(user):
    if user.is_anonymous:
        return False
    else:
        return True