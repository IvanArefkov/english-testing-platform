from django import forms

class QuestionUploadForm(forms.Form):
    upload_file = forms.FileField()



