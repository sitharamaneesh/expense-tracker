from django.contrib import admin
from .models import balance

# Register your m
"""class ExpenseAdmin(admin.ModelAdmin):
    fields=(('user'),('expense'),('amount'))
    #list_display=('user','expense','amount')
    #ordering=('expense',)
    
    #search_fields=('expense','amount')
admin.site.register(expense,ExpenseAdmin)"""

class BalanceAdmin(admin.ModelAdmin):
    fields=(('user'),('deposit'),)
    #list_display=('name','address')
    #ordering=('expense',)
    #search_fields=('expense','amount')
admin.site.register(balance,BalanceAdmin)

