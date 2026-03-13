from flask import Flask, render_template, request
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'Atlas',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry I did not understand that. I believe I will soon.',
            'maximum_similarity_threshold': 0.70
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

 # Training with Personal data
training_data_simple = open('training_data/greetings.txt').read().splitlines()

training_data = training_data_simple

trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)

trainer_corpus.train("chatterbot.corpus.english")

app = Flask(__name__)
app.static_folder = 'static'

    
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    app.run()