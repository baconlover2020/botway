from flask import Flask

app = Flask(__name__)

@app.route("/agecode")
def get_code():
    return "TJUN 200"

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)
