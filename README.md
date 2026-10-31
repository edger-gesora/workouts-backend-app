# Workout Tracker Backend 

## Description

This is a backend API for a workout tracking app for personal trainers. It is made with Flask, SQLAlchemy and Marshmallow. A trainer can create workouts, create reusable exercises, and add exercises to workouts with reps, sets or duration.

The database has three tables: `exercises`, `workouts` and `workout_exercises` (a join table). A workout has many exercises through `workout_exercises`, and an exercise can be used in many workouts.

## Validations

- Table constraints: exercise names must be unique and not empty, workout duration must be greater than 0, reps and sets cannot be negative.
- Model validations: exercise name and category, workout duration, and reps/sets/duration_seconds are checked with `@validates`.
- Schema validations: Marshmallow checks name length, allowed categories, duration ranges, and that at least one of reps, sets or duration_seconds is given.

## Installation

1. Clone the repo:
   ```
   git clone https://github.com/YOUR-USERNAME/workout-app-backend.git
   cd workout-app-backend
   ```
2. Install the packages and open the virtual environment (needs Python 3.8.13 or newer and Pipenv):
   ```
   pipenv install
   pipenv shell
   ```
3. Create the database and add the starter data:
   ```
   cd server
   export FLASK_APP=app.py
   flask db upgrade head
   python seed.py
   ```

## Running the app

From the `server` folder:
```
python app.py
```
The API runs at http://localhost:5555

## Running the tests

From the `server` folder:
```
pytest -v
```

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | Show one workout with its exercises, including reps, sets and duration |
| POST | /workouts | Create a workout (date, duration_minutes, notes) |
| DELETE | /workouts/<id> | Delete a workout and its workout_exercises |
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Show one exercise and the workouts it is used in |
| POST | /exercises | Create an exercise (name, category, equipment_needed) |
| DELETE | /exercises/<id> | Delete an exercise and its workout_exercises |
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout (reps, sets, duration_seconds) |

Valid categories are `strength`, `cardio` and `flexibility`.