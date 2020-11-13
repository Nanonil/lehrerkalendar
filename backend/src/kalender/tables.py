import django_tables2 as tables



class kalenderTable(tables.Table):

    stunden = tables.Column()

    montag = tables.TemplateColumn('<a href="kalender/neue_stunde/tag/{{ days.montag }}/">{{value}}</a>')
    dienstag = tables.TemplateColumn('<a href="kalender/neue_stunde/tag/{{ days.dienstag }}/">{{value}}</a>')
    mittwoch = tables.TemplateColumn('<a href="kalender/neue_stunde/tag/{{ days.mittwoch }}/">{{value}}</a>')
    donnerstag = tables.TemplateColumn('<a href="kalender/neue_stunde/tag/{{ days.donnerstag }}/">{{value}}</a>')
    #freitag = tables.TemplateColumn('<a href="kalender/neue_stunde/tag/{{ days.freitag }}/">{{value}}</a>')
    freitag = tables.Column(linkify=("dummy_view", [tables.A('freitag')]))
    class Meta:
        orderable = False
        show_header = False

    def do(self):
        pass

class dayTabele(tables.Table):
    Stunde = tables.Column()
    Fach = tables.Column()
    Stundeninhalt = tables.Column()
    Notiz = tables.Column()

    class Meta:
        orderable = False

    
    
class searchTable(tables.Table):
    Datum = tables.Column()
    Fach = tables.Column()
    Stundeninhalt = tables.Column()
    Notiz = tables.Column()

    class Meta:
        orderable = False