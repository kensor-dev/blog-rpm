from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Post

users_bp = Blueprint('users', __name__)


@users_bp.route('/<nickname>', methods=['GET'])
def get_user_profile(nickname):
    """Get user profile by nickname"""
    try:
        user = User.query.filter_by(nickname=nickname).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user's posts
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        posts = Post.query.filter_by(author_id=user.id)\
                         .order_by(Post.created_at.desc())\
                         .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'user': user.to_dict(),
            'posts': {
                'items': [post.to_dict(include_content=False) for post in posts.items],
                'total': posts.total,
                'pages': posts.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': posts.has_next,
                'has_prev': posts.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user profile'}), 500


@users_bp.route('/<nickname>/posts', methods=['GET'])
def get_user_posts(nickname):
    """Get posts by user nickname"""
    try:
        user = User.query.filter_by(nickname=nickname).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        posts = Post.query.filter_by(author_id=user.id)\
                         .order_by(Post.created_at.desc())\
                         .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'posts': [post.to_dict(include_content=False) for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user posts'}), 500


@users_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by nickname"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users = User.query.filter(User.nickname.ilike(f'%{query}%'))\
                         .order_by(User.nickname)\
                         .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': users.has_next,
            'has_prev': users.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500 