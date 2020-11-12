import os
import json

intents_path = '../files/backup/latest/checkout/intents/'
files = os.listdir(intents_path)

customer_files = []
concierge_files = []
for file in files:
    if '_usersays_en' in file:
        concierge_files.append(file)
    else:
        customer_files.append(file)

chatbot_mapping = {}

for file in customer_files:
    file = intents_path + file.replace('.json', '')
    with open("{}.json".format(file), 'r', encoding='utf8') as fr:
        customer = json.load(fr)
        name = customer["name"]
        responses = customer["responses"][0]["messages"]
        customer_sentences = []
        for res in responses:
            if res["type"] == "0":
                customer_sentences.extend(res["speech"])

    concierge_sentences = []
    if os.path.isfile("{}_usersays_en.json".format(file)):

        with open("{}_usersays_en.json".format(file), 'r', encoding='utf8') as fr:
            concierge = json.load(fr)

            for sentence in concierge:
                data = sentence["data"]
                full_sentence = ''
                for text in data:
                    if "meta" in text.keys():
                        full_sentence += text["meta"]
                    else:
                        full_sentence += text["text"]
                concierge_sentences.append(full_sentence)

    chatbot_mapping[name] = {
        "FOA": concierge_sentences,
        "guest": customer_sentences
    }
    with open('temp_mapping.json', 'w', encoding='utf8') as fw:
        json.dump(chatbot_mapping, fw, indent=4)
