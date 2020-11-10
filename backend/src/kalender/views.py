from django.shortcuts import render


# Create your views here.
def kalendar_view(request, *args, **kwargs):
	hours = ["1.-2. 07:45-09:15",
			 "3.-4. 09:35-11:05",
			 "5.-6. 11:25-12:55",
			 "7.-8. 13:15-14:45",
			 "9.-10. 15:05-16:35",
			 "11.-13. 16:55-19:10",
			 "14.-15. 19:30-21:00"]
	headings = ["stunden", "montag", "dienstag", "mittwoch", "donnerstag", "freitag"]

	rows = []
	context = {
		"rows": rows,
		"headings": headings
	}
	counter = 0
	for hour in hours:
		hourDictionary = {
			headings[0]: hour,
			headings[1]: "Fach1",
			headings[2]: "Fach2",
			headings[3]: "Fach3",
			headings[4]: "Fach4",
			headings[5]: "Fach5"}
		rows.append(hourDictionary)
		hourDictionary[headings[0]]
		counter += 1

	return render(request, "html/calendar.html", context)


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
