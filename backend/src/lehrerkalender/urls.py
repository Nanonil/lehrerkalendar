"""lehrerkalender URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kalender.views import save_students_view, stunden_view, test_view, kalender_view, login_view, home_view, \
    login_redirect_view, dummy_view, schueler_view, tages_view, search_view, neue_stunde_view, neue_stunde_save, \
    stunde_speichern
urlpatterns = [

    #Login and login redirect path
    path('login', login_view, name='login'),
    path('', login_redirect_view, name='login_redirect'),

    #The Path tot he entry of the both apps
    path('kalender', kalender_view),
    #path('schueler', schueler_view), not activated because not implemented

    #Path to the home of the Website, from here the User can decide which app to use
    path('home', home_view, name='home_view'),

    #Path for all views reachable from the Kalendar
    path('kalender/new/tag/<str:hours>/date/<str:date>', neue_stunde_view, name='neue_stunde' ),
    path('kalender/newLesson', neue_stunde_view, name='neue_stunde'),
    path('kalender/newLesson/save', neue_stunde_save, name='neue_stunde_save'),



    path('kalender/stunde/save', stunde_speichern),




    #Admin views
    path('admin/', admin.site.urls),



    #From Branch Tara
    path('schueler/', schueler_view),
    path('kalender/day', tages_view, name='tag'),
    path('test/<str:tag>', test_view, name='test_view'),
    path('kalender/stunde/<str:hour>', stunden_view),
    path('saveInhalt/', test_view),
    path('saveStudents/', save_students_view),

    #Search View to search by class
    path('kalender/search/', search_view),
    #path('kalender/search/?Klasse=1', dummy_view),

    #This is just a dummy view assigned wherever a view is not ready/implemented yet
    path('dummy_view', dummy_view, name='dummy_view'),
    path('dummy_view/<str:stunden>/<str:Datum>', dummy_view, name='dummy_view'),
    path('dummy_view/<str:stunden>', dummy_view, name='dummy_view'),
    path('function/<str:function>/tag/<str:tag>/stunden/<str:stunden>', dummy_view, name='tag')
]
