from flask import jsonify
import traceback


class APIResponse:
    @staticmethod
    def success(data=None, message=None, status_code=200):
        response = {}
        if message:
            response['message'] = message
        if data:
            response['data'] = data
        else:
            response['data'] = {}
        return jsonify(response), status_code
    
    @staticmethod
    def error(message, error_code=None, status_code=400, details=None, solution=None):
        response = {
            'error': error_code or 'Error',
            'message': message
        }
        if details:
            response['details'] = details
        if solution:
            response['solution'] = solution
        return jsonify(response), status_code
    
    @staticmethod
    def validation_error(missing_fields):
        return APIResponse.error(
            message=f"Missing required fields: {', '.join(missing_fields)}",
            error_code='Validation Error',
            status_code=400,
            details={'missing': missing_fields},
            solution="Provide all required fields in the request body"
        )
    
    @staticmethod
    def unauthorized(message="Authentication required", details=None, solution=None):
        return APIResponse.error(
            message=message,
            error_code='Unauthorized',
            status_code=401,
            details=details or "Valid JWT token not provided or token has expired",
            solution=solution or "Include 'Authorization: Bearer <token>' header with a valid JWT token"
        )
    
    @staticmethod
    def forbidden(message="Access denied", details=None, solution=None):
        return APIResponse.error(
            message=message,
            error_code='Forbidden',
            status_code=403,
            details=details or "User role does not have permission",
            solution=solution or "Contact administrator to grant required permissions"
        )
    
    @staticmethod
    def not_found(message="Resource not found", details=None, solution=None):
        return APIResponse.error(
            message=message,
            error_code='Not Found',
            status_code=404,
            details=details or "The requested resource does not exist",
            solution=solution or "Check the resource ID or create the resource first"
        )
    
    @staticmethod
    def conflict(message="Resource already exists", details=None, solution=None):
        return APIResponse.error(
            message=message,
            error_code='Conflict',
            status_code=409,
            details=details or "A resource with these details already exists",
            solution=solution or "Use a different username/email or update existing resource"
        )
    
    @staticmethod
    def server_error(message="An unexpected error occurred", error=None):
        details = str(error) if error else None
        solution = "Check server logs for more details or contact support"
        return APIResponse.error(
            message=message,
            error_code='Internal Server Error',
            status_code=500,
            details=details,
            solution=solution
        )
    
    @staticmethod
    def handle_exception(e):
        """Catch and format any exception"""
        error_type = type(e).__name__
        error_msg = str(e)
        
        if error_msg:
            details = f"{error_type}: {error_msg}"
        else:
            details = error_type
        
        return APIResponse.server_error(
            message=f"Server error: {error_msg}",
            error=details
        )