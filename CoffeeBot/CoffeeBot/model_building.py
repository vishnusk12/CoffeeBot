from config_updated import preprocess
from config_updated import get_count
from config_updated import get_item
from config_updated import get_sugar
from config_updated import top_classifier
import random
from appos import *


def generate_reply_for_items(reply, Dia):
    items = ['espresso', 'doppio', 'macchiato', 'ristretto', 'americano', 'cappuccino', 'latte', 'mocha', 'affogato', 'black tea', 'lemon tea', 'green tea', 'oolong tea', 'white tea', 'fermented tea', 'yellow tea']
    items = ",".join(items)
    first_reply = 'We provide ' + items.title() + ' as drinks here'
    second_reply = random.choice(items_quest)
    reply['messageText'] = [[first_reply], [second_reply]]
    return reply


def generate_reply(entity, reply, entity_list_available):
    if entity == 'Num':
        items = [i['Items'] for i in reply['property'] if 'Items' in i]
        if len(items) == 0:
            items = ''
        else:
            items = ",".join(items[0])
        first_reply = ['Choosing ' + items.title() + ' is a good option.', items.title() + '\
 is a fine selection', items.title() + ' is a nice choice']
        if items != '':
            reply['messageText'] = [[random.choice(first_reply)], [random.choice(num_quest)]]
        else:
            reply['messageText'] = [[random.choice(fillers)], [random.choice(num_quest)]]
        return reply
    elif entity == 'Items':
        Dia = [i['Dia'] for i in reply['property'] if 'Dia' in i]
        if len(Dia) == 0:
            Dia = ''
        else:
            Dia = Dia[0]
        if Dia != '':
            reply = generate_reply_for_items(reply, Dia)
            return reply
        else:
            reply['messageText'] = [['Sorry We dont have that item here..' ], ['We offer espresso, doppio, macchiato, ristretto, americano, cappuccino, latte, mocha, affogato, black tea, lemon tea, green tea, oolong tea, white tea, fermented tea and yellow tea.'], ['What would you like to have..?']]
            return reply


def build_model(question, kern_medical, symp_list):
    input = question['messageText']
    cleaned_user_input = preprocess(question['messageText'])
    question['messageText'] = cleaned_user_input
    kernel_reply = kern_medical.respond(question['messageText'])
    if not "Sorry, I didn't get you.." in kernel_reply:
        response = {}
        response['property'] = []
        response['messageText'] = [kernel_reply]
        return response
    response = {}
    response['property'] = []
    response['property'].extend(symp_list)
    t_label = top_classifier(question['messageText'])
    if t_label == 1 and question['messageSource'] == 'messageFromUser':
        response['messageText'] = [['We offer a wide variety of Tea and Coffee..'], ['Espresso : 70Rs', ' Doppio : 60Rs', ' Macchiato : 80Rs', ' Ristretto : 70Rs', ' Americano : 90Rs', ' Cappuccino : 60Rs', ' Latte : 80Rs', ' Mocha : 70Rs', ' Affogato : 90Rs', ' Black Tea : 40Rs', ' Lemon Tea : 40Rs', ' Green Tea : 50Rs', ' Oolong Tea : 60Rs', ' White Tea : 50Rs', ' Fermented Tea : 60Rs', ' Yellow Tea : 70Rs']
, ['Please Select from the above List']]
        return response
    elif t_label == 2 and question['messageSource'] == 'messageFromUser':
        response['property'] = get_item(question['messageText'], response['property'])
        response['property'] = get_count(question['messageText'], response['property'])
        response['property'] = get_sugar(question['messageText'], response['property'])
        entity_list = ['Items', 'Num', 'Dia']
        entity_list_available = [i.keys()[0] for i in response['property']]
        entity_list = [i for i in entity_list if i not in entity_list_available]
        for i in entity_list:
            if i == 'Dia':
                items = [i['Items'] for i in response['property'] if 'Items' in i]
                num = [i['Num'] for i in response['property'] if 'Num' in i]
                if len(items) != 0 and len(num) != 0:
                    items_ = ",".join(items[0])
                    num_ = ",".join(num[0])
                    if len(items[0]) >= 2:
                        response['messageText'] = [['You ordered ' + num_ + ' ' + 'cups of ' + ' ' + items_.title() + ' ' + 'respectively'], [random.choice(fillers)], ['Please tell me.., you want it with or without sugar..?']]
                    else:
                        response['messageText'] = [['You ordered ' + num_ + ' ' + 'cups of ' + ' ' + items_.title()], [random.choice(fillers)], ['Please tell me.., you want it with or without sugar..?']]
                    return response
                else:
                    response['messageText'] = [[random.choice(fillers)], ['With or Without Sugar..?']]
                return response
            elif i not in entity_list_available:
                response = generate_reply(i, response, entity_list_available)
                return response
            else:
                continue
        return response
    elif t_label == 3 and "Sorry, I didn't get you.." in kernel_reply:
        response['messageText'] = ['Please Ask Something that we can provide / related to coffee shop']
        return response
