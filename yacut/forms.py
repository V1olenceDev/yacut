from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                regex=r'^[A-Za-z0-9]{1,16}$',
                message='Недопустимое имя для короткой ссылки.'
            )
        ]
    )
    submit = SubmitField('Создать')