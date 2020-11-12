
import json


with open("temp_mapping.json", 'r', encoding='utf8') as fr:
    file = json.load(fr)


text = ""
text += "import random\n\n\n"
text += "class ChatBot:" + '\n'
text += "    " * 1 + "def __init__(self, info):" + '\n'
text += "    " * 2 + "self.info = info" + '\n'
text += "\n"
text += "    " * 2 + "self._intent_mapping = {" + '\n'
for key in file.keys():
    text += "    " * 3 + "'{}': self._{},".format(key, key.replace(' ', '_').replace('.', '_').lower()) + '\n'
text += "    " * 2 + '}' + "\n"

text += '\n'
text += "    " * 1 + "def __call__(self, intent, parameters):" + '\n'
text += "    " * 2 + "print('intent: ', intent)" + '\n'
text += "    " * 2 + "print('parameters:', parameters)" + '\n'
text += '\n'
text += "    " * 2 + "function = self._intent_mapping[intent]" + '\n'
text += "    " * 2 + "return function(action, parameters)" + '\n'



for key in file.keys():
    text += '\n'
    text += "    " * 1 + "def _{}(self, parameters):".format(key.replace(' ', '_').replace('.', '_').lower()) + '\n'
    responses = file[key]["guest"]

    if "question" in key or "request" in key:

        text += "    " * 2 + "response_true = [" + '\n'
        for res in responses:
            text += "    " * 3 + '"{}",'.format(res) + '\n'
        text += "    " * 2 + "]" + '\n'

        text += "    " * 2 + "response_false = []" + '\n'
        text += '\n'
        text += "    " * 2 + "if self.info.:" + '\n'
        text += "    " * 3 + 'response = random.choice(response_true)' + '\n'
        text += "    " * 2 + "else:" + '\n'
        text += "    " * 3 + 'response = random.choice(response_false)' + '\n'
    else:
        text += "    " * 2 + "responses = [" + '\n'
        for res in responses:
            text += "    " * 3 + '"{}",'.format(res) + '\n'
        text += "    " * 2 + "]" + '\n'
        text += "    " * 2 + 'response = random.choice(responses)' + '\n'

    text += '\n'
    text += "    " * 2 + "return response" + '\n'



with open("../HotelChatBot/checkout/server/chatbot.py", 'w', encoding='utf8') as fw:
    fw.write(text)
