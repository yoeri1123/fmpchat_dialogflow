# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os, requests
import sys
import json
import dialogflow_v2 as dialogflow
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

@app.route('/')
def front():
    #list_intent_info('fmpchat-udbn')
    #get_intent_info('fmpchat-udbn', '123456789')
    #create_intent("fmpchat-udbn")
    detect_intent_texts('fmpchat-udbn', '123456789', 'hi', 'ko-kr')
    return render_template('input_form.html')

@app.route('/chat-test', methods=['POST'])
def chatTest():
    #get_intent_info('fmpchat-udbn', '123456789')
    #list_intent_info('fmpchat-udbn')
    print('chat-test')
    content=request.form['content']
    print(content)
    unicode_content = str(unicode(content))
    print(unicode_content)
    response = detect_intent_texts('fmpchat-udbn', '123456789', unicode_content, 'ko-kr')
    print(response)
    return render_template('input_form.html')


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    #for text in texts:
    text_input = dialogflow.types.TextInput(
                text=str(unicode(texts)), language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
                session=session, query_input=query_input)

    print('=' * 20)
    #print(response)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    fulfillment_text = response.query_result.fulfillment_text.encode('utf-8')
    print('Fulfillment text: {}\n'.format(
            fulfillment_text))
    return fulfillment_text

def get_intent_info(project_id, session_id):
    intent_client = dialogflow.IntentsClient()
    intent_id = str("7fb45f6d-da59-423a-b179-b020490574a7")
    name  = intent_client.intent_path(project_id, intent_id)
    #print(name)
    response = intent_client.get_intent(name, intent_view="INTENT_VIEW_FULL")
    #print(response)
    update_intent(project_id, response)

def list_intent_info(project_id):
    intent_client = dialogflow.IntentsClient()
    parent = intent_client.project_agent_path(project_id)
    intents = intent_client.list_intents(parent, intent_view="INTENT_VIEW_FULL")
    for intent in intents:
        print(intent)
        print('=' * 20)
        print('Intent name: {}'.format(intent.name))
        print('Intent display_name: {}'.format(intent.display_name))
        print('Action: {}\n'.format(intent.action))
        print('Root followup intent: {}'.format(
            intent.root_followup_intent_name))
        print('Parent followup intent: {}\n'.format(
            intent.parent_followup_intent_name))

        print('Input contexts:')
        for input_context_name in intent.input_context_names:
            print('\tName: {}'.format(input_context_name))

        print('Output contexts:')
        for output_context in intent.output_contexts:
            print('\tName: {}'.format(output_context.name))    

def create_intent(project_id):
    intent_client = dialogflow.IntentsClient()
    parent = intent_client.project_agent_path(project_id)
    
    display_name = "create_intent_test"

    #intent = {} #json format
    training_phrases_parts = ['example', 'test']
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    # text response
    message_texts=['ok', 'thanks']

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intent_client.create_intent(parent, intent)

def update_intent(project_id, intent):
    intent_client = dialogflow.IntentsClient()
    str_training = str(intent.training_phrases)
    print(str_training.find('parts'))
    print(str_training)
    training_pharses_parts=[]
    print(list(str_training))
    #json_str = json.loads(str_training)
    #training_phrases_parts.append()
    training_phrases_parts = ['examples', 'tests']
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    
    intent_id = str("7fb45f6d-da59-423a-b179-b020490574a7")
    name  = intent_client.intent_path(project_id, intent_id)
    response = intent_client.get_intent(name)

    response.training_phrases.extend(training_phrases)
    #print(intent)
    #response = intent_client.update_intent(intent)

def delete_intent(project_id, intent_id):
    intents_client = dialogflow.IntentsClient()

    intent_path = intents_client.intent_path(project_id, intent_id)

    intents_client.delete_intent(intent_path)

@app.route('/mongo',methods=['GET', 'POST'])
def mongoTest():
    print("come?")
    client = MongoClient('mongodb://localhost:27017/')
    db = client.newDatabase
    collection = db.mongoTest
    results = collection.find()
    client.close()
    return render_template('mongo.html', data=results)

@app.route('/saveForm', methods=["POST"])
def saveForm():
    print("come saveForm?")
    if request.method=="POST":
        swname=request.form['name']
        userId=request.form['email']
        phoneNum=request.form['phone']
        content=request.form['message']
        datas={'swname': swname, 'userid': userId, 'phonemum': phoneNum, 'content':content} 
        print(datas)
        res=requests.post(INPUT_URL, data=datas)
        if res.text=="SUCCESS":
            print("SAVE SUCCESS")
    return render_template('input_form.html')

@app.route('/saveMongo', methods=['POST'])
def mongoSave():
    print("come saveMongo?")
    client = MongoClient('mongodb://localhost:27017/')
    db = client.newDatabase
    collection = db.mongoTest
    name=request.form['name']
    content=request.form['content']
    mdict={'name': name, 'content': content}
    print(mdict)
    collection.insert_one(mdict)
    return redirect(url_for('mongoTest'))

@app.route('/deleteMongo', methods=['POST'])
def mongoDelete():
    print("come deleteMongo?")    
    client = MongoClient('mongodb://localhost:27017/')
    db = client.newDatabase
    collection = db.mongoTest
    idNum=request.form['idNum']
    collection.delete_one({'_id':ObjectId(idNum)})
    return redirect(url_for('mongoTest'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

