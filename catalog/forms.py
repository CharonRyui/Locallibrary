from django import forms
import datetime
from django.core.exceptions import ValidationError

# the gettext_lazy is used to enable the website to be translated more easily
from django.utils.translation import gettext_lazy as _

from catalog.models import BookInstance

# class RenewBookForm(forms.Form):
    
#     renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks(default 3)')
    
#     def clean_renewal_date(self):
#         # use cleaned_data() to get the data
#         data = self.cleaned_data['renewal_date']

#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))
        
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
#         # return data no matter whether it is changed
#         return data

# use the ModelForm to simplify the code
class RenewBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
    
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if (data < datetime.date.today()):
            raise ValidationError(_('Invalid date - renewal in past'))
        
        if (data > datetime.date.today() + datetime.timedelta(weeks=4)):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data