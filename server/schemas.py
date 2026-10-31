from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(['strength', 'cardio', 'flexibility'])
    )
    equipment_needed = fields.Bool()

    @validates('name')
    def validate_name(self, value):
        if value.strip() == '':
            raise ValidationError('Name cannot be blank')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(validate=validate.Length(max=200))


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))
    workout = fields.Nested(WorkoutSchema, dump_only=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def check_at_least_one(self, data, **kwargs):
        if (data.get('reps') is None and data.get('sets') is None
                and data.get('duration_seconds') is None):
            raise ValidationError('Give at least one of reps, sets or duration_seconds')


# used when viewing a single workout or exercise
class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, exclude=('workout',), dump_only=True
    )


class ExerciseDetailSchema(ExerciseSchema):
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema, many=True, exclude=('exercise',), dump_only=True
    )