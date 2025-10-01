from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)