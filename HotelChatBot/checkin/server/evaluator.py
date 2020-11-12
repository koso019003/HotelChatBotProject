class Evaluator:
    """docstring for Evaluator"""

    def __init__(self, deposit):
        self.deposit = deposit
        # naivate by action
        self._tasks = {
            'greeting': 0.,
            'registration_card_verify': {
                'request_passport': 0.,
                'locate_reservation': 0.,
                'update_registration_card': 0.
            },
            'registration_card_accurately': 0.,
            'stay_details_confirmation': {
                'duration': 0.,
                'departure_date': 0.,
                'room_type': 0.,
                'room_rate': 0.,
                'departure_time': 0.,
            },
            'deposit_collected_correctly': {
                'identify_payment_mode': 0.,
                'deposit_amount': 0.
            },
            'signature': 0.,
            'room_checked_smoking': 0.,
            'guidelines': {
                'issue_key_card_level': 0.,
                'issue_key_card_room_number': 0.,
                'explain_keycard': 0.,
                'advise_breakfast': 0.,
                'advise_internet': 0.
            },
            'luggage': {
                'luggage_assistance': 0.,
                'close_with_pleasantries_anything': 0.,
                'close_with_pleasantries_pleasant': 0.
            }
        }
        self._tasks_weight = {
            'greeting': 2,
            'registration_card_verify': 6,
            'registration_card_accurately': 3,
            'stay_details_confirmation': 3,
            'deposit_collected_correctly': 3,
            'signature': 2,
            'room_checked_smoking': 2,
            'guidelines': 2,
            'luggage': 4
        }
        self._intent_mapping = {
            'apologize_or_reject': self._apologize_or_reject,
            'be_sure': self._be_sure,
            'default_fallback_intent': self._default_fallback_intent,
            'default_welcome_intent': self._default_welcome_intent,
            'fill_up_your_contact': self._fill_up_your_contact,
            'finish_up': self._finish_up,
            'info_breakfast': self._info_breakfast,
            'info_confirm_reservation_detail': self._info_confirm_reservation_detail,
            'info_key_usage': self._info_key_usage,
            'info_locate_room': self._info_locate_room,
            'info_luggage_assistance': self._info_luggage_assistance,
            'info_registration_card': self._info_registration_card,
            'info_something': self._info_something,
            'info_terms_conditions': self._info_terms_conditions,
            'info_terms_conditions_indicate': self._info_terms_conditions,
            'info_wifi': self._info_wifi,
            'info_issue_key': self._info_issue_key,
            'question_anythingelse': self._question_anythingelse,
            'question_bag_with_porter': self._question_bag_with_porter,
            'question_bag_with_self': self._question_bag_with_self,
            'question_luggage': self._question_luggage,
            'question_payment_cant_other': self._question_payment_cant_other,
            'question_payment': self._question_payment,
            'question_purpose': self._question_purpose,
            'question_receive_email': self._question_receive_email,
            'question_smoke': self._question_smoke,
            'request_business_card': self._request_business_card,
            'request_departure_time_can_over': self._request_departure_time_can_over,
            'request_departure_time_cant_over': self._request_departure_time_cant_over,
            'request_departure_time_check_again': self._request_departure_time_check_again,
            'request_departure_time': self._request_departure_time,
            'request_passport': self._request_passport,
            'request_passport_request': self._request_passport_request,
            'request_payment_cant_later': self._request_payment_cant_later,
            'request_payment_cant_other': self._request_payment_cant_other,
            'request_payment_finish': self._request_payment_finish,
            'request_payment': self._request_payment,
            'request_signature': self._request_signature,
            'request_signature_indicate': self._request_signature,
            'request_tags': self._request_tags,
            'request_waiting': self._request_waiting,
            'test_fullfillment': self._test_fullfillment,
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

        import json
        # print(json.dumps(each_score, indent=4))

        return total_score, 96, each_score  # max score 96

    def locate_reservation(self):
        self._tasks['registration_card_verify']['locate_reservation'] = 1

    def check_reg(self, reg_data, id_info, business_info):
        id_info = vars(id_info)
        bn_info = vars(business_info)

        complete = True
        correct = True

        for key, val in id_info.items():
            try:
                if not reg_data[key]:
                    complete = False
                if reg_data[key] != val:
                    correct = False
            except:
                pass
        for key, val in bn_info.items():
            try:
                if not reg_data[key]:
                    complete = False
                if reg_data[key] != val:
                    correct = False
            except:
                pass
        if complete:
            self._tasks['registration_card_verify']['update_registration_card'] = 1
        if correct:
            self._tasks['registration_card_accurately'] = 4

    def _apologize_or_reject(self, text: str, parameters):
        pass

    def _be_sure(self, text: str, parameters):
        pass

    def _info_confirm_reservation_detail(self, text: str, parameters):
        for key in parameters:
            self._tasks['stay_details_confirmation'][key] = 1

    def _default_fallback_intent(self, text: str, parameters):
        pass

    def _default_welcome_intent(self, text: str, parameters):
        if 'welcome' in text and 'hotel west' in text.lower():
            if len(self._activate_order) < 3:
                self._tasks['greeting'] = 2

    def _info_breakfast(self, text: str, parameters):
        self._tasks['guidelines']['advise_breakfast'] = 1

    def _info_key_usage(self, text: str, parameters):
        self._tasks['guidelines']['explain_keycard'] = 1

    def _info_wifi(self, text: str, parameters):
        self._tasks['guidelines']['advise_internet'] = 1

    def _fill_up_your_contact(self, text: str, parameters):
        pass

    def _finish_up(self, text: str, parameters):
        if 'anything' in text:
            self._tasks['luggage']['close_with_pleasantries_anything'] = 0.5
        pleasants = [
            'pleasant stay',
            'enjoy your stay',
            'wonderful stay'
        ]
        for p in pleasants:
            if p in text.lower():
                self._tasks['luggage']['close_with_pleasantries_pleasant'] = 0.5
                break

    def _info_something(self, text: str, parameters):
        pass

    def _info_terms_conditions(self, text: str, parameters):
        pass

    def _info_luggage_assistance(self, text: str, parameters):
        pass

    def _info_issue_key(self, text: str, parameters):
        if parameters:
            if parameters['number']:
                self._tasks['guidelines']['issue_key_card_level'] = 0.5
        sentences = [
            'this is your room number',
            'your room number is here'
        ]
        for sent in sentences:
            if sent in text.lower():
                self._tasks['guidelines']['issue_key_card_room_number'] = 0.5
                break

    def _info_locate_room(self, text: str, parameters):
        pass

    def _question_anythingelse(self, text: str, parameters):
        if 'anything' in text:
            self._tasks['luggage']['close_with_pleasantries_anything'] = 0.5

    def _question_bag_with_self(self, text: str, parameters):
        pass

    def _question_bag_with_porter(self, text: str, parameters):
        pass

    def _question_luggage(self, text: str, parameters):
        self._tasks['luggage']['luggage_assistance'] = 1

    def _question_payment_cant_other(self, text: str, parameters):
        pass

    def _question_payment(self, text: str, parameters):
        self._tasks['deposit_collected_correctly']['identify_payment_mode'] = 1

    def _question_purpose(self, text: str, parameters):
        pass

    def _question_receive_email(self, text: str, parameters):
        pass

    def _question_smoke(self, text: str, parameters):
        self._tasks['room_checked_smoking'] = 2

    def _request_business_card(self, text: str, parameters):
        pass

    def _request_departure_time_can_over(self, text: str, parameters):
        pass

    def _request_departure_time_cant_over(self, text: str, parameters):
        pass

    def _request_departure_time_check_again(self, text: str, parameters):
        pass

    def _request_departure_time(self, text: str, parameters):
        self._tasks['stay_details_confirmation']['departure_time'] = 1

    def _request_passport(self, text: str, parameters):
        self._tasks['registration_card_verify']['request_passport'] = 1

    def _request_passport_request(self, text: str, parameters):
        pass

    def _request_payment_cant_later(self, text: str, parameters):
        pass

    def _request_payment_cant_other(self, text: str, parameters):
        pass

    def _request_payment_finish(self, text: str, parameters):
        pass

    def _request_payment(self, text: str, parameters):
        self._tasks['registration_card_verify']['request_passport'] = 1
        try:
            if parameters['unit_currency']['amount'] == self.deposit:
                self._tasks['registration_card_verify']['deposit_amount'] = 1
        except:
            pass

    def _info_registration_card(self, text: str, parameters):
        pass

    def _request_signature(self, text: str, parameters):
        self._tasks['signature'] = 2

    def _request_tags(self, text: str, parameters):
        self._tasks['luggage']['luggage_assistance'] = 1

    def _request_waiting(self, text: str, parameters):
        pass

    def _test_fullfillment(self, text: str, parameters):
        pass

    def _thanks(self, text: str, parameters):
        pass
