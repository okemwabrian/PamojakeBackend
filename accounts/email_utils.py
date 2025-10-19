from django.core.mail import send_mail
from django.conf import settings

def send_deactivation_email(user, reason):
    """Send email notification when user is deactivated"""
    subject = 'Account Deactivation - Pamoja Kenya MN'
    message = f"""
Dear {user.first_name or user.username},

Your account has been deactivated by the administrator.

Reason: {reason}

If you believe this is an error or would like to appeal this decision, 
please contact us at pamojakeny@gmail.com.

Best regards,
Pamoja Kenya MN Team
"""
    
    try:
        send_mail(
            subject,
            message,
            'pamojakeny@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_activation_email(user):
    """Send email notification when user is activated"""
    subject = 'Account Activated - Pamoja Kenya MN'
    message = f"""
Dear {user.first_name or user.username},

Great news! Your account has been activated by the administrator.

You can now access all features of the Pamoja Kenya MN platform.

Login at: http://localhost:3000/login

Best regards,
Pamoja Kenya MN Team
"""
    
    try:
        send_mail(
            subject,
            message,
            'pamojakeny@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False