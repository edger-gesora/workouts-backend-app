#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    # delete the join table first so nothing points to a missing row
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    squat = Exercise(name='Squat', category='strength', equipment_needed=True)
    pushup = Exercise(name='Push-up', category='strength', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    stretch = Exercise(name='Hamstring Stretch', category='flexibility', equipment_needed=False)
    db.session.add_all([squat, pushup, running, stretch])
    db.session.commit()

    leg_day = Workout(date=date(2026, 10, 25), duration_minutes=45, notes='Leg day')
    cardio_day = Workout(date=date(2026, 10, 27), duration_minutes=30, notes='Easy run')
    db.session.add_all([leg_day, cardio_day])
    db.session.commit()

    entries = [
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, reps=10, sets=3),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=stretch.id, duration_seconds=60),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=running.id, duration_seconds=1200),
        WorkoutExercise(workout_id=cardio_day.id, exercise_id=pushup.id, reps=15, sets=2),
    ]
    db.session.add_all(entries)
    db.session.commit()

    print('Database seeded')