from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Habit, db

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/habits', methods=['GET', 'POST'])
def manage_habits():
    if request.method == 'POST':
        data = request.json
        new_habit = Habit(name=data['name'], frequency=data['frequency'])
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({"message": "Habit added!"}), 201
    else:
        habits = Habit.query.all()
        return jsonify([{"id": habit.id, "name": habit.name, "frequency": habit.frequency} for habit in habits])

@app.route('/api/habits/<int:id>', methods=['PUT', 'DELETE'])
def single_habit(id):
    habit = Habit.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.json
        habit.name = data['name']
        habit.frequency = data['frequency']
        db.session.commit()
        return jsonify({"message": "Habit updated!"})
    else:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({"message": "Habit deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
