from django.contrib import admin
from ninja_gate.base_admin import BaseAdmin
from .models import RiskProfile, AbuseEventType, AbuseEvent


@admin.register(RiskProfile)
class RiskProfileAdmin(BaseAdmin):
    list_display = ('phone_number', 'risk_level', 'status', 'risk_score', 'last_seen', 'created')
    list_filter = ('risk_level', 'status', 'created')
    search_fields = ('phone_number',)
    readonly_fields = ('created',)
    ordering = ('-risk_score', '-last_seen')
    
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'risk_score')
        }),
        ('Status', {
            'fields': ('risk_level', 'status')
        }),
        ('Timestamps', {
            'fields': ('last_seen', 'created'),
            'classes': ('collapse',)
        })
    )


@admin.register(AbuseEventType)
class AbuseEventTypeAdmin(BaseAdmin):
    list_display = ('name', 'category', 'severity_weight', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-severity_weight', 'category', 'name')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'severity_weight')
        }),
        ('Details', {
            'fields': ('description',)
        })
    )


@admin.register(AbuseEvent)
class AbuseEventAdmin(BaseAdmin):
    list_display = ('profile', 'event_type', 'source', 'created', 'sms_id')
    list_filter = ('event_type__category', 'event_type', 'source', 'created')
    search_fields = ('profile__phone_number', 'message_content')
    readonly_fields = ('created',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    
    fieldsets = (
        (None, {
            'fields': ('profile', 'event_type', 'source')
        }),
        ('Message Details', {
            'fields': ('message_content', 'sms_id'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        # Optimize queries by selecting related objects
        return super().get_queryset(request).select_related('profile', 'event_type')