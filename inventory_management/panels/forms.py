from django import forms
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"  # Include all fields from the model


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"  # Include all fields from the model

class ManagerForm(forms.ModelForm):
    class Meta:
        model = BranchManager
        fields = "__all__"  # Include all fields from the model
    

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        name = cleaned_data.get('name')
        mobile_number = cleaned_data.get('mobile_number')
        pan_number = cleaned_data.get('pan_number')

        if email=="":
            raise forms.ValidationError("Email can't be empty")
        else:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Invalid email address.')
        
        if pan_number=="":
            raise forms.ValidationError("PAN-Number can't be empty")
        elif len(pan_number)!=10:
            raise forms.ValidationError("PAN-Number must be of length 10")

        if mobile_number=="":
            raise forms.ValidationError("mobile number can't be empty")
        elif len(mobile_number)!=10:
            raise forms.ValidationError("Mobile number must be of length 10")
        




