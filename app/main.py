# app/main.py
from flask import Flask, render_template
from routes.recognition_routes import recognition_routes

app = Flask(__name__)
app.register_blueprint(recognition_routes)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
