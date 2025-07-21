from django.shortcuts import render

# Create your views here.
def bouldering_home(request):
    return render(request, 'bouldering/bouldering-home-page.html')