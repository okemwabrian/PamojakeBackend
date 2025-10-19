from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from contact.models import ContactMessage
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Create mock data for testing'

    def handle(self, *args, **options):
        # Create test users if they don't exist
        user1, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        user2, created = User.objects.get_or_create(
            username='jane_smith',
            defaults={
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith'
            }
        )

        # Create Applications
        Application.objects.get_or_create(
            user=user1,
            first_name='John',
            defaults={
                'type': 'single',
                'status': 'pending',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone_main': '+1234567890',
                'address_1': '123 Main St',
                'city': 'Minneapolis',
                'state_province': 'MN',
                'zip_postal': '55401',
                'declaration_accepted': True,
                'constitution_agreed': True
            }
        )

        Application.objects.get_or_create(
            user=user2,
            first_name='Jane',
            defaults={
                'type': 'double',
                'status': 'approved',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'phone_main': '+1987654321',
                'address_1': '456 Oak Ave',
                'city': 'St. Paul',
                'state_province': 'MN',
                'zip_postal': '55102',
                'spouse': 'Mike Smith',
                'spouse_phone': '+1555666777',
                'declaration_accepted': True,
                'constitution_agreed': True
            }
        )

        # Create Claims
        Claim.objects.get_or_create(
            user=user1,
            member_name='John Doe',
            defaults={
                'claim_type': 'medical',
                'relationship': 'self',
                'amount_requested': Decimal('500.00'),
                'incident_date': date.today() - timedelta(days=30),
                'description': 'Medical expenses for hospital visit',
                'status': 'pending'
            }
        )

        Claim.objects.get_or_create(
            user=user2,
            member_name='Sarah Smith',
            defaults={
                'claim_type': 'education',
                'relationship': 'daughter',
                'amount_requested': Decimal('1000.00'),
                'amount_approved': Decimal('800.00'),
                'incident_date': date.today() - timedelta(days=60),
                'description': 'School tuition assistance',
                'status': 'approved'
            }
        )

        # Create Payments
        Payment.objects.get_or_create(
            user=user1,
            transaction_id='TXN123456',
            defaults={
                'amount': Decimal('50.00'),
                'type': 'membership',
                'status': 'completed',
                'payment_method': 'PayPal',
                'description': 'Monthly membership fee'
            }
        )

        Payment.objects.get_or_create(
            user=user2,
            transaction_id='TXN789012',
            defaults={
                'amount': Decimal('100.00'),
                'type': 'shares',
                'status': 'pending',
                'payment_method': 'Credit Card',
                'description': 'Share purchase'
            }
        )

        # Create Contact Messages
        ContactMessage.objects.get_or_create(
            email='contact1@example.com',
            defaults={
                'name': 'Alice Johnson',
                'phone': '+1111222333',
                'subject': 'Membership Inquiry',
                'message': 'I would like to know more about joining Pamoja Kenya MN.',
                'status': 'new'
            }
        )

        ContactMessage.objects.get_or_create(
            email='contact2@example.com',
            defaults={
                'user': user1,
                'name': 'Bob Wilson',
                'phone': '+1444555666',
                'subject': 'Payment Issue',
                'message': 'I am having trouble with my payment processing.',
                'status': 'read'
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully created mock data'))