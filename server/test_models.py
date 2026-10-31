import pytest
from models import Exercise, Workout, WorkoutExercise


def test_exercise_name_cannot_be_empty():
    with pytest.raises(ValueError):
        Exercise(name='', category='strength')


def test_exercise_category_must_be_valid():
    with pytest.raises(ValueError):
        Exercise(name='Squat', category='dancing')


def test_workout_duration_must_be_positive():
    with pytest.raises(ValueError):
        Workout(duration_minutes=0)


def test_workout_exercise_reps_cannot_be_negative():
    with pytest.raises(ValueError):
        WorkoutExercise(reps=-5)


def test_valid_exercise_is_created():
    exercise = Exercise(name='Squat', category='strength')
    assert exercise.name == 'Squat'