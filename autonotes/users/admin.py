from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email',)
    search_fields = ('email',)
    hide = ['password', 'last_login']

    def get_fields(self, request, obj=None):
        fields = super(UserAdmin, self).get_fields(request)
        for hide_field in self.hide:
            if hide_field in fields:
                fields.pop(fields.index(hide_field))
        return fields


admin.site.register(User, UserAdmin)
