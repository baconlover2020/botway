from flask import Flask
import pickle

app = Flask(__name__)

@app.route("/agecode")
def get_code():
    with open('vars/winway', 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)
