from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gallery import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.gallery, name='gallery'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_photo, name='upload'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete'),
    path('lang/<str:lang_code>/', views.set_language, name='set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)