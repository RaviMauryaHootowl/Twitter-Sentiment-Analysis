from flask import Flask, request, jsonify
import re, string
import pickle
import requests
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from PyDictionary import PyDictionary
dictionary=PyDictionary()
load_dotenv()
import os
app = Flask(__name__)
cors = CORS(app)


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def getSentiment(query):
  # Loading
  f = open('my_classifier.pickle', 'rb')
  classifier = pickle.load(f)
  f.close()

  url = "https://api.twitter.com/1.1/search/tweets.json?q=" + query + "&result_type=mixed&count=100&lang=en&tweet_mode=extended"
  bearerToken = os.environ.get("bearerToken")
  headers = {
    'Authorization': 'Bearer ' + bearerToken,
    'Cookie': 'personalization_id="v1_4uBj+Xmfoj7IhxyR5B/adg=="; guest_id=v1%3A159473130844397528; lang=en'
  }

  response = requests.request("GET", url, headers=headers)
  texts = []
  tweets = response.json()['statuses']

  for tweet in tweets:
      texts.append(tweet['full_text'])
  nOfPos = 0

  for text in texts:
      custom_tokens = remove_noise(word_tokenize(text))
      if classifier.classify(dict([token, True] for token in custom_tokens)) == 'Positive':
        nOfPos+=1
  return nOfPos/len(texts)*100

@app.route('/api/v1/search')
def hello():
  print(request.args['query'])

  #synonyms
  simWords=dictionary.synonym(request.args['query'])
  
  countWords=0

  if simWords<5:
    countWords=len(simWords)
    simPercent=[0]*len(simWords)
  else:
    countWords=5
    simPercent=[0]*5
    
  for i in range(countWords):
    simPercent[i]=getSentiment(simWords[i])

  percent = getSentiment(request.args['query'])
  return jsonify({"percent":percent,"simWords":simWords,"simPercent":simPercent})

if __name__ == '__main__':
    app.run(debug=True)