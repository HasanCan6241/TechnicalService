from django.urls import path
from . import views
from .views import VideoGalleryView

app_name = 'mainapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('service_request/', views.service_request, name='service_request'),
    path('hizmetler/', views.services, name='services'),
    path('iletisim/', views.contact, name='contact'),
    path('about/',views.about,name='about'),
    path('combi_service/',views.combi_service,name='combi_service'),
    path('boiler_service/', views.boiler_service, name='boiler_service'),
    path('su_aritma/', views.su_aritma, name='su_aritma'),
    path('sofben_bakimi/', views.sofben_bakimi, name='sofben_bakimi'),
    path('airconditioning/', views.airconditioning, name='airconditioning'),
    path('repair/', views.repair, name='repair'),
    path('eca-about/', views.eca_about, name='eca-about'),
    path('viessmann-about/', views.viessmann_about, name='viessmann-about'),
    path('immergas-about/', views.immergas_about, name='immergas-about'),
    path('videolar/', VideoGalleryView.as_view(), name='video_gallery'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('marka/<slug:slug>/', views.BrandDetailView.as_view(), name='brand-detail'),

]