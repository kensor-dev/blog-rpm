from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import User, Post, Comment

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post_comments(post_id):
    """Get comments for a specific post"""
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        comments = Comment.query.filter_by(post_id=post_id)\
                              .order_by(Comment.created_at.asc())\
                              .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'comments': [comment.to_dict() for comment in comments.items],
            'total': comments.total,
            'pages': comments.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': comments.has_next,
            'has_prev': comments.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get comments'}), 500


@comments_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a specific comment by ID"""
    try:
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        return jsonify({
            'comment': comment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get comment'}), 500


@comments_bp.route('', methods=['POST'])
@jwt_required()
def create_comment():
    """Create a new comment"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not all(k in data for k in ('content', 'post_id')):
            return jsonify({'error': 'Missing required fields: content, post_id'}), 400
        
        content = data['content'].strip()
        post_id = data['post_id']
        
        if not content:
            return jsonify({'error': 'Content cannot be empty'}), 400
        
        # Check if post exists
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Create new comment
        comment = Comment(
            content=content,
            post_id=post_id,
            author_id=current_user_id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create comment'}), 500


@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """Update a comment (only by author)"""
    try:
        current_user_id = get_jwt_identity()
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        if comment.author_id != current_user_id:
            return jsonify({'error': 'You can only edit your own comments'}), 403
        
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        content = data['content'].strip()
        
        if not content:
            return jsonify({'error': 'Content cannot be empty'}), 400
        
        comment.content = content
        db.session.commit()
        
        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update comment'}), 500


@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Delete a comment (only by author)"""
    try:
        current_user_id = get_jwt_identity()
        comment = Comment.query.get(comment_id)
        
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        if comment.author_id != current_user_id:
            return jsonify({'error': 'You can only delete your own comments'}), 403
        
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete comment'}), 500


@comments_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_comments(user_id):
    """Get comments by a specific user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        comments = Comment.query.filter_by(author_id=user_id)\
                              .order_by(Comment.created_at.desc())\
                              .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'comments': [comment.to_dict() for comment in comments.items],
            'total': comments.total,
            'pages': comments.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': comments.has_next,
            'has_prev': comments.has_prev
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user comments'}), 500 