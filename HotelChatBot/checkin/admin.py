from django.contrib.admin import DateFieldListFilter
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import CheckinRecord, CheckinTask, CheckinDialogRecord
# Register your models here.
from django.contrib.auth.admin import UserAdmin


class SiteUserAdmin(UserAdmin):
    pass


class CheckinRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_info', 'total_score', 'max_score', 'task_link', 'time')
    list_display_links = ('time',)
    list_per_page = 20

    readonly_fields = ('id', 'author_info', 'total_score', 'max_score', 'task_link', 'time')

    fields = ('author_info', 'total_score', 'max_score', 'task_link', 'time')
    # fieldsets = [
    #     (None, {'fields': ['question_text']}),
    #     ('Date information', {'fields': ['pub_date']}),
    # ]

    def task_link(self, record):
        # url = reverse("admin:record_task_change", kwargs={'object_id': record.author_info.id})
        url = '/admin/checkin/checkintask/{}/change/'.format(record.task.id)
        link = '<a href="{}">task detail</a>'.format(url)
        return mark_safe(link)

    task_link.short_description = 'task'

    def author_link(self, record):
        # url = reverse("admin:record_task_change", kwargs={'object_id': record.author_info.id})
        url = '/admin/auth/user/{}/change/'.format(record.author_info.id)
        link = '<a href="{}">{}</a>'.format(url, record.author_info.username)
        return mark_safe(link)

    author_link.short_description = 'name'
    search_fields = ('author_info__username',)
    ordering = ('author_info__username',)
    list_filter = (
        ('time', DateFieldListFilter),
    )


class CheckinTaskAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'greeting',
                    'registration_card_verify',
                    # 'registration_card_verify_subtask',
                    'registration_card_accurately',
                    'stay_details_confirmation',
                    # 'stay_details_confirmation_subtask',
                    'deposit_collected_correctly',
                    # 'deposit_collected_correctly_subtask',
                    'signature',
                    'room_checked_smoking',
                    'guidelines',
                    # 'guidelines_subtask',
                    'luggage',
                    # 'luggage_subtask',
                    )
    list_per_page = 20

    readonly_fields = list_display + ('registration_card_verify_subtask',
                                      'stay_details_confirmation_subtask',
                                      'deposit_collected_correctly_subtask',
                                      'guidelines_subtask',
                                      'luggage_subtask')

    fieldsets = [
        ('Greet', {'fields': ['greeting']}),
        ('Registration Card', {'fields': ['registration_card_verify', 'registration_card_verify_subtask',
                                          'registration_card_accurately']}),
        ('Stay Details', {'fields': ['stay_details_confirmation', 'stay_details_confirmation_subtask']}),
        ('Deposit', {'fields': ['deposit_collected_correctly', 'deposit_collected_correctly_subtask']}),
        ('Signature', {'fields': ['signature']}),
        ('Room Preference', {'fields': ['room_checked_smoking']}),
        ('Guide', {'fields': ['guidelines', 'guidelines_subtask']}),
        ('Luggage', {'fields': ['luggage', 'luggage_subtask']}),
    ]

    # def registration_card_verify_subtask_link(self, task):
    #     # url = reverse("admin:record_task_change", kwargs={'object_id': record.author_info.id})
    #     url = '/admin/dialogflow_backend/task/{}/change/'.format(task.id)
    #     link = '<a href="{}">task detail</a>'.format(url)
    #     return mark_safe(link)
    #
    # registration_card_verify_subtask_link.short_description = 'task'


class CheckinDialogRecordAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'created_time',
                    )
    list_display_links = ('created_time',)
    list_per_page = 20

    readonly_fields = list_display + ('body',)


admin.site.register(CheckinRecord, CheckinRecordAdmin)
admin.site.register(CheckinTask, CheckinTaskAdmin)
admin.site.register(CheckinDialogRecord, CheckinDialogRecordAdmin)
