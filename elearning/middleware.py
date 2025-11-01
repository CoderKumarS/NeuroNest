from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class MessageLimitMiddleware(MiddlewareMixin):
    """
    Middleware to limit the number of messages per request to prevent accumulation
    """
    
    def process_response(self, request, response):
        # Get messages from the request
        storage = messages.get_messages(request)
        message_list = list(storage)
        
        # If there are more than 5 messages, keep only the last 5
        if len(message_list) > 5:
            # Clear all messages
            storage.used = False
            storage._queued_messages = []
            
            # Add only the last 5 messages
            for message in message_list[-5:]:
                messages.add_message(request, message.level, message.message, message.tags)
        
        return response