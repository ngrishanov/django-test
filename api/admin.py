from django.contrib import admin

from api.models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ['internal_id', 'function_code', 'status']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
