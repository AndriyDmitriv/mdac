from django.urls import path
from .views import index_view, submit_contact_form # Імпортуємо нову функцію
 

urlpatterns = [
    path('', index_view, name='index'),
    path('api/submit-form/', submit_contact_form, name='submit_contact_form'),

]