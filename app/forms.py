from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class CourseForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[Length(max=500)])
    graduation_year = SelectField('Год окончания', choices=[], coerce=int, validators=[DataRequired()])
    category_id = SelectField('Категория', choices=[], coerce=int, validators=[DataRequired()])
    audience_id = SelectField('Аудитория', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить курс')