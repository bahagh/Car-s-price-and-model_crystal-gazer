from django.contrib import admin
from .models import Listing,ReviewRating

class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner','Model', 'Make', 'price', 'is_published', 'list_date')
    list_display_links = ('id', 'title')
    list_filter = ('Make',)
    search_fields = ('title', 'description', 'address', 'city', 'zipcode', 'state', 'price')
    list_per_page = 30

class Listreg(admin.ModelAdmin):
    list_display = ('car', 'user', 'subject','rating')
    list_display_links = ('car', 'user')
    list_filter = ('car',)
    search_fields = ('car', 'user')
    list_per_page = 10


admin.site.register(Listing, ListAdmin)
admin.site.register(ReviewRating, Listreg)