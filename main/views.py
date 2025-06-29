from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import (
    SiteConfiguration, MenuItem, SectionBackground, Service, 
    ServiceCategoryInfo, Advantage, Result, Testimonial, AlgorithmStep, 
    FAQ, Bonus, ContactRequest, HeroBanner
)

# Ця функція тепер буде віддавати головну сторінку
def index_view(request):
    site_config = SiteConfiguration.get_solo()
    menu_items = MenuItem.objects.all()
    divorce_services = Service.objects.filter(category='DIVORCE')
    alimony_services = Service.objects.filter(category='ALIMONY')
    divorce_info = ServiceCategoryInfo.objects.filter(category='DIVORCE').first()
    alimony_info = ServiceCategoryInfo.objects.filter(category='ALIMONY').first()
    advantages = Advantage.objects.all()
    results = Result.objects.all()
    testimonials = Testimonial.objects.filter(is_published=True)
    algorithm_steps = AlgorithmStep.objects.all()
    faqs = FAQ.objects.filter(is_published=True)
    bonuses = Bonus.objects.filter(is_active=True)
    backgrounds_qs = SectionBackground.objects.all()
    backgrounds = {bg.name: bg.background_image.url for bg in backgrounds_qs}
    hero_banner = HeroBanner.get_solo()   
    header_carousel_texts = [
        site_config.header_carousel_text_1,
        site_config.header_carousel_text_2,
        site_config.header_carousel_text_3,
    ]

    context = {
        'site_config': site_config,
        'menu_items': menu_items,
        'header_carousel_texts': header_carousel_texts,
        'divorce_services': divorce_services,
        'alimony_services': alimony_services,
        'divorce_info': divorce_info,
        'alimony_info': alimony_info,
        'advantages': advantages,
        'results': results,
        'testimonials': testimonials,
        'algorithm_steps': algorithm_steps,
        'faqs': faqs,
        'bonuses': bonuses,
        'backgrounds': backgrounds,
        'hero': hero_banner,    
    }
    return render(request, 'index.html', context)

# ▼▼▼ НОВА ФУНКЦІЯ для обробки форми ▼▼▼
def submit_contact_form(request):
    if request.method == 'POST':
        try:
            # Отримуємо дані з тіла POST-запиту
            data = json.loads(request.body)
            situation = data.get('situation')
            name = data.get('name')
            phone = data.get('phone')

            # Створюємо і зберігаємо заявку в базі даних
            ContactRequest.objects.create(
                situation=situation,
                name=name,
                phone_number=phone
            )
            
            # Надсилаємо успішну відповідь
            return JsonResponse({'status': 'success', 'message': 'Заявку успішно відправлено!'})
        except Exception as e:
            # Надсилаємо відповідь з помилкоюпи
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Якщо це не POST-запит, повертаємо помилку
    return JsonResponse({'status': 'error', 'message': 'Неправильний метод запиту'}, status=405)