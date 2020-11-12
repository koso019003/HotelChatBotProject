from django.contrib.admin import DateFieldListFilter
from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import CheckoutRecord, CheckoutTask, CheckoutDialogRecord


# Register your models here.


class CheckoutRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_info', 'total_score', 'max_score', 'task_link', 'time')
    list_display_links = ('time',)
    list_per_page = 20

    readonly_fields = ('id', 'author_info', 'total_score', 'max_score', 'task_link', 'time')

    fields = ('author_info', 'total_score', 'max_score', 'task_link', 'time')

    def task_link(self, record):
        # url = reverse("admin:record_task_change", kwargs={'object_id': record.author_info.id})
        url = '/admin/checkout/checkouttask/{}/change/'.format(record.task.id)
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


class CheckoutTaskAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'stay_information',
                    # 'stay_information_subtask',
                    'present_folio',
                    # 'present_folio_subtask',
                    'process_payment',
                    # 'process_payment_subtask',
                    'assistance_obtain',
                    # 'assistance_obtain_subtask',
                    )
    list_per_page = 20

    readonly_fields = list_display + ('stay_information_subtask',
                                      'present_folio_subtask',
                                      'process_payment_subtask',
                                      'assistance_obtain_subtask',
                                      )

    fieldsets = [
        ('Establish Guest Stay Information', {'fields': ['stay_information', 'stay_information_subtask']}),
        ('Present Folio', {'fields': ['present_folio', 'present_folio_subtask']}),
        ('Process Payment', {'fields': ['process_payment', 'process_payment_subtask']}),
        ('Further Service And Assistance', {'fields': ['assistance_obtain', 'assistance_obtain_subtask']}),
    ]


class CheckoutDialogRecordAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'created_time',
                    )
    list_display_links = ('created_time',)
    list_per_page = 20

    readonly_fields = list_display + ('body',)


admin.site.register(CheckoutRecord, CheckoutRecordAdmin)
admin.site.register(CheckoutTask, CheckoutTaskAdmin)
admin.site.register(CheckoutDialogRecord, CheckoutDialogRecordAdmin)
