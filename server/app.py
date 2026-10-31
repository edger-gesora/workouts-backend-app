from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    ExerciseSchema, ExerciseDetailSchema,
    WorkoutSchema, WorkoutDetailSchema,
    WorkoutExerciseSchema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(WorkoutSchema(many=True).dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(WorkoutDetailSchema().dump(workout)), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = WorkoutSchema().load(request.get_json())
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except ValueError as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 400
    return jsonify(WorkoutSchema().dump(workout)), 201

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    # the cascade on the model also deletes its WorkoutExercises
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted'}), 200

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(ExerciseSchema(many=True).dump(exercises)), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(ExerciseDetailSchema().dump(exercise)), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = ExerciseSchema().load(request.get_json())
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except ValueError as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An exercise with that name already exists'}), 400
    return jsonify(ExerciseSchema().dump(exercise)), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'}), 200

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return jsonify({'error': 'Workout or exercise not found'}), 404

    try:
        data = WorkoutExerciseSchema().load(request.get_json())
        workout_exercise = WorkoutExercise(
            workout_id=workout_id, exercise_id=exercise_id, **data
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except ValueError as err:
        db.session.rollback()
        return jsonify({'error': str(err)}), 400
    return jsonify(WorkoutExerciseSchema().dump(workout_exercise)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)