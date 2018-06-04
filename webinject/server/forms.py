from django import forms

class SubmitForm(forms.Form):
    steps = forms.CharField(widget=forms.Textarea)

