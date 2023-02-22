from django.forms import ModelForm
from models import Promotion
from django.core.exceptions import ValidationError

class PromotionForm(ModelForm):
        
    def clean(self):
        cleaned_data = super(PromotionForm, self).clean()
        reward_amount = cleaned_data.get("reward_amount", 0)
        reward_percentage = cleaned_data.get("reward_percentage", 0)
       
        if reward_amount and reward_percentage:
            self.add_error('reward_amount', 'You need to select either Reward Amount or Reward Percentage but not both.')
            
        if reward_percentage > 100:
            self.add_error('reward_percentage', 'Can not be greater than 100%.')
                    
    class Meta:
        model = Promotion
        exclude = ['date_created', 'created_by', 'promotion_code']
