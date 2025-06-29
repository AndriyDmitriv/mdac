from django.db import models
from solo.models import SingletonModel

class SiteConfiguration(SingletonModel):
    header_logo_text = models.CharField(max_length=50, default="ЛОГОТИП", verbose_name="Текст логотипу в хедері")
    header_carousel_text_1 = models.CharField(max_length=50, default="під ключ", verbose_name="Текст каруселі 1")
    header_carousel_text_2 = models.CharField(max_length=50, default="онлайн", verbose_name="Текст каруселі 2")
    header_carousel_text_3 = models.CharField(max_length=50, default="24/7", verbose_name="Текст каруселі 3")
    footer_logo_text = models.CharField(max_length=50, default="ЛОГОТИП", verbose_name="Текст логотипу в футері")
    footer_tagline = models.TextField(verbose_name="Текст-слоган у футері")
    footer_contacts_title = models.CharField(max_length=50, default="КОНТАКТИ", verbose_name="Заголовок 'Контакти' у футері")
    footer_phone = models.CharField(max_length=20, verbose_name="Номер телефону у футері")
    footer_email = models.EmailField(verbose_name="Email у футері")
    footer_cta_text = models.CharField(max_length=100, default="Безкоштовна консультація", verbose_name="Текст кнопки у футері")
    footer_cta_link = models.CharField(max_length=200, default="#", verbose_name="Посилання для кнопки у футері")
    divorce_section_title = models.CharField(max_length=100, default="РОЗІРВАННЯ ШЛЮБУ", verbose_name="Заголовок секції 'Розірвання шлюбу'")
    alimony_section_title = models.CharField(max_length=100, default="СТЯГНЕННЯ АЛІМЕНТІВ", verbose_name="Заголовок секції 'Стягнення аліментів'")
    packages_subtitle = models.CharField(max_length=100, default="Пакети послуг", verbose_name="Підзаголовок 'Пакети послуг'")
    advantages_section_title = models.CharField(max_length=100, default="НАШІ ПЕРЕВАГИ", verbose_name="Заголовок секції 'Переваги'")
    results_section_title = models.CharField(max_length=100, default="НАШІ РІШЕННЯ", verbose_name="Заголовок секції 'Рішення'")
    results_section_subtitle = models.CharField(max_length=100, default="ЗА 2022-2025 РІК", verbose_name="Підзаголовок секції 'Рішення'")
    results_button_text = models.CharField(max_length=50, default="Переглянути всі", verbose_name="Текст кнопки 'Переглянути всі'")
    testimonials_section_title = models.CharField(max_length=100, default="ВІДГУКИ КЛІЄНТІВ", verbose_name="Заголовок секції 'Відгуки'")
    algorithm_section_title = models.CharField(max_length=100, default="АЛГОРИТМ СПІВПРАЦІ З НАМИ", verbose_name="Заголовок секції 'Алгоритм'")
    faq_section_title = models.CharField(max_length=100, default="ЧАСТІ ЗАПИТАННЯ", verbose_name="Заголовок секції 'Часті запитання'")
    bonuses_section_title = models.CharField(max_length=100, default="АКЦІЇ ТА БОНУСИ", verbose_name="Заголовок секції 'Бонуси'")
    contact_form_title = models.CharField(max_length=100, default="Задати інше запитання", verbose_name="Заголовок контактної форми")
    contact_form_subtitle = models.TextField(verbose_name="Підзаголовок контактної форми")
    
    def __str__(self):
        return "Налаштування Сайту"

    class Meta:
        verbose_name = "0. Налаштування Сайту"
        verbose_name_plural = "0. Налаштування Сайту"


# --- Інші моделі ---

