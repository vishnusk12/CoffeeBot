from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.externals import joblib
from .models import RequestCache
import dill
import aiml
from appos import *
from nltk.tokenize import word_tokenize
import string
import re
from CoffeeBot.models import UserCache

exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
brain_file = "/home/server/CoffeeBot/CoffeeBot/Coffee.brn"


def preprocess(text):
    text = text.replace(',', ' ')
    words = text.split()
    reformed = [appos[word] if word in appos else word for word in words]
    reformed = " ".join(reformed)
    tokens = word_tokenize(reformed)
    punc_free = [ch for ch in tokens if ch not in exclude]
    normalized = [lemma.lemmatize(word).lower() for word in punc_free]
    reformed = " ".join(normalized)
    return reformed


def get_count(text, cache_list):
    text = text.lower()
    dict_ = {}
    list_ = re.findall('\d+', text)
    try:
        text = re.sub(r'\beach\b', list_[0], text)
        list_new = re.findall('\d+', text)
    except:
        pass
    if len(list_) != 0:
        dict_['Num'] = list_new
        cache_list = remove_duplicate(cache_list, 'Num')
        cache_list.append(dict_)
    else:
        for key, value in count.items():
            for j in value:
                match = re.compile(r"\b%s\b"%(j))
                num = match.findall(text)
                if len(num) != 0:
                    dict_ = {}
                    dict_['Num'] = [key]
                    cache_list = remove_duplicate(cache_list, 'Num')
                    cache_list.append(dict_)
    return cache_list


def get_item(text, cache_list):
    dict_item_name = {}
    text = text.lower()
    item_name = re.findall(r"(?=("+'|'.join(items)+r"))", text)
    if len(item_name) != 0:
        dict_item_name['Items'] = item_name
        cache_list = remove_duplicate(cache_list, 'Items')
        cache_list.append(dict_item_name)
    return cache_list


def get_sugar(text, cache_list):
    text = text.lower()
    text = re.sub(r'\bnot diabetic\b', 'notdiabetic', text)
    text = re.sub(r'\bwith sugar\b', 'withsugar', text)
    text = re.sub(r'\bwithout sugar\b', 'withoutsugar', text)
    text = re.sub(r'\bnt diabetic\b', 'ntdiabetic', text)
    text = re.sub(r'\bwith out\b', 'without', text)
    text = re.sub(r'\bno sugar\b', 'nosugar', text)
    text = re.sub(r'\bsugar less\b', 'sugarless', text)
    dict_sugar = {}
    for key, value in sugar.items():
        for i in value:
            match = re.compile(r"\b%s\b"%(i))
            sug = match.findall(text)
            if len(sug) != 0:
                dict_sugar['Dia'] = key
                cache_list = remove_duplicate(cache_list, 'Dia')
                cache_list.append(dict_sugar)
    return cache_list


def create_cache(CACHE_ID):
    import base64
    try:
        req_cache = RequestCache.objects.get(cache_id=CACHE_ID)
    except RequestCache.DoesNotExist:
        kern_medical = aiml.Kernel()
        kern_medical.bootstrap(brainFile=brain_file)
        kernel_str = dill.dumps(kern_medical)
        kernel_str = base64.b64encode(kernel_str)
        req_cache = RequestCache.objects.create(cache_id=CACHE_ID, cache=[],
                                                user=UserCache.objects
                                                .create(aiml_kernel=kernel_str)
                                                )
    return req_cache


def top_classifier(text):
    text_list = []
    text_list.append(str(text))
    clf = joblib.load('/home/server/CoffeeBot/model_files/model_coffee.pkl')
    t_label = clf.predict(text_list)
    return t_label[0]


def remove_duplicate(list_, key_name):
    if len(list_) != 0:
        for dicts in list_:
            if dicts.has_key(key_name):
                list_.remove(dicts)
    return list_
