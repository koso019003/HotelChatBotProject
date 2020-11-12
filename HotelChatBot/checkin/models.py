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


class RCV(models.Model):
    request_passport = models.BooleanField()
    locate_reservation = models.BooleanField()
    update_registration_card = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class SDC(models.Model):
    duration = models.BooleanField()
    departure_date = models.BooleanField()
    room_type = models.BooleanField()
    room_rate = models.BooleanField()
    departure_time = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class DCC(models.Model):
    identify_payment_mode = models.BooleanField()
    deposit_amount = models.BooleanField()

    def __str__(self):
        return sub_task2string(self)


class G(models.Model):
    issue_key_card_level = models.BooleanField()
    issue_key_card_room_number = models.BooleanField()
    explain_keycard = models.BooleanField()
    advise_breakfast = models.BooleanField()
    advise_internet = models.BooleanField()

    def __str__(self):
        string = '<div class="form-row field-{}">' \
                 '    <div>' \
                 '        <label>{}:</label>' \
                 '        <div class="readonly">{}</div>' \
                 '    </div>' \
                 '</div>' * 5

        return format_html(
            string,
            # class Name            # Label Name            # content
            'issue_key_card_level', 'Issue Key Card - Level', self.issue_key_card_level,
            'issue_key_card_room_number', 'Issue Key Card - Room Number', self.issue_key_card_room_number,
            'explain_keycard', 'Explain Keycard', self.explain_keycard,
            'advise_breakfast', 'Advise Breakfast', self.advise_breakfast,
            'advise_internet', 'Advise Internet', self.advise_internet,
        )


class L(models.Model):
    luggage_assistance = models.BooleanField()
    close_with_pleasantries_anything = models.BooleanField()
    close_with_pleasantries_pleasant = models.BooleanField()

    def __str__(self):
        string = '<div class="form-row field-{}">' \
                 '    <div>' \
                 '        <label>{}:</label>' \
                 '        <div class="readonly">{}</div>' \
                 '    </div>' \
                 '</div>' * 3

        return format_html(
            string,
            # class Name            # Label Name            # content
            'luggage_assistance', 'Luggage Assistance', self.luggage_assistance,
            'close_with_pleasantries_anything', 'Close With Pleasantries - Anything',
            self.close_with_pleasantries_anything,
            'close_with_pleasantries_pleasant', 'Close With Pleasantries - Pleasant',
            self.close_with_pleasantries_pleasant,
        )


class CheckinTask(models.Model):
    # marks
    greeting = models.IntegerField()
    registration_card_verify = models.IntegerField()
    registration_card_verify_subtask = models.OneToOneField(
        RCV,
        on_delete=models.CASCADE,
    )
    registration_card_accurately = models.IntegerField()
    stay_details_confirmation = models.IntegerField()
    stay_details_confirmation_subtask = models.OneToOneField(
        SDC,
        on_delete=models.CASCADE,
    )
    deposit_collected_correctly = models.IntegerField()
    deposit_collected_correctly_subtask = models.OneToOneField(
        DCC,
        on_delete=models.CASCADE,
    )
    signature = models.IntegerField()
    room_checked_smoking = models.IntegerField()
    guidelines = models.IntegerField()
    guidelines_subtask = models.OneToOneField(
        G,
        on_delete=models.CASCADE,
    )
    luggage = models.IntegerField()
    luggage_subtask = models.OneToOneField(
        L,
        on_delete=models.CASCADE,
    )
    sub_mapping = {
        'registration_card_verify_subtask': RCV,
        'stay_details_confirmation_subtask': SDC,
        'deposit_collected_correctly_subtask': DCC,
        'guidelines_subtask': G,
        'luggage_subtask': L,
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


class CheckinRecord(models.Model):
    author_info = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Name'
    )
    time = models.DateTimeField(auto_now=True)
    total_score = models.IntegerField()
    max_score = models.IntegerField()

    task = models.OneToOneField(
        CheckinTask,
        on_delete=models.CASCADE,
    )

    @classmethod
    def add_record(cls, user, score, max_score, each_score: dict):
        data_dict = {
            'author_info': user,
            'total_score': score,
            'max_score': max_score,
            'task': CheckinTask.add_record(each_score=each_score)
        }
        return cls.objects.create(**data_dict)


class CheckinDialogRecord(models.Model):
    body = models.TextField()
    created_time = models.DateTimeField(auto_now=True)

    @classmethod
    def add_record(cls, body):
        data_dict = {
            'body': body,
        }
        return cls.objects.create(**data_dict)
