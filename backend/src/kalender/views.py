from django.shortcuts import render
from kalender.tables import kalenderTable
from kalender.constants import hours, headings
# Create your views here.
def kalender_view(request, *args, **kwargs):

	list = []
	headingsList = {}
	for heading in headings:
		headingsList.update({heading : heading})

	list.append(headingsList)
	for hour in hours:
		list.append({headings[0]: hour, headings[1]: 'ANW', headings[2]: '', headings[3]: '', headings[4]: '', headings[5]: ''})

	table = kalenderTable(list)


	return render(request, "html/calendar.html", {'table': table})






def tages_view(request, *args, **kwargs):

	table = {
		[

		]
	}

	return render(request, "html/day.html", {})

#ignore this one
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
def test_view(request, *args, **kwargs):
	return "Test"