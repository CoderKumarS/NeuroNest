from django.core.management.base import BaseCommand
from tutor.models import AIConfiguration

class Command(BaseCommand):
    help = 'Set up default AI tutor configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            type=str,
            default='openai',
            help='AI provider (openai or gemini)'
        )
        parser.add_argument(
            '--api-key',
            type=str,
            help='API key for the AI service'
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Model name (e.g., gpt-3.5-turbo, gemini-pro)'
        )

    def handle(self, *args, **options):
        provider = options['provider']
        api_key = options.get('api_key')
        model = options.get('model')
        
        # Set default model based on provider
        if not model:
            if provider == 'openai':
                model = 'gpt-3.5-turbo'
            elif provider == 'gemini':
                model = 'gemini-pro'
            else:
                model = 'gpt-3.5-turbo'
        
        # Check if configuration already exists
        existing_config = AIConfiguration.objects.filter(is_active=True).first()
        if existing_config:
            self.stdout.write(
                self.style.WARNING(
                    f'Active AI configuration already exists: {existing_config.provider} - {existing_config.model_name}'
                )
            )
            
            if not api_key:
                self.stdout.write(
                    self.style.SUCCESS('Use Django admin to update the API key.')
                )
                return
        
        # Create or update configuration
        config, created = AIConfiguration.objects.get_or_create(
            provider=provider,
            model_name=model,
            defaults={
                'api_key': api_key or 'YOUR_API_KEY_HERE',
                'max_tokens': 1000,
                'temperature': 0.7,
                'daily_request_limit': 1000,
                'monthly_token_limit': 100000,
                'is_active': True
            }
        )
        
        if not created and api_key:
            config.api_key = api_key
            config.is_active = True
            config.save()
        
        # Deactivate other configurations
        AIConfiguration.objects.exclude(id=config.id).update(is_active=False)
        
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} AI configuration: {config.provider} - {config.model_name}'
            )
        )
        
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            self.stdout.write(
                self.style.WARNING(
                    'Please update the API key in Django admin or run this command with --api-key parameter'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                'AI Tutor setup complete! Students can now access the AI Tutor from the navigation menu.'
            )
        )