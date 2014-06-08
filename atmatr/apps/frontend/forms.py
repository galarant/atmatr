from django import forms

class IndexForm(forms.Form):
    starting_page = forms.URLField(label="NOW YOU MUST GIVE ME A STARTING URL:")
