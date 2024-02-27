import string
from datetime import datetime
from random import choice
from typing import Any

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def get_unique_short_id(cls) -> str:
        size = 6
        while True:
            short_id = ''.join([choice(
                string.ascii_lowercase
                + string.ascii_uppercase
                + string.digits
            ) for i in range(size)])
            existing_short_id = cls.query.filter_by(short=short_id).first()
            if not existing_short_id:
                return short_id

    def to_dict(self) -> dict[str, Any]:
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    def from_dict(self, data: dict[str, str]) -> None:
        api_column_mapping = {
            'url': 'original',
            'custom_id': 'short'
        }
        for field in ['url', 'custom_id']:
            setattr(self, api_column_mapping[field], data[field])