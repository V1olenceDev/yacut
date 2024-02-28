import re
from http import HTTPStatus

from flask import jsonify, request
from flask.wrappers import Response

from . import app
from .exceptions import InvalidAPIUsageError
from .models import URLMap


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id: str) -> tuple[Response, int]:
    url_map = URLMap.find_by_short_id(short_id)
    if not url_map:
        raise InvalidAPIUsageError('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.to_dict().get('original')}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_url_map() -> tuple[Response, int]:
    data = request.get_json()
    if not data:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    url_map = URLMap()
    url_map.from_dict(data)
    url_map.save()
    return jsonify({
        'url': url_map.original,
        'short_link': 'http://localhost/' + url_map.short
    }), HTTPStatus.CREATED