class MenuItem(models.Model):
    text = models.CharField(max_length=50, verbose_name="Текст пункту меню")
    link = models.CharField(max_length=200, verbose_name="Посилання (напр. #results)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    
    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "1. Пункт меню"
        verbose_name_plural = "1. Пункти меню"
        ordering = ['order']

class HeroBanner(SingletonModel): 
    title = models.TextField(verbose_name="Головний заголовок")
    button1_text = models.CharField(max_length=50, verbose_name="Текст кнопки 1")
    button1_link = models.CharField(max_length=200, default="#", verbose_name="Посилання для кнопки 1")
    button2_text = models.CharField(max_length=50, verbose_name="Текст кнопки 2")
    button2_link = models.CharField(max_length=200, default="#", verbose_name="Посилання для кнопки 2")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону під кнопками")

    def __str__(self):
        return "Головний банер"
    class Meta:
        verbose_name = "1. Головний банер"
        verbose_name_plural = "1. Головний банер"


class SectionBackground(models.Model):
    SECTION_CHOICES = [
        ('ALIMONY', 'Фон для секції аліментів'),
        ('BONUSES', 'Фон для секції бонусів'),
        ('TESTIMONIALS', 'Фон для секції відгуків'),
        ('CONTACT', 'Фон для контактної форми'),
        ('HOME_BANER', 'Фон для головного банера'),
    ]
    name = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True, verbose_name="Секція")
    background_image = models.ImageField(upload_to='backgrounds/', verbose_name="Фонове зображення")
    def __str__(self):
        return self.get_name_display()
    class Meta:
        verbose_name = "2. Фонове зображення секції"
        verbose_name_plural = "2. Фонові зображення секцій"

class Service(models.Model):
    CATEGORY_CHOICES = [('DIVORCE', 'Розірвання шлюбу'), ('ALIMONY', 'Стягнення аліментів')]
    title = models.CharField(max_length=200, verbose_name="Назва послуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    label = models.CharField(max_length=50, blank=True, null=True, verbose_name="Мітка, напр. «Під ключ»")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name="Категорія")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"
    class Meta:
        verbose_name = "3. Послуга"
        verbose_name_plural = "3. Послуги"
        ordering = ['order']

class ServiceCategoryInfo(models.Model):
    category = models.CharField(max_length=10, choices=Service.CATEGORY_CHOICES, unique=True, verbose_name="Категорія")
    description = models.TextField(verbose_name="Описовий текст для секції")
    def __str__(self):
        return f"Опис для категорії: {self.get_category_display()}"
    class Meta:
        verbose_name = "3.1. Опис категорії послуг"
        verbose_name_plural = "3.1. Описи категорій послуг"

class Advantage(models.Model):
    title = models.CharField(max_length=100, verbose_name="Назва переваги")
    description = models.TextField(verbose_name="Опис переваги")
    icon_class = models.CharField(max_length=50, verbose_name="Клас іконки Font Awesome (напр. fa-bolt)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "4. Перевага"
        verbose_name_plural = "4. Переваги"
        ordering = ['order']

class Result(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок під зображенням")
    case_image = models.ImageField(upload_to='results/', verbose_name="Зображення судового рішення (скріншот)")
    case_url = models.URLField(max_length=500, verbose_name="Пряме посилання на рішення в реєстрі")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "5. Рішення (Результат)"
        verbose_name_plural = "5. Рішення (Результати)"
        ordering = ['order']

class Testimonial(models.Model):
    text = models.TextField(verbose_name="Текст відгуку")
    author = models.CharField(max_length=100, verbose_name="Автор (напр. 'Олександр, м. Львів')")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")
    def __str__(self):
        return f"Відгук від {self.author}"
    class Meta:
        verbose_name = "6. Відгук"
        verbose_name_plural = "6. Відгуки"
        ordering = ['order']

class AlgorithmStep(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва кроку")
    description = models.TextField(verbose_name="Опис кроку")
    order = models.PositiveIntegerField(default=0, verbose_name="Номер кроку (порядок)")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "7. Крок алгоритму"
        verbose_name_plural = "7. Кроки алгоритму"
        ordering = ['order']

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Питання")
    answer = models.TextField(verbose_name="Відповідь")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")
    def __str__(self):
        return self.question
    class Meta:
        verbose_name = "8. Часте запитання"
        verbose_name_plural = "8. Часті запитання"
        ordering = ['order']

class Bonus(models.Model):
    text = models.CharField(max_length=200, verbose_name="Текст акції / бонусу")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортування")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    def __str__(self):
        return self.text
    class Meta:
        verbose_name = "9. Акція / Бонус"
        verbose_name_plural = "9. Акції та Бонуси"
        ordering = ['order']

class ContactRequest(models.Model):
    situation = models.TextField(verbose_name="Опис ситуації")
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефону")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_processed = models.BooleanField(default=False, verbose_name="Оброблено")
    def __str__(self):
        return f"Заявка від {self.name} ({self.phone_number})"
    class Meta:
        verbose_name = "10. Заявка з сайту"
        verbose_name_plural = "10. Заявки з сайту"
        ordering = ['-created_at']