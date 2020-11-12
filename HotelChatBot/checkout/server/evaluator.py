class Evaluator:
    """docstring for Evaluator"""

    def __init__(self):
        # naivate by action
        self._tasks = {
            'stay_information': {
                'verify_stay_detail': 0,
                'collect_key_card': 0
            },
            'present_folio': {
                'verify_minibar_charge': 0,
                'post_minibar_charge_correctly': 0,
                'present': 0,
                'get_signature': 0
            },
            'process_payment': {
                'confirm_payment_mode': 0,
                'signature_after_pay': 0
            },
            'assistance_obtain': {
                'clear_safe_deposit': 0,
                'guest_feedback': 0,
                'future_reservation': 0,
                'luggage_assistance': 0,
                'transport_option': 0,
            }
        }
        self._tasks_weight = {
            'stay_information': 2,
            'present_folio': 4,
            'process_payment': 4,
            'assistance_obtain': 4
        }
        self._intent_mapping = {
            'apologize_or_reject': self._apologize_or_reject,
            'be_sure': self._be_sure,
            'default_fallback_intent': self._default_fallback_intent,
            'default_welcome_intent': self._default_welcome_intent,
            'info_clear_deposit': self._info_clear_deposit,
            'info_feedback_glad': self._info_feedback_glad,
            'info_finish_thanks_bid': self._info_finish_thanks_bid,
            'info_no_key_fine': self._info_no_key_fine,
            'info_present_folio': self._info_present_folio,
            'info_present_folio_indicate': self._info_present_folio_indicate,
            'info_something': self._info_something,
            'info_stay_detail': self._info_stay_detail,
            'info_update_bill': self._info_update_bill,
            'question_feedback': self._question_feedback,
            'question_future': self._question_future,
            'question_luggage_assistance': self._question_luggage_assistance,
            'question_minibar': self._question_minibar,
            'question_minibar_items': self._question_minibar_items,
            'question_payment': self._question_payment,
            'question_safe_deposit': self._question_safe_deposit,
            'question_transportation_assistance': self._question_transportation_assistance,
            'request_payment_signature': self._request_payment_signature,
            'request_payment_signature_indicate': self._request_payment_signature_indicate,
            'request_key': self._request_key,
            'request_name_room_num': self._request_name_room_num,
            'request_signature': self._request_signature,
            'request_signature_indicate': self._request_signature_indicate,
            'request_waiting': self._request_waiting,
            'thanks': self._thanks,
        }
        self._activate_order = []

    def __call__(self, input_text, intent, parameters):

        function = self._intent_mapping[intent]
        function(input_text, parameters)
        self._activate_order.append(intent)

    def _calculate_score(self):
        score_dict = {}
        for key, obj in self._tasks.items():
            if isinstance(obj, dict):
                total_score = 0
                values = obj.values()
                num_sub_task = len(values)
                score = sum(values)
                if (score / num_sub_task) < 0.2:
                    pass
                # minor lapses
                elif (score / num_sub_task) < 0.51:
                    total_score = 2
                else:
                    total_score = 4

                score_dict[key] = total_score
                score_dict['{}_subtask'.format(key)] = obj
            else:
                score_dict[key] = obj

        return score_dict

    def finalize(self):
        each_score = self._calculate_score()
        total_score = 0
        for key, weight in self._tasks_weight.items():
            each_score[key] = each_score[key] * weight
            total_score += each_score[key]

        # import json
        # print(json.dumps(each_score, indent=4))

        return total_score, 56, each_score  # max score 56

    def check_minibar(self, minibar_data: dict, minibar_items: dict):
        complete = True
        correct = True

        for key, val in minibar_items.items():
            try:
                if not minibar_data[key]:
                    complete = False
                if minibar_data[key] != val:
                    correct = False
            except:
                pass
        if complete and correct:
            self._tasks['present_folio']['post_minibar_charge_correctly'] = 1

    def _apologize_or_reject(self, text: str, parameters):
        pass

    def _be_sure(self, text: str, parameters):
        pass

    def _default_fallback_intent(self, text: str, parameters):
        pass

    def _default_welcome_intent(self, text: str, parameters):
        pass

    def _info_clear_deposit(self, text: str, parameters):
        pass

    def _info_feedback_glad(self, text: str, parameters):
        pass

    def _info_finish_thanks_bid(self, text: str, parameters):
        pass

    def _info_no_key_fine(self, text: str, parameters):
        pass

    def _info_present_folio(self, text: str, parameters):
        self._tasks['present_folio']['present'] = 1

    def _info_present_folio_indicate(self, text: str, parameters):
        pass

    def _info_something(self, text: str, parameters):
        pass

    def _info_stay_detail(self, text: str, parameters):
        self._tasks['stay_information']['verify_stay_detail'] = 1

    def _info_update_bill(self, text: str, parameters):
        pass

    def _question_feedback(self, text: str, parameters):
        self._tasks['assistance_obtain']['guest_feedback'] = 1

    def _question_future(self, text: str, parameters):
        self._tasks['assistance_obtain']['future_reservation'] = 1

    def _question_luggage_assistance(self, text: str, parameters):
        self._tasks['assistance_obtain']['luggage_assistance'] = 1

    def _question_minibar(self, text: str, parameters):
        self._tasks['present_folio']['verify_minibar_charge'] = 1

    def _question_minibar_items(self, text: str, parameters):
        pass

    def _question_payment(self, text: str, parameters):
        self._tasks['process_payment']['confirm_payment_mode'] = 1

    def _question_safe_deposit(self, text: str, parameters):
        self._tasks['assistance_obtain']['clear_safe_deposit'] = 1

    def _question_transportation_assistance(self, text: str, parameters):
        self._tasks['assistance_obtain']['transport_option'] = 1

    def _request_payment_signature(self, text: str, parameters):
        self._tasks['process_payment']['signature_after_pay'] = 1

    def _request_payment_signature_indicate(self, text: str, parameters):
        self._request_payment_signature(text, parameters)

    def _request_key(self, text: str, parameters):
        self._tasks['stay_information']['collect_key_card'] = 1

    def _request_name_room_num(self, text: str, parameters):
        pass

    def _request_signature(self, text: str, parameters):
        self._tasks['present_folio']['get_signature'] = 1

    def _request_signature_indicate(self, text: str, parameters):
        self._request_signature(text, parameters)

    def _request_waiting(self, text: str, parameters):
        pass

    def _thanks(self, text: str, parameters):
        pass
