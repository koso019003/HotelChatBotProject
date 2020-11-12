import random


class ChatBot:
    def __init__(self, info):
        self.info = info

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
        self._can_see_payment_sign_blank = True  # False
        self._can_see_sign_blank = False
        self._can_see_folio = False

    def __call__(self, intent, parameters):
        print('intent: ', intent)
        print('parameters:', parameters)

        function = self._intent_mapping[intent]
        return function(parameters)

    def set_showed_sign(self):
        self._can_see_sign_blank = True

    # def set_showed_sign_payment(self):
    #     self._can_see_payment_sign_blank = True

    def set_showed_folio(self):
        self._can_see_folio = True

    def _apologize_or_reject(self, parameters):
        responses = [
            "that's fine",
            "It is okay",
            "it's okay, don't worry about it",
            "that's fine, no problem",
        ]
        response = random.choice(responses)

        return response

    def _be_sure(self, parameters):
        responses = [
            "thanks",
        ]
        response = random.choice(responses)

        return response

    def _default_fallback_intent(self, parameters):
        responses = [
            "I didn't get that. Can you say it again?",
            "I missed what you said. What was that?",
            "Sorry, could you say that again?",
            "Sorry, can you say that again?",
            "Can you say that again?",
            "Sorry, I didn't get that. Can you rephrase?",
            "Sorry, what was that?",
            "One more time?",
            "What was that?",
            "Say that one more time?",
            "I didn't get that. Can you repeat?",
            "I missed that, say that again?",
        ]
        response = random.choice(responses)

        return response

    def _default_welcome_intent(self, parameters):
        responses = [
            "I would like to checkout",
            "I want to checkout",
            "I want to checkout now",
            "I would like to checkout now",
            "Checkout",
            "Checkout, please",
            "It's time to checkout",
        ]
        response = random.choice(responses)

        return response

    def _info_clear_deposit(self, parameters):
        responses = [
            "Okay, thank you",
            "Ok",
            "Thanks",
        ]
        response = random.choice(responses)

        return response

    def _info_feedback_glad(self, parameters):
        responses = [
            ": )",
            ":目",
        ]
        response = random.choice(responses)

        return response

    def _info_finish_thanks_bid(self, parameters):
        responses = [
            "bye bye ~ : )",
            "bye~ : 目",
            "bye~",
            "bye bye~",
        ]
        response = {
            'text': random.choice(responses),
            'action': 'complete',
            'params': None,
        }
        return response

    def _info_no_key_fine(self, parameters):
        responses = [
            "Thank you",
            "Thanks",
            "That's great",
        ]
        response = random.choice(responses)

        return response

    def _info_present_folio(self, parameters):
        responses_true = [
            "Sure",
            "Okay",
            "Here? Okay",
            "Alright",
            "No problem",
        ]
        responses_false = [
            "where is it?",
            "do you mean.. where?",
            "sorry, where?"
        ]

        if self._can_see_folio:
            response = random.choice(responses_true)
            response = {
                'text': response,
                'action': 'fill_credit_card_signature',
                'params': {
                    'signature': self.info.full_name
                }
            }

        else:
            response = random.choice(responses_false)

        return response, self._can_see_payment_sign_blank

    def _info_present_folio_indicate(self, parameters):
        return self._info_present_folio(parameters)

    def _info_something(self, parameters):
        responses = [
            "Sure",
            "Sure, thank you",
            "Okay, thanks",
        ]
        response = random.choice(responses)

        return response

    def _info_stay_detail(self, parameters):
        responses = [
            "Yes",
            "Ya",
            "Right",
        ]
        response = random.choice(responses)

        return response

    def _info_update_bill(self, parameters):
        responses = [
            "Sure",
            "Okay",
        ]
        response = random.choice(responses)

        return response

    def _question_feedback(self, parameters):
        response_true = [
            "I had the most enjoyable stay",
            "I enjoyed my stay very much",
            "Very much",
        ]

        response = random.choice(response_true)
        return response

    def _question_future(self, parameters):
        response_true = [
            "At the moment, I have no plans yet",
            "I am not sure when I am coming back to Singapore",
            "No",
        ]

        response = random.choice(response_true)
        return response

    def _question_luggage_assistance(self, parameters):
        response_true = [
            "Yes, thank you so much",
            "Yes, that will be great",
            "Thanks, I can do it by myself",
        ]

        response = random.choice(response_true)
        return response

    def _question_minibar(self, parameters):
        response_true = [
            "Yes",
            "Yes, some of {}",
        ]
        response_false = [
            "No, I didn't",
            "No, I didn't touch the minibar at all",
            "No, I did not"
        ]

        if self.info.use_minibar:
            num_items = len(self.info.minibar_item_dict.keys())
            if num_items == 1:
                items = self.info.minibar_item_dict.keys()[0]
            elif num_items == 2:
                items = '{} and {}'.format(*self.info.minibar_item_dict.keys())
            elif num_items == 3:
                items = '{}, {} and {}'.format(*self.info.minibar_item_dict.keys())
            else:
                items = ''
            response = random.choice(response_true).format(items)
        else:
            response = random.choice(response_false)

        return response

    def _question_minibar_items(self, parameters):
        response_true = [
            "yes, {}",
            "okay, {}",
        ]
        items = self.info.minibar_item_dict.items()
        num_items = len(items)
        if num_items == 1:
            items_str = '{} of {}'.format(*items[0])
        elif num_items == 2:
            items_str = '{} and {}'.format(*['{} of {}'.format(item[1], item[0]) for item in items])
        elif num_items == 3:
            items_str = '{}, {} and {}'.format(*['{} of {}'.format(item[1], item[0]) for item in items])
        else:
            items_str = 'items error'
        response = random.choice(response_true).format(items_str)
        return response

    def _question_payment(self, parameters):
        response_true = [
            "{}, please",
            "I would like to use {}",
            "{}, thanks",
            "I am paying by {}",
            "I will be paying by {}",
            "I would like to pay by {}",

        ]
        response_give = [
            "For payment? Sure",
            "There you go",
            "Here"
        ]

        if len(parameters["payment"]) == 1 and parameters["payment"][0] == self.info.payment:
            response = random.choice(response_give)
        else:
            response = random.choice(response_true).format(self.info.payment)

        return response

    def _question_safe_deposit(self, parameters):
        response_true = [
            "Yes, thank you for asking",
            "Yes",
        ]
        response_false = [
            "Oh No, glad you reminded me! I left my {} in the room",
        ]

        if self.info.clear_deposit:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false).format(self.info.left_item)

        return response

    def _question_transportation_assistance(self, parameters):
        response_true = [
            "Yes, thank you so much",
            "Yes, thanks",
        ]

        response = random.choice(response_true)
        return response

    def _request_payment_signature(self, parameters):
        responses_true = [
            "Sure",
            "Okay",
            "Here? Okay",
        ]
        responses_false = [
            "where is it?",
            "do you mean.. where?",
            "where should I sign up?"
        ]

        if self._can_see_payment_sign_blank:
            response = random.choice(responses_true)
            response = {
                'text': response,
                'action': 'fill_credit_card_signature',
                'params': {
                    'signature': self.info.full_name
                }
            }

        else:
            response = random.choice(responses_false)

        return response, self._can_see_payment_sign_blank

    def _request_payment_signature_indicate(self, parameters):
        return self._request_payment_signature(parameters)

    def _request_key(self, parameters):
        response_true = [
            "Yes, here it is",
            "There you go",
        ]
        response_false = [
            "Sorry, I left it in the room"
        ]

        if self.info.with_key:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _request_name_room_num(self, parameters):
        response_true = [
            "I am {} from Room {}",
        ]

        response = random.choice(response_true).format(
            self.info.full_name,
            self.info.room_number
        )
        return response

    def _request_signature(self, parameters):
        responses_true = [
            "Sure",
            "Okay",
            "Here? Okay",
        ]
        responses_false = [
            "where is it?",
            "do you mean.. where?",
            "where should I sign up?"
        ]

        if self._can_see_sign_blank:
            response = random.choice(responses_true)
            response = {
                'text': response,
                'action': 'fill_credit_card_signature',
                'params': {
                    'signature': self.info.full_name
                }
            }

        else:
            response = random.choice(responses_false)

        return response, self._can_see_sign_blank

    def _request_signature_indicate(self, parameters):
        return self._request_signature(parameters)

    def _request_waiting(self, parameters):
        response_true = [
            "Sure",
            "take your time",
            "OK",
        ]

        response = random.choice(response_true)
        return response

    def _thanks(self, parameters):
        responses = [
            "you are welcome",
        ]
        response = random.choice(responses)

        return response
