import string
import re
from datetime import datetime
from http import HTTPStatus
from random import choices
from typing import Any

from . import db
from .constants import SIZE_SHORT_ID, MAX_ATTEMPTS, SHORT_ID_PATTERN
from .exceptions import InvalidAPIUsageError

CHAR_SET = string.ascii_letters + string.digits


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_unique_short_id(cls) -> str:
        for _ in range(MAX_ATTEMPTS):
            short_id = ''.join(choices(CHAR_SET, k=SIZE_SHORT_ID))
            if not cls.find_by_short_id(short_id):
                return short_id
        raise InvalidAPIUsageError(
            'Не удалось сгенерировать уникальный короткий идентификатор.')

    @classmethod
    def find_by_short_id(cls, short_id: str):
        return cls.query.filter_by(short=short_id).first()

    def save(self):
        if self.short:
            pattern = SHORT_ID_PATTERN
            if not re.match(pattern, self.short):
                raise InvalidAPIUsageError('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)
        if not self.short:
            self.short = self.get_unique_short_id()
        existing_url_map = self.find_by_short_id(self.short)
        if existing_url_map and existing_url_map.id != self.id:
            raise InvalidAPIUsageError('Предложенный вариант короткой ссылки уже существует.', HTTPStatus.BAD_REQUEST)
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InvalidAPIUsageError('Ошибка сохранения в базу данных', HTTPStatus.INTERNAL_SERVER_ERROR)


    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'original': self.original,
            'short': self.short,
            'timestamp': self.timestamp
        }


    @staticmethod
    def from_dict(data: dict) -> 'URLMap':
        url_map = URLMap()
        url_map.original = data.get('url')
        url_map.short = data.get('custom_id') if data.get('custom_id') else URLMap.get_unique_short_id()
        return url_map