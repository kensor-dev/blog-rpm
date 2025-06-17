from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Post

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    """Get all posts with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        posts = Post.query.order_by(Post.created_at.desc())\
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
        return jsonify({'error': 'Failed to get posts'}), 500


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post by ID"""
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        return jsonify({
            'post': post.to_dict(include_content=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get post'}), 500


@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """Create a new post"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not all(k in data for k in ('title', 'content')):
            return jsonify({'error': 'Missing required fields: title, content'}), 400
        
        title = data['title'].strip()
        content = data['content'].strip()
        
        if not title or not content:
            return jsonify({'error': 'Title and content cannot be empty'}), 400
        
        if len(title) > 200:
            return jsonify({'error': 'Title must be 200 characters or less'}), 400
        
        # Create new post
        post = Post(
            title=title,
            content=content,
            author_id=current_user_id
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': post.to_dict(include_content=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create post'}), 500


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update a post (only by author)"""
    try:
        current_user_id = get_jwt_identity()
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        if post.author_id != current_user_id:
            return jsonify({'error': 'You can only edit your own posts'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields if provided
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({'error': 'Title cannot be empty'}), 400
            if len(title) > 200:
                return jsonify({'error': 'Title must be 200 characters or less'}), 400
            post.title = title
        
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return jsonify({'error': 'Content cannot be empty'}), 400
            post.content = content
        
        db.session.commit()
        
        return jsonify({
            'message': 'Post updated successfully',
            'post': post.to_dict(include_content=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update post'}), 500


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a post (only by author)"""
    try:
        current_user_id = get_jwt_identity()
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        if post.author_id != current_user_id:
            return jsonify({'error': 'You can only delete your own posts'}), 403
        
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete post'}), 500


@posts_bp.route('/search', methods=['GET'])
def search_posts():
    """Search posts by title and content"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        posts = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) | 
            (Post.content.ilike(f'%{query}%'))
        ).order_by(Post.created_at.desc())\
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
        return jsonify({'error': 'Search failed'}), 500 