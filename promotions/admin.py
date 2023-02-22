from django.contrib import admin

from django.contrib import admin

from models import *
from forms import *

class PromotionAdmin(admin.ModelAdmin):

    form = PromotionForm
    
    """fieldsets = [
        (None, {'fields': ['promotion_name', 'description', 'use_promotion_code', 'apply_for_new_subscriptions', 'reward_amount', 'reward_percentage']}),         
    ]"""
    list_display = ('promotion_name', 'promotion_code', 'description', 'promotion_start_date', 'date_created', 'created_by', 'use_promotion_code', 'apply_for_new_subscriptions', 'reward_amount', 'reward_percentage', 'active')
    
    search_fields = ('promotion_name', 'promotion_code', 'description')
    
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()
        
class PromotionBonusAdmin(admin.ModelAdmin):
    list_display = ('circle_member', 'promotion', 'invoice', 'bonus_amount')
    
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(PromotionBonus, PromotionBonusAdmin)
