from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from config_updated import create_cache
from model_building import build_model
from appos import welcome_note
from appos import price
import dill
import base64


@permission_classes((permissions.AllowAny,))
class Bot(viewsets.ViewSet):
    def create(self, request):
        CACHE_ID = 'CONSTANT5'
        question = request.data
        if 'user_id' in question:
            CACHE_ID = question['user_id']
        req_cache = create_cache(CACHE_ID)
        user_input = question['messageText']
        if question['messageSource'] == 'userInitiatedReset':
            req_cache.delete()
            question['messageSource'] = 'messageFromBot'
            question['messageText'] = welcome_note
            return Response(question)

        kern_RE = dill.loads(base64.b64decode(req_cache.user.aiml_kernel))
        question = build_model(question, kern_RE, req_cache.cache)
        if 'property' in question:
            req_cache.cache = question['property']
            req_cache.user.aiml_kernel = \
                base64.b64encode(dill.dumps(kern_RE))
            req_cache.user.save()
            req_cache.save()
        if len(question['property']) == 3 and {key: value for d in question["property"] for key, value in d.items()}.has_key('Dia'):
            if str({key: value for d in question["property"] for key, value in d.items()}['Dia']) == 'with sugar':
                list1 = []
                for i in {key: value for d in question['property'] for key, value in d.items()}['Items']:
                    for key, value in price.items():
                        if i == key:
                            list1.append(value)
                list2 = {key: value for d in question['property'] for key, value in d.items()}['Num']
                list1 = [int(i) for i in list1]
                list2 = [int(i) for i in list2]
                mul = [a*b for a, b in zip(list1, list2)]
                total = sum(mul)
                question['messageText'] = [['I hope you are not having diabetes..and thats gooood.'], ['Your order will be delivered soon and your total bill is ' + str(total) + 'Rs.'], ['Thank You for visiting.']]
                question['messageSource'] = 'messageFromUser'
                reply = question
                return Response(reply)
            elif str({key: value for d in question["property"] for key, value in d.items()}['Dia']) == 'without sugar':
                list1 = []
                for i in {key: value for d in question['property'] for key, value in d.items()}['Items']:
                    for key, value in price.items():
                        if i == key:
                            list1.append(value)
                list2 = {key: value for d in question['property'] for key, value in d.items()}['Num']
                list1 = [int(i) for i in list1]
                list2 = [int(i) for i in list2]
                mul = [a*b for a, b in zip(list1, list2)]
                total = sum(mul)
                question['messageText'] = [['Ohhh..I think you are having diabetes..Please take care.'], ['Your order will be delivered soon and your total bill is ' + str(total) + 'Rs.'], ['Thank You for visiting.']]
                question['messageSource'] = 'messageFromUser'
                reply = question
                return Response(reply)
        else:
            reply = question
            return Response(reply)
        return Response(reply)
