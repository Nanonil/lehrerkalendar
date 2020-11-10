import django_tables2 as tables


class kalenderTable(tables.Table):

    stunden = tables.Column()
    #montag = tables.TemplateColumn('<a href="{{value}}">{{value}}</a>')
    montag = tables.Column(linkify=("test_view", [tables.A("montag")]))
    dienstag = tables.Column()
    mittwoch = tables.Column()
    donnerstag = tables.Column()
    freitag = tables.Column()

    class Meta:
        orderable = False
        row_attrs = {"href": 'ANW'}
        show_header = False
        #Diasable header is it that simple?

