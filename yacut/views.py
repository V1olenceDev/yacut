from flask import flash, redirect, render_template, url_for
from werkzeug.wrappers.response import Response

from . import app, db
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def add_url_map() -> str:
    form = UrlForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if URLMap.find_by_short_id(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.', 'non-unique')
            return render_template('index.html', form=form)
        
        url_map = URLMap(
            original=form.original_link.data,
            short=(custom_id if custom_id else URLMap.get_unique_short_id())
        )
        url_map.save()
        flash(url_for('follow_url_map', short=url_map.short, _external=True), 'link')

    return render_template('index.html', form=form)



@app.route('/<string:short>')
def follow_url_map(short: str) -> Response:
    url_map = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url_map.original)