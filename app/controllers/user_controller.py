from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.services.admin import AdminService

user_bp = Blueprint('users', __name__)


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    """Get user profile by user ID"""
    current_user_id = get_jwt_identity()
    
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({
            "success": False, 
            "message": "Access denied. You can only access your own profile."
        }), 403
    
    try:
        user = UserService.get_user_with_profile(user_id)
        
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        
        user_data = user.serialize()
        if user.profile:
            user_data['profile'] = user.profile.serialize()
        else:
            user_data['profile'] = None
        
        return jsonify({
            "success": True,
            "message": "User profile retrieved successfully",
            "data": user_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving user profile: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve user profile"
        }), 500


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    """Update user profile by user ID"""
    current_user_id = get_jwt_identity()
    
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({
            "success": False,
            "message": "Access denied. You can only update your own profile."
        }), 403
    
    try:
        user_data = request.get_json()
        
        if not user_data:
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400
        
        if 'is_admin' in user_data and current_user_id != user_id:
            if not AdminService.is_admin(current_user_id):
                return jsonify({
                    "success": False,
                    "message": "Only admins can modify admin status"
                }), 403
        
        updated_user = UserService.update_user(user_id, user_data)
        
        user_with_profile = UserService.get_user_with_profile(user_id)
        user_response = user_with_profile.serialize()
        
        if user_with_profile.profile:
            user_response['profile'] = user_with_profile.profile.serialize()
        else:
            user_response['profile'] = None
        
        return jsonify({
            "success": True,
            "message": "User profile updated successfully",
            "data": user_response
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error updating user profile: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to update user profile"
        }), 500


@user_bp.route('/<int:user_id>/deactivate', methods=['PATCH'])
@jwt_required()
def deactivate_user(user_id):
    """Deactivate user account"""
    current_user_id = get_jwt_identity()
    
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403
    
    try:
        updated_user = UserService.deactivate_user(user_id)
        
        return jsonify({
            "success": True,
            "message": "User account deactivated successfully",
            "data": updated_user.serialize()
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error deactivating user: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to deactivate user account"
        }), 500


@user_bp.route('/<int:user_id>/activate', methods=['PATCH'])
@jwt_required()
def activate_user(user_id):
    """Activate user account - Admin only"""
    current_user_id = get_jwt_identity()
    
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if not AdminService.is_admin(current_user_id):
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403
    
    try:
        updated_user = UserService.activate_user(user_id)
        
        return jsonify({
            "success": True,
            "message": "User account activated successfully",
            "data": updated_user.serialize()
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error activating user: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to activate user account"
        }), 500


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Check if user is logged in and return current user information"""
    try:
        current_user_id = get_jwt_identity()
        
        # Convert to int if needed (JWT identity might be string)
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        # Get current user with profile
        user = UserService.get_user_with_profile(current_user_id)
        
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found",
                "logged_in": False
            }), 404
        
        # Check if user is active
        if not user.is_active:
            return jsonify({
                "success": False,
                "message": "User account is deactivated",
                "logged_in": False
            }), 403
        
        # Prepare user data with profile
        user_data = user.serialize()
        if user.profile:
            user_data['profile'] = user.profile.serialize()
        else:
            user_data['profile'] = None
        
        return jsonify({
            "success": True,
            "message": "User is logged in",
            "logged_in": True,
            "data": user_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error checking user login status: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to verify login status",
            "logged_in": False
        }), 500


@user_bp.route('/check-auth', methods=['GET'])
@jwt_required()
def check_authentication():
    """Simple endpoint to check if JWT token is valid"""
    try:
        current_user_id = get_jwt_identity()
        
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        # Just verify the user exists and is active
        user = UserService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({
                "success": False,
                "authenticated": False,
                "message": "User not found"
            }), 404
        
        if not user.is_active:
            return jsonify({
                "success": False,
                "authenticated": False,
                "message": "User account is deactivated"
            }), 403
        
        return jsonify({
            "success": True,
            "authenticated": True,
            "user_id": user.id,
            "username": user.username,
            "message": "Token is valid"
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error checking authentication: {str(e)}")
        return jsonify({
            "success": False,
            "authenticated": False,
            "message": "Authentication check failed"
        }), 500
