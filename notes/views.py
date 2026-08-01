import datetime
from django.http import HttpResponse



def hello_from_notes_app(request):
    return HttpResponse("Hello, from Notes app!")

#def current_time(request):
    now= datetime.datetime.now()
    html = f"<h1>Поточний час</h1><p>Зараз: {now.strftime('%Y-%m-%d %H:%M:%S')}</p>"
    return HttpResponse(html)