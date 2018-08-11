from flask import request, jsonify, current_app, url_for
from . import api
from app.models import User, Post


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id).paginate(
        page, per_page=15, error_out=False
    )
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_users', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_users', page=page+1)
    return jsonify({
        'users': [user.to_json() for user in users],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })



@api.route('/users/', methods=['POST'])
def new_user():
    user = request.get_data()
    pass


@api.route('/users/<int:id>/posts', methods=['GET'])
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page+1)
    return jsonify({
        'user': user.name,
        'posts': [post.to_json() for post in posts],
        'next': next,
        'prev': prev,
        'count': pagination.total
    })


@api.route('/users/<int:id>/followed')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = User.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
