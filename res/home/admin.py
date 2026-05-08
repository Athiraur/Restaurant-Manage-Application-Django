from django.contrib import admin

# Register your models here.
from .models import reg,card,signup

admin.site.register(reg)

admin.site.register(card)

admin.site.register(signup)
