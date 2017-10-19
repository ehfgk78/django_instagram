from django import forms

__all__ = (
    'PostForm',
)


class PostForm(forms.Form):
    photo = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    text = forms.CharField(
        max_length=5,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 10,
                'cols': 100,
            }
        )
    )

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.upper():
            raise forms.ValidationError('All text must uppercase!')
        return data


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 1,
                'cols': 80,
            }
        ),
)