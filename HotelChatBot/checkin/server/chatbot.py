import random


class ChatBot:
    def __init__(self, info):
        self.info = info

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
            'info_terms_conditions_indicate': self._info_terms_conditions_indicate,
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
            'request_signature_indicate': self._request_signature_indicate,
            'request_tags': self._request_tags,
            'request_waiting': self._request_waiting,
            'test_fullfillment': self._test_fullfillment,
            'thanks': self._thanks,
        }
        self._can_see_sign_blank = False
        self._can_see_term = False

    def __call__(self, intent, parameters):
        print('intent: ', intent)
        print('parameters:', parameters)

        function = self._intent_mapping[intent]
        return function(parameters)

    def set_showed_sign(self):
        self._can_see_sign_blank = True

    def set_showed_term(self):
        self._can_see_term = True

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

    def _info_confirm_reservation_detail(self, parameters):
        responses = [
            "Yes, correct",
            "Yes, perfect",
            "Yes, all correct",
            "Yes"
        ]
        responses_ok = [
            "Okay",
            "Ok",
            "Yes"
        ]
        for k in parameters.keys():
            if parameters[k]:
                return random.choice(responses)

        response = random.choice(responses_ok)

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
            "I have a room reservation and I would like to check in",
            "I have a booking and I would like to check in",
            "I want to check in",
            "I have a reservation for today",
            "I have a room reservation",
            "I have a booking",
            "I have made a booking",

        ]
        reservation_detail = [
            "This is my booking confirmation",
            "This is my confirmation number",
            "This is my confirmation letter",
        ]
        if random.random() > 0.7:
            response = random.choice(reservation_detail)
            response = {
                'text': response,
                'action': 'show_card',
                'params': {
                    'title': "Confirmation Letter",
                    'content': str(self.info.booking_info).replace('\n', '<br>').replace('\t', '&nbsp;' * 2)
                }
            }
        else:
            response = random.choice(responses)

        return response

    def _info_breakfast(self, parameters):
        responses = [
            "Sure",
            "Great, thank you",
        ]
        response = random.choice(responses)

        return response

    def _info_key_usage(self, parameters):
        responses = [
            "Sure",
            "Great, thank you",
        ]
        response = random.choice(responses)

        return response

    def _info_wifi(self, parameters):
        responses = [
            "Sure",
            "Thank you",
        ]
        response = random.choice(responses)

        return response

    def _fill_up_your_contact(self, parameters):
        responses = [
            "Okay",
            "Yeah, I can do that",
            "Sure",
        ]
        response = random.choice(responses)
        response = {
            'text': response,
            'action': 'show_business_info',
            'params': vars(self.info.business_info)
        }

        return response

    def _finish_up(self, parameters):
        responses = [
            "thanks",
            "Great, thank you",
        ]
        response = random.choice(responses)
        response = {
            'text': response,
            'action': 'complete',
            'params': None,
        }
        return response

    def _info_something(self, parameters):
        responses = [
            "Sure",
            "Sure, thank you",
            "Okay, thanks",
        ]
        response = random.choice(responses)

        return response

    def _info_terms_conditions(self, parameters):
        responses_true = [
            "Okay, got it",
            "Yea, I saw",
            "Okay, I saw",
            "Noted"
        ]
        responses_false = [
            "where is it?",
            "do you mean.. where?",
            "Sorry, I can't see that"
        ]

        if self._can_see_term:
            response = random.choice(responses_true)
        else:
            response = random.choice(responses_false)

        return response, self._can_see_term

    def _info_terms_conditions_indicate(self, paramerters):
        return self._info_terms_conditions(paramerters)

    def _info_luggage_assistance(self, parameters):
        responses = [
            "thank you so much",
            "That’s great!",
        ]
        response = random.choice(responses)

        return response

    def _info_issue_key(self, parameters):
        responses = [
            "Okay, thank you",
            "Got it, thanks",
        ]
        response = random.choice(responses)

        return response

    def _info_locate_room(self, parameters):
        responses = [
            "Thank you",
            "thanks",
        ]
        response = random.choice(responses)

        return response

    def _question_anythingelse(self, parameters):
        response_true = [
        ]
        response_false = [
            "No, thank you",
            "I have nothing else",
            "I think I am good thank you",
        ]

        if self.info.special_issue:
            response = self.info.special_issue
        else:
            response = random.choice(response_false)

        return response

    def _question_bag_with_self(self, parameters):
        response_true = [
            "yes, my all bags are here",
            "yes, here",
        ]
        response_false = [
            "No, some of my bags are the bellman there",
            "No, some of my bags are the porter there",
        ]

        if self.info.bag_with_self:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _question_bag_with_porter(self, parameters):
        response_true = [
            "Yes, the {} has my bags".format(parameters['man']),
        ]
        response_false = [
            "No, all my bags are here",
        ]

        if self.info.bags_with_porter:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _question_luggage(self, parameters):
        response_true = [
            "Yes please",
            "Yes, I need assistance",
            "That will be nice",
            "Thanks, that will be great",
        ]
        response_false = [
            "No, thanks",
            "Thanks, I'm fine",
            "No, I can manage",
            "No I can bring it up by myself",
            "No thank you",
        ]

        if self.info.luggage_help:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _question_payment_cant_other(self, parameters):
        responses = [
            "fine, I would like to use {} please",
            "then, I prefer to pay by {}, thanks"
        ]

        response = random.choice(responses).format(self.info.payment)

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
        response_false = [
            "Can I use {}?",
            "Can I pay by {}?",
            "I am paying by {}",
            "I would like to use {}",
            "I will be paying by {}",
            "I would like to pay by {}",
        ]
        response_give = [
            "For payment? Sure",
            "There you go",
            "Here"
        ]

        if self.info.payment_other:
            response = random.choice(response_false).format(self.info.payment_other)
            self.info.payment_other = ''
        else:
            if len(parameters["payment"]) == 1 and parameters["payment"][0] == self.info.payment:
                response = random.choice(response_give)
            else:
                response = random.choice(response_true).format(self.info.payment)

        return response

    def _question_purpose(self, parameters):
        responses = [
            "{}",
            "A mix of both",
            "{}",
            "I come here for {}"
        ]

        response = random.choice(responses).format(self.info.purpose)

        return response

    def _question_receive_email(self, parameters):
        response_true = [
            "Sure, that will be nice",
            "Sure I look forward it",
            "Yes, I would like that",
            "Yes, I would like to receive the promotions and special offers",
        ]
        response_false = [
            "No, thanks",
            "Thank you but no",
        ]

        if self.info.receive_email:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _question_smoke(self, parameters):
        response_true = [
            "I prefer a smoking room, thanks",
            "I would like a smoking room",
            "Smoking room, please",
        ]
        response_false = [
            "I prefer a non smoking room, thanks",
            "I would like a non smoking room",
            "Non smoking room, please",
        ]

        if self.info.smoke:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _request_business_card(self, parameters):
        response_true = [
            "Yes, here it is",
            "Sure, there you go",
            "Sure",
        ]
        response_false = [
            "No, I don't have",
            "No, I don't have one with me",
            "Sorry, I do not have one",
        ]

        if self.info.business_card:
            response = random.choice(response_true)
            response = {
                'text': response,
                'action': 'show_card',
                'params': {
                    'title': "Business Card",
                    'content': str(self.info.business_info).replace('\n', '<br>').replace('\t', '&nbsp;' * 2)
                }
            }
        else:
            response = random.choice(response_false)

        return response

    def _request_departure_time_can_over(self, parameters):
        response_true = [
            "Okay, thank you",
            "Okay, thanks"
        ]
        response_false = []
        response_free = [
            "That's perfect",
            "Great! Thanks"
        ]
        if parameters['charge'] != 'no additional charge':
            if self.info.pay_overtime:
                response = random.choice(response_true)
            else:
                response = random.choice(response_false)
        else:
            response = random.choice(response_free)

        return response

    def _request_departure_time_cant_over(self, parameters):
        response_true = [
            "that's fine ..",
            "okay ...",
        ]
        response_false = []

        if self.info.overtime_no_argue:
            response = random.choice(response_true)
        else:
            response = random.choice(response_false)

        return response

    def _request_departure_time_check_again(self, parameters):
        responses = [
            "Okay, thanks",
            "thanks,",
        ]
        response = random.choice(responses)

        return response

    def _request_departure_time(self, parameters):
        response_true = [
            "can I check out at {}:00?",
            "is it possible to check out at {}:00?",

        ]
        response_false = [
            "about {} o'clock",
            "no problem, I will leave around {} o'clock",
        ]

        if self.info.will_over_time:
            response = random.choice(response_true).format(self.info.departure_time)
        else:
            response = random.choice(response_false).format(self.info.departure_time)

        return response

    def _request_passport(self, parameters):

        def check_passport(asking):
            driver_license = [
                'driver license',
                "driver's license",
                'drive license'
            ]
            ic = [
                'nric',
                "ic",
                'identification card',
                'identity card'
            ]

            if asking.lower() in driver_license and self.info.identity_document_true == "Driver's License":
                return True
            elif asking.lower() in ic and self.info.identity_document_true == "Identity Card":
                return True
            elif asking.lower() == self.info.identity_document_true.lower():
                return True
            elif asking.lower() == 'nric' and self.info.local:
                return True
            else:
                return False

        def true_doc_asked():
            for value in parameters["identity_document"]:
                if check_passport(value):
                    return True
            return False

        # print('identity_document_true:', self.info.identity_document_true)

        response_true = [
            "Sure, here you are",
            "there you go",
        ]
        response_false = [
            "No, I don't have {0} with me",
            "I do not have {0} with me. Can I use my {1} instead?",
            "Is it ok if I give you {1} instead",
        ]
        local_response = [
            "I am a local, I have my NRIC",
        ]

        if true_doc_asked():
            response = random.choice(response_true)
            response = {
                'text': response,
                'action': 'show_card',
                'params': {
                    'title': self.info.identity_document_true,
                    'content': str(self.info.id_info).replace('\n', '<br>').replace('\t', '&nbsp;' * 2)
                }
            }
            return response
        else:
            if self.info.local and random.random() > 0.8:
                response = random.choice(local_response)
            else:
                response = random.choice(response_false)

            ids = 'any of them'
            if len(parameters["identity_document"]) == 1:
                ids = 'my ' + parameters["identity_document"][0]

            response = response.format(ids,
                                       random.choice([
                                           self.info.identity_document_true,
                                           self.info.identity_document_fake]))

        return response

    def _request_passport_request(self, parameters):
        responses = [
            "Yes, here you are",
        ]
        response = random.choice(responses)
        response = {
            'text': response,
            'action': 'show_card',
            'params': {
                'title': self.info.identity_document_true,
                'content': str(self.info.id_info).replace('\n', '<br>').replace('\t', '&nbsp;' * 2)
            }
        }
        return response

    def _request_payment_cant_later(self, parameters):
        responses = [
            "okay, thanks",
            "that's fine",
            "okay ...",
        ]
        response = random.choice(responses)

        return response

    def _request_payment_cant_other(self, parameters):
        response_true = [
            "Well, I would like to use {} please.",
            "Okay, then I will paying by {}"
        ]
        response_false = [
            "I {} now",
            "I {} now. Can I pay later?",
        ]

        if self.info.pay_later:
            response = random.choice(response_false).format(self.info.pay_later_reason)
        else:
            response = random.choice(response_true).format(self.info.payment)

        return response

    def _request_payment_finish(self, parameters):
        responses = [
            "You are welcome",
            "No problem",
        ]
        response = random.choice(responses)

        return response

    def _request_payment(self, parameters):
        response_true = [
            "Okay",
            "No problem",
            "Sure"
        ]
        response_false = [
            "I {}, can I pay it later?",
            "I {} now, can I pay it tomorrow?",
        ]
        response_give = [
            "yes, here",
            "yes, there you go",
        ]
        # response_use_the_other = [
        #     "Can I use {} please?",
        #     "Can I pay by {} please?",
        # ]

        if self.info.pay_later:
            response = random.choice(response_false).format(self.info.pay_later_reason)
        else:
            if parameters["payment"] != self.info.payment:
                print('forward to question_payment intent')
                response = self._question_payment(parameters)
            else:
                if parameters["unit_currency"]:
                    if parameters["payment"] == "credit card":
                        response = random.choice(response_true) + ", you may proceed"
                    else:
                        response = random.choice(response_give)

                else:
                    if self.info.payment == "credit card":
                        # it mean FOA is asking for credit card
                        response = random.choice(response_give)
                    else:
                        response = random.choice(response_true)

        return response

    def _info_registration_card(self, parameters):
        responses = [
            "Sure, do whatever you have to do",
            "Okay",
            "Alright",
        ]
        response = random.choice(responses)

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
                'action': 'fill_signature',
                'params': {
                    'signature': self.info.id_info.full_name
                }

            }

        else:
            response = random.choice(responses_false)

        return response, self._can_see_sign_blank

    def _request_signature_indicate(self, parameters):
        return self._request_signature(parameters)

    def _request_tags(self, parameters):
        responses = [
            "Sure, thank you",
            "Sure, there you go. Thank you",
        ]

        response = random.choice(responses)

        return response

    def _request_waiting(self, parameters):
        responses = [
            "Sure",
            "take your time",
            "OK",
        ]
        response = random.choice(responses)

        return response

    def _test_fullfillment(self, parameters):
        responses = [
            "hello",
        ]
        response = random.choice(responses)

        return response

    def _thanks(self, parameters):
        responses = [
            "you are welcome",
        ]
        response = random.choice(responses)

        return response
