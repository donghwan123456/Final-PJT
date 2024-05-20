# myapp/views.py

from django.shortcuts import redirect, render

def map_view(request):
    return render(request, 'myapp/map.html')

# def home_redirect(request):
#     return redirect('/map/')
