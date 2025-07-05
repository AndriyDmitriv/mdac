from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import (
    SiteConfiguration, MenuItem, HeroBanner, SectionBackground, Service, 
    ServiceCategoryInfo, Advantage, Result, Testimonial, AlgorithmStep, 
    FAQ, Bonus, ContactRequest
)
from django.utils.html import format_html

class SiteConfigurationAdmin(SingletonModelAdmin):
    readonly_fields = (
        'header_logo_image_preview',
        'footer_logo_image_preview',
        'footer_background_image_preview',
    )
    fieldsets = (
        (None, {
            'fields': (
                'header_logo_text',
                'header_logo_image', 'header_logo_image_preview',
                'header_logo_image_footer', 'footer_logo_image_preview',
                'footer_background_image', 'footer_background_image_preview',
                'header_carousel_text_1', 'header_carousel_text_2', 'header_carousel_text_3',
                'footer_logo_text', 'footer_tagline', 'footer_contacts_title',
                'footer_phone', 'footer_email', 'footer_cta_text', 'footer_cta_link',
                'divorce_section_title', 'alimony_section_title', 'packages_subtitle',
                'advantages_section_title', 'results_section_title', 'results_section_subtitle',
                'results_button_text', 'testimonials_section_title', 'algorithm_section_title',
                'faq_section_title', 'bonuses_section_title', 'contact_form_title',
                'contact_form_subtitle', 'contact_form_button_text',
            )
        }),
    )

    def header_logo_image_preview(self, obj):
        if obj.header_logo_image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.header_logo_image.url)
        return "-"
    header_logo_image_preview.short_description = "Прев'ю логотипу в хедері"

    def footer_logo_image_preview(self, obj):
        if obj.header_logo_image_footer:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.header_logo_image_footer.url)
        return "-"
    footer_logo_image_preview.short_description = "Прев'ю логотипу в футері"

    def footer_background_image_preview(self, obj):
        if obj.footer_background_image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.footer_background_image.url)
        return "-"
    footer_background_image_preview.short_description = "Прев'ю фону футера"

admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
admin.site.register(MenuItem)
admin.site.register(HeroBanner, SingletonModelAdmin)

@admin.register(SectionBackground)
class SectionBackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'background_image_preview')
    readonly_fields = ('background_image_preview',)

    def background_image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 60px;"/>', obj.background_image.url)
        return "-"
    background_image_preview.short_description = "Прев'ю фону"

admin.site.register(Service)
admin.site.register(ServiceCategoryInfo)
admin.site.register(Advantage)
admin.site.register(Result)
admin.site.register(Testimonial)
admin.site.register(AlgorithmStep)
admin.site.register(FAQ)
admin.site.register(Bonus)

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'phone_number', 'situation')
    readonly_fields = ('name', 'phone_number', 'situation', 'created_at')