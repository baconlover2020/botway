from flask import Flask
import pickle


app = Flask(__name__)

@app.route("/agecode")
def get_code():
    with open('vars/winway', 'rb') as f:
        return pickle.load(f)

@app.route("/hogwarts")
def get_names():
    return "Steinway HWA-RPG SpaceBlythe MariettaSanchez"

@app.route("/autorizados")
def get_autorizados():
    return "Steinway lolaindaeyo teresa170 Guinness Maifoy Osgar Luiza. Ranger. Tassi."

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)
