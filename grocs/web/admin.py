from django.contrib import admin
from . models import *
from .models import ContactMessage
# Register your models here.
admin.site.register(Customer)




@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')