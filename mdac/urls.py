from django.contrib import admin
from django.urls import path, include # <-- Додаємо 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Для шляху '/admin/' буде, як і раніше, відповідати адмін-панель.
    path('admin/', admin.site.urls),

    # Для всіх інших шляхів (включаючи головну сторінку '/')
    # Django буде шукати відповідності у файлі main/urls.py
    path('', include('main.urls')),
]

# Ця частина залишається без змін, вона потрібна для відображення медіафайлів
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)