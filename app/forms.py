from flask_wtf import FlaskForm
from wtforms import widgets, StringField, TextAreaField, SelectField, IntegerField, SubmitField, URLField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Length

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CourseForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[Length(max=500)])
    year = SelectField('Год окончания', choices=[], coerce=int, validators=[DataRequired()])
    link_id = SelectField('Тип ссылки', choices=[], coerce=int, validators=[DataRequired()])
    url = URLField('Описание')
    authors = TextAreaField('Авторы', validators=[Length(max=120), DataRequired()])
    category_id = SelectField('Категория', choices=[], coerce=int, validators=[DataRequired()])
    audience_id = SelectField('Аудитория', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    title = StringField('Название', validators=[Length(max=200)])
    years = MultiCheckboxField('Год', choices=[])
    categories = MultiCheckboxField('Категория', choices=[])
    audiences = MultiCheckboxField('Аудитория', choices=[])
    submit = SubmitField() 