def validate_input(user_input):
    if not user_input or not isinstance(user_input, str):
        return False
    return True

def format_response(response):
    if isinstance(response, dict) and 'message' in response:
        return response['message']
    return "Sorry, I didn't understand that."