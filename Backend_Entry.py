from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TriviaGame.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return 'Hello, Trivia Game!'

if __name__ == '__main__':
    app.run(debug=True)
