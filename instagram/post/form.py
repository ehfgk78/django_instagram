from django import forms

__all__=(
    'PostForm',
)

class PostForm(forms.Form):
    photo = forms.ImageField()
    # Text를 받을 수 있는 필드 추가
    # comment = forms.CharField(max_length=5)

    # 임의로 만든 유효성 검사 메서드
    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     if data != data.upper():
    #         raise forms.ValidationError('All text must uppercase!')
    #     return data


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea,
    )