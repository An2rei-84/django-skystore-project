from django.contrib import admin
from .models import Mailing, Message, Client, Attempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'frequency', 'status', 'owner')
    list_filter = ('status', 'frequency', 'owner')
    search_fields = ('start_time', 'end_time')
    filter_horizontal = ('clients',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'mailing')
    list_filter = ('mailing',)
    search_fields = ('subject', 'body')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'owner')
    list_filter = ('owner',)
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'timestamp', 'status')
    list_filter = ('status', 'mailing')
