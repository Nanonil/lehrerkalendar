from django.shortcuts import render
from .tables import kalenderTable
from .constants import hours, headings
from .forms import DatepickerForm
# Create your views here.
def kalender_view(request, *args, **kwargs):
	form = DatepickerForm(request.POST or None)
	if form.is_valid():
		form.save()

	list = []
	headingsList = {}
	for heading in headings:
		headingsList.update({heading : heading})
	list.append(headingsList)

	#Just dummy data
	for hour in hours:
		list.append({headings[0]: hour, headings[1]: 'ANW', headings[2]: '', headings[3]: '', headings[4]: '', headings[5]: ''})

	#Make sure all empty spaces are replaced with 'neue Stunde'
	for row in list:
		for element in row.keys():
			if row[element] == '':
				row[element] = 'neue Stunde'

	print(list)
	table = kalenderTable(list)
	context = {
		'table': table,
		'form': form,
	}
	return render(request, "html/calendar.html", context)






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