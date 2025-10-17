from django.contrib import admin
from .models import User, Post, Response, EmailConfirmation

# ---------------------------
# Inline отклики для Post
# ---------------------------
class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0
    readonly_fields = ('author', 'text', 'created_at')
    can_delete = True

# ---------------------------
# Админка для Post с inline откликами
# ---------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    inlines = [ResponseInline]

# ---------------------------
# Админка для пользователей
# ---------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'email_confirmed', 'is_staff')
    list_filter = ('email_confirmed', 'is_staff')
    search_fields = ('username', 'email')

# ---------------------------
# Админка для откликов отдельно
# ---------------------------
@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'accepted', 'created_at')
    list_filter = ('accepted', 'created_at', 'post__category')
    search_fields = ('author__username', 'text', 'post__title')
    date_hierarchy = 'created_at'

# ---------------------------
# Админка для EmailConfirmation (для отладки)
# ---------------------------
@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__username', 'token')
