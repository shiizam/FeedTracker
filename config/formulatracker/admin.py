from django.contrib import admin

from .models import User, FormulaLog, Weight

# Register your models here.

admin.site.register(User)
admin.site.register(FormulaLog)
admin.site.register(Weight)