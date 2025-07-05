from django.urls import path
from .views import index_view, submit_contact_form, submit_testimonial # Імпортуємо нову функцію
 

urlpatterns = [
    path('', index_view, name='index'),
    path('api/submit-form/', submit_contact_form, name='submit_contact_form'),
    path('api/submit-testimonial/', submit_testimonial, name='submit_testimonial'),
]