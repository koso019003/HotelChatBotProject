from .guest_info import GuestInfo
from .chatbot import ChatBot
from .evaluator import Evaluator
from ..models import CheckoutRecord, CheckoutDialogRecord


class CheckoutController(object):
    """docstring for Controller"""

    def __init__(self, gender='0'):
        super(CheckoutController, self).__init__()
        self.chatbot = ChatBot(GuestInfo(gender=gender))
        self.evaluator = Evaluator()
        self._dialog_record = ''

    def _record_dialog(self, input_text, output_text):
        string = 'User:{}\nBot:{}\n'.format(input_text, output_text)
        self._dialog_record = self._dialog_record + string

    def calculate_score(self, current_user):
        score, max_score, each_score = self.evaluator.finalize()

        if current_user.is_authenticated:
            # Do something for authenticated users.
            CheckoutRecord.add_record(
                user=current_user,
                score=score,
                max_score=max_score,
                each_score=each_score
            )
        CheckoutDialogRecord.add_record(
            body=self._dialog_record,
        )

        response = 'Your score is {}/{}'.format(score, max_score)
        grade = score / max_score
        if grade > 85:
            comment = 'Perfect!\n{}'
        elif grade > 70:
            comment = 'Good!\n{}'
        else:
            comment = 'Keep going!\n{}'

        return {
            "text": response,
            "action": 'finalize',
            "params": comment.format(response) + "\n\n" + format_score(each_score),
        }

    def __call__(self, input_text, intent, action, params):
        success = True
        # Get response
        # response = "Text response from webhook for number {}".format(len(response))
        response = self.chatbot(intent, params)

        if isinstance(response, tuple):
            response, success = response

        # Record dialog
        if isinstance(response, dict):
            output_text = response['text']
        else:
            output_text = response
        self._record_dialog(input_text, output_text)

        if not success:
            return response

        # Record mark
        self.evaluator(input_text, intent, params)

        return response

    def get_info(self, info_type, name=None, room_num=None):
        if not name and not room_num:
            return False, {'last_name': self.chatbot.info.stay_info.l_name}
        if name:
            if name != self.chatbot.info.stay_info.l_name:
                return False, {}
        if room_num:
            if room_num != self.chatbot.info.stay_info.room_num:
                return False, {}

        if info_type == 'stay_info':
            return True, vars(self.chatbot.info.stay_info)
        else:
            return False, {}

    def show_sign(self):
        self.chatbot.set_showed_sign()

    # def show_sign_payment(self):
    #     self.chatbot.set_showed_sign_payment()

    def submit_bill(self, minibar_data):
        self.chatbot.set_showed_folio()
        self.evaluator.check_minibar(
            minibar_data=minibar_data,
            minibar_items=self.chatbot.info.minibar_item_dict)


def format_score(score_dict):
    string = ""
    for key, value in score_dict.items():
        if isinstance(value, dict):
            for k, v in value.items():
                string = string + "        {}: {}\n".format(
                    k.replace('_', ' ').title(), 'V' if v else 'X')
            string = string + "\n"
        else:
            string = string + "{}: {}\n".format(key.replace('_', ' ').title(), value)
    return string.strip()
