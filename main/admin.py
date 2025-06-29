from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import (
    SiteConfiguration, MenuItem, HeroBanner, SectionBackground, Service, 
    ServiceCategoryInfo, Advantage, Result, Testimonial, AlgorithmStep, 
    FAQ, Bonus, ContactRequest
)

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(MenuItem)
admin.site.register(HeroBanner, SingletonModelAdmin)
admin.site.register(SectionBackground)
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