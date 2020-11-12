import os
import json
import dialogflow_v2beta1
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .server.controller import CheckinController
import configparser
config = configparser.ConfigParser()

config.read('config.txt')

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 config['DEFAULT']['PRIVATE_KEY_PATH']))

PROJECT_ID = config['DEFAULT']['PROJECT_ID']
SUB_PROJECT_ID = config['DEFAULT']['CHECKIN_PROJECT_ID']
LANGUAGE_CODE = config['DEFAULT']['LANGUAGE_CODE']


@csrf_exempt
def webhook_dialogflow(request):
    checkin_controller = request.session.get('checkin_controller')
    request.session['checkin_controller'] = checkin_controller

    # build a request object
    req = json.loads(request.body)
    req = req["queryResult"]

    input_text = req["queryText"]
    intent = req["intent"]["displayName"]
    action = req["action"] if 'action' in req.keys() else None
    params = req["parameters"] if 'parameters' in req.keys() else None

    response = checkin_controller(input_text, intent, action, params)

    res = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        response
                    ]
                }
            }
        ]
    }

    # return response
    return JsonResponse(res, safe=False)


@csrf_exempt
def chat(request):
    checkin_controller = request.session.get('checkin_controller')
    request.session['checkin_controller'] = checkin_controller

    req = json.loads(request.body)
    # print("Request:")
    # print(json.dumps(req, indent=4))

    input_text = req["message"]

    if input_text == '/complete':
        current_user = request.user
        output = checkin_controller.calculate_score(current_user)
        del request.session['checkin_controller']
    else:
        session_id = "1234"

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

        # output = response.query_result.fulfillment_text
        output = checkin_controller(input_text, intent, action, params)

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
        del request.session['checkin_controller']
    except:
        pass
    request.session['checkin_controller'] = CheckinController(gender)
    return HttpResponse('Success!!')


def locate_search(request):
    checkin_controller = request.session.get('checkin_controller')
    request.session['checkin_controller'] = checkin_controller

    last_name = request.GET['last_name']
    confirmation_num = request.GET['confirmation_num']

    success, parameters_dict = checkin_controller.get_info('booking_info', last_name, confirmation_num)

    if success:
        parameters_dict['result'] = 'Find!'
    else:
        parameters_dict['result'] = 'Not Find!'
    return JsonResponse(parameters_dict)


def show_sign(request):
    checkin_controller = request.session.get('checkin_controller')
    request.session['checkin_controller'] = checkin_controller
    checkin_controller.show_sign()
    return HttpResponse('Success!!')


def show_term(request):
    checkin_controller = request.session.get('checkin_controller')
    request.session['checkin_controller'] = checkin_controller

    checkin_controller.show_term()
    return HttpResponse('Success!!')


@csrf_exempt
def submit_reg(request):
    checkin_controller = request.session.get('checkin_controller')
    request.session['checkin_controller'] = checkin_controller

    req = get_json(request.body.decode("utf-8"))
    # print("Request:")
    # print(json.dumps(req, indent=4))

    checkin_controller.submit_reg(req)
    return HttpResponse('Success!!')


def get_json(post_data: str):

    post_data = post_data.split('&')
    result = {}
    for p in post_data:
        k, v = p.split('=')
        result[k] = v.replace('+', ' ')
    return result


def handler404(request, *args):
    response = render(request, 'error_pages/404.html')
    response.status_code = 404
    return response


def handler500(request, *args):
    response = render(request, 'error_pages/500.html')
    response.status_code = 500
    return response
