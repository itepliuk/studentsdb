"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from students.views import (
    students, groups, journal, exams, ratings, contact_admin)



urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #Students urls
    url(r'^$', students.students_list, name='home'),
    url(r'^students/add/$', students.students_add, name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', students.StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', students.StudentDeleteView.as_view(), name='students_delete'),
    url(r'^students/(?P<pk>\d+)/$', students.StudentDetailView.as_view(), name='students_detail'),

    #Groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    url(r'^groups/add/$', groups.groups_add, name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', groups.groups_delete, name='groups_delete'),
    url(r'^groups/(?P<pk>\d+)/$', groups.groups_detail, name='groups_detail'),


    #Exams urls
    url(r'^exams/$', exams.exams_list, name='exams'),
    url(r'^exams/add/$', exams.exams_add, name='exams_add'),

    #Ratings urls
    url(r'^ratings/$', ratings.ratings_list, name='ratings'),
    url(r'^ratings/add/$', ratings.ratings_add, name='ratings_add'),
    url(r'^ratings/(?P<pk>\d+)/edit/$', ratings.ratings_edit, name='ratings_edit'),
    url(r'^ratings/(?P<pk>\d+)/delete/$', ratings.ratings_delete, name='ratings_delete'),

    #Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', journal.JournalView.as_view(), name='journal'),

    #Contact Admin Form
    #url(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),
    url(r'^contact-admin/$', contact_admin.ContactView.as_view(), name='contact_admin'),
    
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)