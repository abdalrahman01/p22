from flask import Flask, request
# from AI2 import AI

PORT = 5001
HOST = '0.0.0.0'
DEVICE = 'cpu'

# bot = AI(device=DEVICE)

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/start_new_chat')
def start_new_chat():
    return 'Starting a new chat!'

@app.route('/chat', methods=['POST'])
def chat():
    text = request.get_json().get('text', '')
    return 'Chatting with AI: ' + text

if __name__ == '__main__':
    app.run(port=PORT, debug=True, host=HOST)
    