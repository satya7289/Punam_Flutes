from django import forms

from captcha.fields import ReCaptchaField
from .models import UserQuery
from commons.country_currency import country as Country

class UserQueryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
    
    CountryChoice  = [['', '-----']] + Country[1:]
    country = forms.ChoiceField(choices=CountryChoice)
    captcha = ReCaptchaField()

    class Meta:
        model = UserQuery
        fields = '__all__'
        required = (
            'country', 'full_name','email', 'subject', 'message'
        )