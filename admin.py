from django.contrib import admin

# Register your models here.

from .models import Follow,Posts, User

admin.site.register(Follow)
admin.site.register(Posts)
admin.site.register(User)