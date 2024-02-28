import string, re
from datetime import datetime
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
        size = SIZE_SHORT_ID
        max_attempts = MAX_ATTEMPTS
        for _ in range(max_attempts):
            short_id = ''.join(choices(CHAR_SET, k=size))
            if not cls.query.filter_by(short=short_id).first():
                return short_id
        raise Exception("Не удалось сгенерировать уникальный короткий идентификатор.")

    
    @classmethod
    def find_by_short_id(cls, short_id: str):
        return cls.query.filter_by(short=short_id).first()


    def save(self):
        if not self.original or not re.match(r'^https?://', self.original):
            raise InvalidAPIUsageError('Неверный формат URL.')
        if self.short:
            pattern = r'^[A-Za-z0-9]{1,16}$'
            if not re.match(pattern, self.short):
                raise InvalidAPIUsageError('Указано недопустимое имя для короткой ссылки')
        if not self.short:
            self.short = self.get_unique_short_id()
        if self.find_by_short_id(self.short):
            raise InvalidAPIUsageError('Предложенный вариант короткой ссылки уже существует.')
        db.session.add(self)
        db.session.commit()
    
    
    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'original': self.original,
            'short': self.short,
            'timestamp': self.timestamp
        }

    def from_dict(self, data: dict[str, str]) -> None:
        api_column_mapping = {
            'url': 'original',
            'custom_id': 'short'
        }
        for field in ['url', 'custom_id']:
            if field in data:
                setattr(self, api_column_mapping[field], data[field])