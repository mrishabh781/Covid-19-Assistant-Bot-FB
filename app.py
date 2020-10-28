import nltk
nltk.download('punkt')
from flask import Flask, request
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import re
import requests
from bs4 import BeautifulSoup


FB_API_URL = 'https://graph.facebook.com/v6.0/me/messages?access_token=<PAGE_ACCESS_TOKEN>'
VERIFY_TOKEN = 'rishabh121'
PAGE_ACCESS_TOKEN = "your access code"
def get_stats():
    page = requests.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find(class_='content-inner').find_all_next('div')
    date = (data[1].text)
    total_case = data[3].find(class_="maincounter-number").text
    total_case = total_case.strip()
    death = data[6].find(class_="maincounter-number").find('span').text
    recovered = data[8].find(class_="maincounter-number").find('span').text
    currently_infected =  data[11].find(class_='number-table-main').text
    mild_condition = data[15].find(class_='number-table').text +' ('+ data[15].find('strong').text  +'%)'
    serious = data[15].find_all(class_='number-table')
    serious = serious[1].text +' ('+ data[15].find_all('strong')[1].text  +'%)'
    result_text = "*Worldwide Stats Of Coronavirus*\n({})\n\nTotal Coronavirus Cases: *{}*\nTotal Deaths: *{}*\nTotal Recovered: *{}*\n\n *ACTIVE CASES*\nCurrently Infected Patients: *{}*\nIn Mild Condition: *{}*\nCritical: *{}*".format(date,total_case,death,recovered,currently_infected,mild_condition,serious)
    result_text += '\n\nFor more information visit\nsource: https://www.worldometers.info/coronavirus/'
    return result_text


def get_headline(num=10):
    url="https://tinyurl.com/wqjrzv5"
    url1 ="https://economictimes.indiatimes.com/news/politics-and-nation/coronavirus-cases-in-india-live-news-latest-updates-march25/liveblog/74801993.cms"
    page = requests.get(url1)
    soup = BeautifulSoup(page.content, 'html.parser')
    headline1 = soup.find(class_='textDiv l1')
    time = soup.find(class_='date-time')
    result2 = str((time.find(class_='time').text))
    result2 += '\n*' + str((headline1.find('h1').text)) + '*\n'
    #result2 += str(headline1.find('p').text) + '\n'
    headline = soup.find(class_='clearfix container hitDone')
    headline = headline.find_all(class_='eachStory')
    x = 0
    result_text = result2
    for i in headline:
        if x < num:
            result = '*' + str(i.find(class_="timeStamp").find('span').text) + '* '
            try:
                result += str(i.find(class_="updateText").find('h2').text) + '\n'
            except:
                pass
            try:
                result += str(i.find(class_="updateText").find('h3').text) + '\n'
            except:
                pass
            '''try:
                result += str(i.find(class_="updateText").find('h3').find(class_='quote').text) + '\n'
            except:
                pass
            try:
                result += str(i.find(class_="updateText").find(class_='blogSysn').text) + '\n'
            except:
                pass
            try:
                result += str(i.find(class_="updateText").find(class_='blogSysn').find('li').text) + '\n'
            except:
                pass'''
            x += 1
            if (len(result_text + result) < 1560):
                result_text += '\n' + result
    result_text += '\nsource : ' + url
    print(len(result_text))
    return result_text

def live_india():
    page = requests.get('https://www.mohfw.gov.in/')
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find('div', class_='information_row').find_all("div",class_="iblock")
    people_scanned = data[0].text
    total_active = data[1].find(class_='info_label').text +': *'
    total_active += data[1].find('span').text +'*\n'
    cured = data[2].find(class_='info_label').text +': *'
    cured += data[2].find('span').text +'*\n'
    #migrated = data[3].text
    death = data[3].find(class_='info_label').text +': *'
    star = soup.find('div', class_='contribution').find('p').text
    death += data[3].find('span').text +'*'

    '''result_text = "*Status of INDIA*\nActive COVID 2019 cases: *{}*\nCured COVID 2019 cases: *{}*\nMigrated COVID-19 Patient: *{}*\nNo. of Deaths: *{}*\nPassengers screened at airport: *{}*\n\n*{}*".format(
        total_active[-4:].strip(), cured[-3:].strip(), migrated[-2:].strip(), death[-3:].strip(),
        people_scanned[-12:].strip(), star).strip()'''
    result_text = "*Status of India*\n" + total_active + cured + death + '\n\n' + star
    result_text += "\n\nFor Detailed Report of every State\nVisit: http://www.mohfw.gov.in/"

    return result_text

