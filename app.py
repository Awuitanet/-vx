from flask import Flask

app = Flask(__name__, static_folder='.')

@app.route('/')
def inicio():
    return """
    <h1>Hiiiii</h1>
    <p>¿Crees que soy pro?</p>
    <a href="/si"><button>Sí</button></a>
    <a href="/no"><button>No</button></a>
    """

@app.route('/si')
def si():
    return '<img src="/jeje%20like.jpeg" width="500">'

@app.route('/no')
def no():
    return '<img src="/bbae58d9-73a6-4386-93ca-c862d63236fc.jpeg" width="500">'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
