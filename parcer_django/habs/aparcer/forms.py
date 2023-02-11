from django import forms

from .models import Product

class ProductForm(forms.ModelForm):

    #def clean_url(self):
    #   url = self.clean_data['url']

    class Meta:
        model = Product
        fields = (
            'title',
            'url',
            'user_name',
            'user_link',
        )
        widgets = {
            'title': forms.TextInput
        }