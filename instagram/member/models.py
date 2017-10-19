from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models


#createsuperuser의 입력 항목을 재정의
## REQUIRED_FIELDS에서  +  ['age'] 불필요해짐
class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


# Create your models here.
class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    # DB에 저장되는 것은 image의 '저장 위치' --> "null=True"를 쓰지 않음
    age = models.IntegerField(default=30)
    # REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS +  ['age']
    objects = UserManager()