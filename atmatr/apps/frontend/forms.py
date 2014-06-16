from django import forms


class IndexForm(forms.Form):
    starting_url = forms.URLField(label="PLEASE GIVE ME A URL TO START WITH:")
