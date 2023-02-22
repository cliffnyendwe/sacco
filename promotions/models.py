from django.db import models
from utils import get_activation_code
from core_manager.models import User
from chama.models import Invoices
from django.utils import timezone

class Promotion(models.Model):
    promotion_name = models.CharField(max_length=200, unique=False)
    promotion_code = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=False, null=True)
    promotion_start_date = models.DateTimeField('promotion start date', default=timezone.now)
    date_created = models.DateTimeField('date created', default=timezone.now)
    created_by = models.ForeignKey(User)    
    use_promotion_code = models.BooleanField(default=False, help_text='Used for promotions that utilize promotion codes')
    apply_for_new_subscriptions = models.BooleanField(default=False)    # if checked, all incoming payments will be subjected to date comparison between promotion date created and time payment was made
    reward_amount = models.IntegerField(blank=True, default = 0)
    reward_percentage = models.IntegerField(blank=True, default = 0)
    active = models.BooleanField(blank=True, default=False)   
    
    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'
    
    def __unicode__(self):            
        return "%s %s" %(self.promotion_name, self.promotion_code)
    
    def __str__(self):             
        return "%s %s" %(self.promotion_name, self.promotion_code)
     
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.promotion_code:
            self.promotion_code = get_activation_code(size = 5)

        super(Promotion, self).save(force_insert=force_insert,
            force_update=force_update, using=using, update_fields=update_fields)
            
class PromotionBonus(models.Model):
    circle_member = models.ForeignKey(User)
    promotion = models.ForeignKey(Promotion)
    invoice = models.ForeignKey(Invoices, null=True)
    bonus_amount = models.FloatField(blank=True, default = 0)
    
    def __unicode__(self):            
        return "%s %s" %(self.circle_member.first_name, self.promotion.promotion_name)
