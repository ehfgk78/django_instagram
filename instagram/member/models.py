from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models
from post.models import Post


# createsuperuser의 입력 항목을 재정의
## REQUIRED_FIELDS에서  +  ['age'] 불필요해짐
class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)

    def create_facebook_user(self, facebook_user_id):
        # Facebook type의 유저 생성
        pass


class User(AbstractUser):
    objects = UserManager()

    img_profile = models.ImageField(
        # 프로필 이미지
        upload_to='user',
        blank=True)
    # DB에 저장되는 것은 image의 '저장 위치' --> "null=True"를 쓰지 않음
    age = models.IntegerField('나이')
    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS +  ['age']
    like_posts = models.ManyToManyField(
        'post.Post',
        verbose_name='좋아요 누른 포스트 목록'
    )
    following_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
        related_name='followers',
    )
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_DJANGO = 'd'
    CHOICES_USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_DJANGO, 'Django'),
    )
    user_type = models.CharField(max_length=1, choices=CHOICES_USER_TYPE)
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'

    def follow_toggle(self, user):
        # 1. 주어진 user가 User객체인지 확인  > 아니면 > raise ValueError()
        # 2. 주어진 user가 follow하고 있으면 해제 > 아니면 > follow함
        if not isinstance(user, User):
            raise ValueError("'user' argument must be User instance!")
        relation, relation_created = self.following_users.get_or_create(
            to_user=user
        )
        if relation_created:
            return True
        relation.delete()
        return False

        # if user in self.following_users.all():
        #     Relation.objects.create(
        #         from_user=self,
        #         to_user=user,
        #     )
        # else:
        #     self.following_user_relations.create(to_user=user)
        #     Relation.objects.create(
        #         from_user=self,
        #         to_user=user,
        #     )


class Relation(models.Model):
    # User의 follow목록을 가질 수 있도록  MTM 중개모델을 구성
    # fields:: from_user, to_user, created_at
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed_user_relations',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_relations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relation (' \
               f'from: { self.from_user.username },' \
               f'to: { self.to_user.username })'
