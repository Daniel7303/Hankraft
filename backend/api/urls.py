from django.urls import path
from . import views

urlpatterns = [
    # Public endpoints
    path('gallery/', views.public_gallery, name='public_gallery'),
    path('services/', views.public_services, name='public_services'),
    
    # Admin auth
    path('admin/login/', views.admin_login, name='admin_login'),
    
    # Admin gallery
    path('admin/gallery/', views.admin_gallery_list, name='admin_gallery_list'),
    path('admin/gallery/create/', views.admin_gallery_create, name='admin_gallery_create'),
    path('admin/gallery/<int:pk>/update/', views.admin_gallery_update, name='admin_gallery_update'),
    path('admin/gallery/<int:pk>/delete/', views.admin_gallery_delete, name='admin_gallery_delete'),
    
    # Admin services
    path('admin/services/', views.admin_services_list, name='admin_services_list'),
    path('admin/services/create/', views.admin_service_create, name='admin_service_create'),
    path('admin/services/<int:pk>/update/', views.admin_service_update, name='admin_service_update'),
    path('admin/services/<int:pk>/delete/', views.admin_service_delete, name='admin_service_delete'),
]