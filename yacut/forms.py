from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import MAX_URL_LENGTH, SHORT_ID_PATTERN


class UrlForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_URL_LENGTH)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                regex=SHORT_ID_PATTERN,
                message='Недопустимое имя для короткой ссылки.'
            )
        ]
    )
    submit = SubmitField('Создать')
