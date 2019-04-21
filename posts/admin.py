from django.contrib import admin
from .models import Users,Category,Posts,Tag,Remote

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Remote)

class UsersAdmin(admin.ModelAdmin):
    list_display=('username','email', 'website','is_active', 'introduction','last_login','date_joined')
admin.site.register(Users,UsersAdmin)

class PostsAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'category','timestamp')
admin.site.register(Posts,PostsAdmin)