def live_state(state):
    print(state)
    result_text = ''
    try:
            page = requests.get('https://www.mohfw.gov.in/')
            soup = BeautifulSoup(page.content, 'html.parser')
            data = soup.find('div', class_="content newtab").find('tbody').find_all('tr')
            result_text = ''
            for i in data:
                print(i.find_all('td')[1].text.lower())
                if state in i.find_all('td')[1].text.lower():
                    result_text += "*" + i.find_all('td')[1].text + "*\nTotal cases(Indian): *" + i.find_all('td')[
                        2].text + '*' + '\nTotal cases (Foreigner): *' + i.find_all('td')[3].text + '*\n' + 'Cured: *' + \
                                   i.find_all('td')[4].text + '*\nDeath: *' + i.find_all('td')[5].text + '*\n'
                    break
            if result_text == "":
                result_text += "Your state {} has no confirmed case of Corona Virus yet.".format(state)
            result_text += '\n' + live_india()
            return result_text
    except:
        return ''




def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


app = Flask(__name__)

with open("intentsN.json") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])
print(docs_x)
stemmer = LancasterStemmer()
words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)
training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)
tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

#model = tflearn.DNN(net)

try:
    model = tflearn.DNN(net)
    model.load("model.tflearn")

except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)





def get_bot_response(inp):
    inp = inp.lower()
    print(inp)
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    print('Probability- '+str(results[results_index])+'\n')
    #print(results[results_index])
    tag = labels[results_index]

    if results[results_index] > 0.7: 
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        result = random.choice(responses)
        flag = 0
        state1 = re.findall('[a-z]+', inp)
        for i in state1:
            if len(i)<4 or i=='pradesh':
                if i != 'goa':
                    state1.remove(i) 
        state_list = ["andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat",
                      "haryana", "himachal pradesh", "union territory of jammu and kashmir", "jharkhand", "karnataka", "kerala",
                      "union territory of ladakh",
                      "madhya pradesh", "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha",
                      "punjab", "rajasthan", "sikkim", "tamil", "nadu", "telangana", "tripura", "uttar pradesh",
                      "uttarakhand", "west", "bengal", "andaman", "nicobar", "union territory of chandigarh", "dadra nagar haveli",
                      "daman diu", "lakshadweep", "delhi", "puducherry"]
        if tag == 'live':
            print(state1)
            for i in state1:

                #print(i)
                for x in state_list:

                    if i in x:
                        result = live_state(x)
                        flag = 1
                        break
            if not flag:
                result = live_india()

        if tag == 'headline':
            num = re.findall('[0-9]+', inp)
            try:
                if int(num[0]) <= 8:
                    result = get_headline(int(num[0]))
                else:
                    result = get_headline()
            except:
                result = get_headline()

        if tag == "world_stat":
            result = get_stats()

    else:
        result = '⚠ Unable to understand your query. Please try to use simple keywords.\n\nTry asking *manual* to know more.\n\n*Pl note* if the bot is now replying, please go to our youtube video and reply here with *new token* from the video descriptionbox.\n'

    return result

    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    result = get_bot_response(message)
    print(result)
    list = [" *Live status of Bihar* or any State", "If you're done say *bye*", "*Status of China*",
            "*Avoid traveling to?*","*janata curfew*" ,"*Top affected countries*", "*Updates by government*",
            " *Top 5 headlines on CoronaVirus* ", "*Can coronavirus spread in hot weather*",
            "*How likely am I to catch the corona disease*",
            " *World stats* -gives you live stats related to COVID-19 ",
            "*Live data of India* -gives you stats of corona virus in India",
            " *Death ratio* or *Ratio* - gives you the stats about death ratio.", "Safety precautions", "Food safety",
            "Country wise status", "how effective are masks"]
    x = '💡Try asking:- '
    if "We hope this" not in result:
        send_message(sender,result+'\n\n'+x+random.choice(list))
    else:
        share = "Tune Yourself With *Covid-19-Assistant-Bot* .\nPlease click on the following link and see the video on how to use the bot.\nPl Go through the *Video description*\n\nVideo Link:- https://tinyurl.com/rnc7yea"
        send_message(sender,result)
        send_message(sender,share)
    #resp.message(data['intents'][1])


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))



@app.route("/", methods=['GET'])
def listen():
    return verify_webhook(request)


@app.route("/", methods=['POST'])
def resp():
    payload = request.json
    event = payload['entry'][0]['messaging']
    print(event)
    for x in event:
        if is_user_message(x):
            text = x['message']['text']
            sender_id = x['sender']['id']
            respond(sender_id, text)

    return "ok"

if __name__ == "__main__":
    app.run()




#done
