from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html


# Create your models here.


def sub_task2string(obj):
    obj_dict = vars(obj)
    del obj_dict['_state']
    del obj_dict['id']

    num = len(obj_dict)
    string = '<div class="form-row field-{}">' \
             '    <div>' \
             '        <label>{}:</label>' \
             '        <div class="readonly">{}</div>' \
             '    </div>' \
             '</div>' * num
    content_list = []
    for k, v in obj_dict.items():
        content_list.append(k)
        content_list.append(k.replace('_', ' ').title())
        content_list.append(v)
    return format_html(
        string,
        *content_list
    )


class SI(models.Model):
    verify_stay_detail = models.BooleanField()
    collect_key_card = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class PF(models.Model):
    verify_minibar_charge = models.BooleanField()
    post_minibar_charge_correctly = models.BooleanField()
    present = models.BooleanField()
    get_signature = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class PP(models.Model):
    confirm_payment_mode = models.BooleanField()
    signature_after_pay = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class AO(models.Model):
    clear_safe_deposit = models.BooleanField()
    guest_feedback = models.BooleanField()
    future_reservation = models.BooleanField()
    luggage_assistance = models.BooleanField()
    transport_option = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class CheckoutTask(models.Model):
    # marks
    stay_information = models.IntegerField()
    stay_information_subtask = models.OneToOneField(
        SI,
        on_delete=models.CASCADE,
    )
    present_folio = models.IntegerField()
    present_folio_subtask = models.OneToOneField(
        PF,
        on_delete=models.CASCADE,
    )
    process_payment = models.IntegerField()
    process_payment_subtask = models.OneToOneField(
        PP,
        on_delete=models.CASCADE,
    )
    assistance_obtain = models.IntegerField()
    assistance_obtain_subtask = models.OneToOneField(
        AO,
        on_delete=models.CASCADE,
    )
    sub_mapping = {
        'stay_information_subtask': SI,
        'present_folio_subtask': PF,
        'process_payment_subtask': PP,
        'assistance_obtain_subtask': AO,
    }

    @classmethod
    def add_record(cls, each_score: dict):
        import json
        print(json.dumps(each_score, indent=4))

        data_dict = {}
        for key, value in each_score.items():
            if '_subtask' in key:
                assert isinstance(value, dict)
                sub_task = cls.sub_mapping[key]
                data_dict[key] = sub_task.objects.create(**{
                    k: True if v > 0 else False for k, v in value.items()
                })
            else:
                data_dict[key] = value

        return cls.objects.create(**data_dict)


class CheckoutRecord(models.Model):
    author_info = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Name'
    )
    time = models.DateTimeField(auto_now=True)
    total_score = models.IntegerField()
    max_score = models.IntegerField()

    task = models.OneToOneField(
        CheckoutTask,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add_record(cls, user, score, max_score, each_score: dict):
        data_dict = {
            'author_info': user,
            'total_score': score,
            'max_score': max_score,
            'task': CheckoutTask.add_record(each_score=each_score)
        }
        return cls.objects.create(**data_dict)


class CheckoutDialogRecord(models.Model):
    body = models.TextField()
    created_time = models.DateTimeField(auto_now=True)

    @classmethod
    def add_record(cls, body):
        data_dict = {
            'body': body,
        }
        return cls.objects.create(**data_dict)
