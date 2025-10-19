from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def send_activation_notification(user):
    """Send activation notification to admin and pamojakeny@gmail.com"""
    subject = f'User Activation Required: {user.first_name} {user.last_name}'
    message = f"""
    A new user requires activation:
    
    Name: {user.first_name} {user.last_name}
    Email: {user.email}
    Username: {user.username}
    Registration Date: {user.date_joined}
    
    Please review and activate this user in the admin panel.
    """
    
    recipients = ['pamojakeny@gmail.com']
    if hasattr(settings, 'ADMIN_EMAIL'):
        recipients.append(settings.ADMIN_EMAIL)
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send activation notification: {e}")

def send_meeting_registration_confirmation(user, meeting):
    """Send meeting registration confirmation to user"""
    subject = f'Meeting Registration Confirmed: {meeting.title}'
    message = f"""
    Dear {user.first_name},
    
    Your registration for the following meeting has been confirmed:
    
    Meeting: {meeting.title}
    Date: {meeting.date}
    Duration: {meeting.duration_minutes} minutes
    Type: {meeting.get_type_display()}
    
    {f'Meeting Link: {meeting.meeting_link}' if meeting.meeting_link else ''}
    
    Thank you for registering!
    
    Best regards,
    Pamoja Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send meeting confirmation: {e}")

def send_payment_approval_notification(user, payment):
    """Send payment approval notification to user"""
    subject = f'Payment Approved: {payment.get_type_display()}'
    message = f"""
    Dear {user.first_name},
    
    Your payment has been approved:
    
    Type: {payment.get_type_display()}
    Amount: ${payment.amount}
    Transaction ID: {payment.transaction_id}
    
    Thank you for your payment!
    
    Best regards,
    Pamoja Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send payment approval notification: {e}")

def send_payment_rejection_notification(user, payment):
    """Send payment rejection notification to user"""
    subject = f'Payment Rejected: {payment.get_payment_type_display()}'
    message = f"""
    Dear {user.first_name},
    
    Your payment has been rejected:
    
    Type: {payment.get_payment_type_display()}
    Amount: ${payment.amount}
    Reference: {payment.reference_number}
    Reason: {payment.admin_notes}
    
    Please contact support for assistance.
    
    Best regards,
    Pamoja Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send payment rejection notification: {e}")

def send_activation_fee_notification(payment):
    """Send activation fee notification to admin"""
    subject = f'Activation Fee Payment - {payment.user.username}'
    message = f"""
    New activation fee payment received:
    
    User: {payment.user.get_full_name()}
    Amount: ${payment.amount}
    Date: {payment.created_at}
    
    Please review and activate the account.
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['pamojakeny@gmail.com'],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send activation fee notification: {e}")

def send_claim_notification(claim):
    """Send claim notification to admin"""
    subject = f'New Claim Submitted - {claim.user.username}'
    message = f"""
    New claim submitted:
    
    User: {claim.user.get_full_name()}
    Type: {claim.claim_type}
    Amount: ${claim.amount}
    Description: {claim.description}
    
    Please review in admin panel.
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['pamojakeny@gmail.com'],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send claim notification: {e}")