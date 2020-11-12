import os
import json
import dialogflow_v2beta1
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .server.controller import CheckoutController
import configparser
config = configparser.ConfigParser()

config.read('config.txt')

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 config['DEFAULT']['PRIVATE_KEY_PATH']))

PROJECT_ID = config['DEFAULT']['PROJECT_ID']
SUB_PROJECT_ID = config['DEFAULT']['CHECKOUT_PROJECT_ID']
LANGUAGE_CODE = config['DEFAULT']['LANGUAGE_CODE']

# Create your views here.


@csrf_exempt
def chat(request):
    checkout_controller = request.session.get('checkout_controller')
    request.session['checkout_controller'] = checkout_controller

    req = json.loads(request.body)
    # print("Request:")
    # print(json.dumps(req, indent=4))

    input_text = req["message"]

    if input_text == '/complete':
        current_user = request.user
        output = checkout_controller.calculate_score(current_user)
        del request.session['checkout_controller']
    else:
        session_id = "1235"

        text_input = dialogflow_v2beta1.types.TextInput(text=input_text, language_code=LANGUAGE_CODE)
        query_input = dialogflow_v2beta1.types.QueryInput(text=text_input)

        sub_agents = dialogflow_v2beta1.types.SubAgent(project=SUB_PROJECT_ID)
        query_params = dialogflow_v2beta1.types.QueryParameters(sub_agents=(sub_agents,))

        session_client = dialogflow_v2beta1.SessionsClient()
        session = session_client.session_path(PROJECT_ID, session_id)

        response = session_client.detect_intent(session=session, query_input=query_input, query_params=query_params)

        intent = response.query_result.intent.display_name
        action = response.query_result.action
        params = response.query_result.parameters

        # print("Query text:", response.query_result.query_text)
        # print("Detected intent:", response.query_result.intent.display_name)
        # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        # print("Fulfillment text:", response.query_result.fulfillment_text)

        output = checkout_controller(input_text, intent, action, params)

    if isinstance(output, dict):
        res = {
            "response": output['text'],
            "action": output['action'],
            "params": output['params']
        }
    else:
        res = {
            "response": output,
            "action": ""
        }
    return JsonResponse(res, safe=False)


def ready(request):
    gender = request.GET['gender']
    try:
        del request.session['checkout_controller']
    except:
        pass
    request.session['checkout_controller'] = CheckoutController(gender)
    return HttpResponse('Success!!')


def stay_detail_search(request):
    checkout_controller = request.session.get('checkout_controller')
    request.session['checkout_controller'] = checkout_controller

    last_name = request.GET['last_name']
    room_num = request.GET['room_num']

    success, parameters_dict = checkout_controller.get_info('stay_info', last_name, room_num)

    if success:
        parameters_dict['result'] = 'Find!'
    else:
        parameters_dict['result'] = 'Not Find!'
    return JsonResponse(parameters_dict)


def submit_bill(request):
    checkout_controller = request.session.get('checkout_controller')
    request.session['checkout_controller'] = checkout_controller

    req = get_json(request.body.decode("utf-8"))
    # print("Request:")
    # print(json.dumps(req, indent=4))

    checkout_controller.submit_bill(req)
    return HttpResponse('Success!!')


def show_sign(request):
    checkout_controller = request.session.get('checkout_controller')
    request.session['checkout_controller'] = checkout_controller
    checkout_controller.show_sign()
    return HttpResponse('Success!!')


# def show_sign_payment(request):
#     checkout_controller = request.session.get('checkout_controller')
#     request.session['checkout_controller'] = checkout_controller
#     checkout_controller.show_sign_payment()
#     return HttpResponse('Success!!')


def get_json(post_data: str):
    post_data = post_data.split('&')
    result = {}
    for p in post_data:
        k, v = p.split('=')
        result[k] = v.replace('+', ' ')
    return result
