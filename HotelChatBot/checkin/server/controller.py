from .guest_info import GuestInfo
from .chatbot import ChatBot
from .evaluator import Evaluator
from ..models import CheckinRecord, CheckinDialogRecord


class CheckinController(object):
    """docstring for Controller"""

    def __init__(self, gender='0'):
        super(CheckinController, self).__init__()
        self.chatbot = ChatBot(GuestInfo(gender=gender))
        deposit = (100 * self.chatbot.info.booking_info.duration +
                   self.chatbot.info.booking_info.r_rate * self.chatbot.info.booking_info.duration * 1.77)
        self.evaluator = Evaluator(deposit)

        self._dialog_record = ''

    def _record_dialog(self, input_text, output_text):
        string = 'User:{}\nBot:{}\n'.format(input_text, output_text)
        self._dialog_record = self._dialog_record + string

    def calculate_score(self, current_user):
        score, max_score, each_score = self.evaluator.finalize()

        if current_user.is_authenticated:
            # Do something for authenticated users.
            CheckinRecord.add_record(
                user=current_user,
                score=score,
                max_score=max_score,
                each_score=each_score
            )
        CheckinDialogRecord.add_record(
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
            "params": comment.format(response) + "\n\n" + format_score(each_score)
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

    def get_info(self, info_type, name=None, confirm_no=None):
        if not name and not confirm_no:
            return False, {'last_name': self.chatbot.info.booking_info.l_name}
        if name:
            if name != self.chatbot.info.booking_info.l_name:
                return False, {}
        if confirm_no:
            if confirm_no != self.chatbot.info.booking_info.res_no:
                return False, {}

        if info_type == 'booking_info':
            self.evaluator.locate_reservation()
            return True, vars(self.chatbot.info.booking_info)
        elif info_type == 'business_info':
            return True, vars(self.chatbot.info.business_info)
        else:
            return False, {}

    def show_sign(self):
        self.chatbot.set_showed_sign()

    def show_term(self):
        self.chatbot.set_showed_term()

    def submit_reg(self, reg_data):
        self.evaluator.check_reg(reg_data,
                                 id_info=self.chatbot.info.id_info,
                                 business_info=self.chatbot.info.business_info)


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
