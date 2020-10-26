from django import forms
from .models import ExcelUpload


class ExcelUploadForm(forms.ModelForm):
    excel = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input',
        'accept': '.xlsx',
        'id': 'validatedCustomFile'
    }), required=True)

    class Meta:
        model = ExcelUpload
        fields = [
            'excel'
        ]
