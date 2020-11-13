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
    TEMPLATE = """
        <input id="count" maxlength="100" name="count" value="" onfocusout="myFunction()" type="text"/>
        """

    day = "Montag"
    Stunde = tables.Column()
    Fach = tables.Column()
    Stundeninhalt = tables.TemplateColumn(TEMPLATE)
    Notiz = tables.TemplateColumn(TEMPLATE)

    class Meta:
        orderable = False

    
    
class searchTable(tables.Table):
    TEMPLATE = """
        
        """

    Datum = tables.Column()
    Fach = tables.Column()
    Stundeninhalt = tables.TemplateColumn(TEMPLATE)
    Notiz = tables.TemplateColumn(TEMPLATE)

    class Meta:
        orderable = False