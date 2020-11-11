import django_tables2 as tables


class kalenderTable(tables.Table):

    stunden = tables.Column()
    #montag = tables.TemplateColumn('<a href="{{value}}">{{value}}</a>')
    montag = tables.Column(linkify=("dummy_view", [tables.A("montag")]))
    dienstag = tables.Column(linkify=("dummy_view", [tables.A("dienstag")]))
    mittwoch = tables.Column(linkify=("dummy_view", [tables.A("mittwoch")]))
    donnerstag = tables.Column(linkify=("dummy_view", [tables.A("donnerstag")]))
    freitag = tables.Column(linkify=("dummy_view", [tables.A("freitag")]))

    class Meta:
        orderable = False
        row_attrs = {"href": 'test/{{value}}'}
        show_header = False
        #Diasable header is it that simple?

