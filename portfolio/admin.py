from django.contrib import admin

from .models import Customer, Investment, Stock, Fund, Mutual


class CustomerList(admin.ModelAdmin):
    list_display = ('cust_number', 'name', 'city', 'cell_phone')
    list_filter = ('cust_number', 'name', 'city')
    search_fields = ('cust_number', 'name')
    ordering = ['cust_number']


class InvestmentList(admin.ModelAdmin):
    list_display = ('customer', 'category', 'description', 'recent_value')
    list_filter = ('customer', 'category')
    search_fields = ('customer', 'category')
    ordering = ['customer']


class StockList(admin.ModelAdmin):
    list_display = ('customer', 'symbol', 'name', 'shares', 'purchase_price')
    list_filter = ('customer', 'symbol', 'name')
    search_fields = ('customer', 'symbol', 'name')
    ordering = ['customer']


class FundList(admin.ModelAdmin):
    list_display = ('customer', 'type', 'description','minimum_purchase','purchase_date',
                    'purchase_value', 'recent_date', 'present_value')
    list_filter = ('customer', 'type', 'description','minimum_purchase','purchase_date',
                    'purchase_value', 'recent_date', 'present_value')
    search_fields = ('customer', 'type', 'description','minimum_purchase','purchase_date',
                    'purchase_value', 'recent_date', 'present_value')
    ordering = ['customer']

class MutualList(admin.ModelAdmin):
    list_display = ('customer', 'name', 'shares', 'purchase_value','present_value')
    list_filter = ('customer',  'name')
    search_fields = ('customer',  'name')
    ordering = ['customer']

admin.site.register(Fund, FundList)
admin.site.register(Customer, CustomerList)
admin.site.register(Investment, InvestmentList)
admin.site.register(Stock, StockList)
admin.site.register(Mutual, MutualList)
