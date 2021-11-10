from django.shortcuts import render

def home_page(request):
    homePagePath = 'home.html'
    context = {'Message' : 'Home Page'}
    return render(request, 'home.html', context)

def astro_projection(request):
    context = {}
    return render(request, 'astroProjection.html', context)