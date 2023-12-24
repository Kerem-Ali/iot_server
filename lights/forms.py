from django import forms

from lights.models import Light

    

class LightEditForm(forms.ModelForm):
    class Meta:
        model = Light
        fields = ("name","is_on")

        widgets = {
            "name":forms.TextInput(attrs={"class":"form-control"}),
            
        }
