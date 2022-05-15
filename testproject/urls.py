"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = "index"),
    path('index.html', views.index, name = "index"),
    path('saisie.html', views.saisie, name = "saisie"),
    path('<marquepage>', views.car, name = "marquepage"),  
    
    
    path('about.html', views.about, name = "about"),
    
    
    path('<str:logospage>', views.logos, name = "logospage"),
    path('contact.html', views.contact, name = "contact"),
    path('main.html', views.main, name = "main"),
    path('/<marquesLinks>', views.car_details, name = "marquesLinks"),
    path('a/<recpage>', views.rec, name = "recpage"),

    path('/page/<blogpages>', views.blog, name = "blogpages"),
    path('details/page/<blogDetails>', views.blog_details, name = "blogDetails"),

    path('/1/2/3/<pageNbr>', views.saisieOccasion, name = "pageNbr"),
    path('1/2/3/4/<detailsLink>', views.occasion_details, name = "detailsLink"),

    path('1/2/3/4/5/statistics.html', views.statistics, name = "statistics"),
    path('1/2/3/4/5/6/<linkPage>', views.paginationOccasion, name="linkPage"),

    path('1/2/3/4/5/6/7/comparaison.html', views.comparaison, name = "comparaison"),
    
]
