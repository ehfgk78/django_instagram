from django import forms

from .models import Post, PostComment

__all__ = (
    'PostForm',
)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = __all__
        fields = (
            'photo',
        )

    def save(self, commit=True, *args, **kwargs):
        # 1. 처음으로 Post객체가 만들어지는 순간
        # 2. instance의 author필드가 비어있으면 save(commit=True)를 비허용
        #   2-1. 하지만 save(commit=False)는 허용 (나중에 author필드를 채움)
        # 3. save()에 author키워드 인수값을 전달할 수 있도록 save() 메서드를 재정의

        # 새로 저장하려는 객체는 pk값이 없다. (DB 저장하려고 할 경우  commit=True)
        # form.save(author=request.user)
        if not self.instance.pk and commit:
            # author값을 키워드 인수 묶음에서 pop으로 삭제하며 값을 가져온다.
            author = kwargs.pop('author', None)
            if not author:
                raise ValueError('Author field is required')
            self.instance.author = author
        return super().save(*args, **kwargs)


class CommentForm(forms.Form):
    # content = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'form-control',
    #             'rows': 1,
    #             'cols': 80,
    #         }
    #     ),
    # )
    class Meta:
        model = PostComment
        fields = (
            'content',
        )
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
