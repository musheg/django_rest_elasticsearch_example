import arrow
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html

from apps.user.models import User, Product, Hashtag, ProductPicture


class JoinedFilter(SimpleListFilter):
    title = 'joined'
    parameter_name = 'joined'

    LOOKUP_VALUES = {
        '24h': {'days': -1},
        '48h': {'days': -2},
        '1week': {'weeks': -1},
        '1month': {'months': -1},
        'quarter': {'months': -3},
        '6months': {'months': -6},
        '1year': {'years': -1}
    }

    def lookups(self, request, model_admin):
        return [('24h', '24h'), ('48h', '48h'), ('1week', '1 week'), ('1month', '1 month'), ('quarter', 'quarter'),
                ('6months', '6 months'), ('1year', '1 year')]

    def queryset(self, request, queryset):
        now = arrow.utcnow()
        return queryset.filter(
            date_joined__gt=now.shift(**self.LOOKUP_VALUES[self.value()]).datetime) if self.value() else queryset


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'username',
        'number_of_followers',
    ]

    list_display_links = ['id', 'full_name', 'username']
    search_fields = ['full_name', 'username', 'email', ]
    list_filter = [JoinedFilter]
    readonly_fields = ['profile_picture', 'number_of_followings', 'number_of_followers', ]

    def number_of_followings(self, obj):
        return obj.following.all().count()

    def number_of_followers(self, obj):
        return obj.followers.all().count()

    def profile_picture(self, obj):
        return format_html('<img src="%s" />' % obj.photo.url) if obj.photo is not None else ''

    number_of_followers.admin_order_field = 'followers'

    class Meta:
        model = User


class ProductPictureInline(admin.StackedInline):
    model = ProductPicture


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        # 'link',
        # 'supplier',
    ]
    list_display_links = ['id', 'name']
    search_fields = ['name']
    fields = ['name', 'description', 'primary_picture']
    inlines = [ProductPictureInline]

    class Meta:
        model = Product


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]
    list_display_links = ['id', 'name']
    search_fields = ['name']

    class Meta:
        model = Hashtag
