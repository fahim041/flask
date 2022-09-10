from flask import Blueprint, request, jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from src.database import db, Bookmark

bookmarks = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')


@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    user = get_jwt_identity()
    if request.method == 'POST':
        body = request.json.get('body', '')
        url = request.json.get('url', '')

        if not validators.url(url):
            return jsonify({'error': 'invalid url'}), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({'error': 'bookmark already exist'}), HTTP_400_BAD_REQUEST

        bookmark = Bookmark(body=body, url=url, user_id=user)
        db.session.add(bookmark)
        db.session.commit()

        return ({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visits': bookmark.visits,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), HTTP_201_CREATED

    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 3, type=int)
        bookmarks = Bookmark.query.filter_by(
            user_id=user).paginate(page=page, per_page=per_page)
        data = []
        for item in bookmarks.items:
            data.append({
                'id': item.id,
                'url': item.url,
                'short_url': item.url,
                'visits': item.visits,
                'body': item.body,
                'created_at': item.created_at,
                'updated_at': item.updated_at
            })
        meta = {
            'page': bookmarks.page,
            'pages': bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num
        }
        return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


@bookmarks.get('/<int:id>')
@jwt_required()
def get_bookmark(id):
    user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'bookmark is not found'}), HTTP_404_NOT_FOUND

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK


@bookmarks.patch('/<int:id>')
@bookmarks.put('/<int:id>')
@jwt_required()
def edit_bookmark(id):
    user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'Bookmark not found'})

    body = request.json.get('body', '')
    url = request.json.get('url', '')

    if not validators.url(url):
        return jsonify({'error': 'invalid url'}), HTTP_400_BAD_REQUEST

    bookmark.url = url
    bookmark.body = body

    db.session.commit()

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK


@bookmarks.delete('/<int:id>')
@jwt_required()
def delete_bookmark(id):
    user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'Bookmark not found'})

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
