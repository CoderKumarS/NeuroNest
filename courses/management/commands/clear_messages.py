from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.contrib.messages.storage.session import SessionStorage

class Command(BaseCommand):
    help = 'Clear all stuck Django messages from sessions'

    def handle(self, *args, **options):
        cleared_count = 0
        
        # Get all sessions
        sessions = Session.objects.all()
        
        for session in sessions:
            session_data = session.get_decoded()
            
            # Check if session has messages
            if SessionStorage.session_key in session_data:
                # Clear messages from this session
                del session_data[SessionStorage.session_key]
                session.session_data = session.encode(session_data)
                session.save()
                cleared_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleared messages from {cleared_count} sessions'
            )
        )
        
        # Also clear any message-related session keys
        for session in sessions:
            session_data = session.get_decoded()
            message_keys = [key for key in session_data.keys() if 'message' in key.lower()]
            
            if message_keys:
                for key in message_keys:
                    del session_data[key]
                session.session_data = session.encode(session_data)
                session.save()
        
        self.stdout.write(
            self.style.SUCCESS('All stuck messages have been cleared!')
        )