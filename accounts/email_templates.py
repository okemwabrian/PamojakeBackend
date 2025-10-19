from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import secrets
import string

def generate_random_password(length=12):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_activation_email(user):
    """Send email when user is activated"""
    subject = 'Account Activated - Pamoja Kenya MN'
    message = f"""
Dear {user.first_name or user.username},

Great news! Your account has been activated by the administrator.

You can now access all features of the Pamoja Kenya MN platform including:
- Submit membership applications
- Purchase shares
- Submit claims
- View announcements and events
- Participate in meetings

Login at: http://localhost:3000/login

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send activation email: {e}")
        return False

def send_deactivation_email(user, reason):
    """Send email when user is deactivated"""
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
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send deactivation email: {e}")
        return False

def send_password_reset_email(user):
    """Send new random password to user"""
    new_password = generate_random_password()
    user.set_password(new_password)
    user.save()
    
    subject = 'Password Reset - Pamoja Kenya MN'
    message = f"""
Dear {user.first_name or user.username},

Your password has been reset by the administrator.

New Password: {new_password}

Please login and change your password immediately for security.

Login at: http://localhost:3000/login

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True, new_password
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
        return False, None

def send_low_shares_warning(user):
    """Send email when user has low shares (below 25)"""
    subject = 'Low Shares Alert - Pamoja Kenya MN'
    message = f"""
Dear {user.first_name or user.username},

Your share balance is running low!

Current Shares: {user.shares_owned}
Available Shares: {user.available_shares}

When your shares fall below 25, you may not be eligible for certain benefits.
Please consider purchasing more shares to maintain your membership benefits.

To purchase shares:
1. Login to your account
2. Go to Shares section
3. Make a payment to increase your shares

Login at: http://localhost:3000/login

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send low shares warning: {e}")
        return False

def send_membership_status_email(user, status, application_type='single'):
    """Send email for membership application status"""
    status_text = {
        'approved': 'Approved',
        'rejected': 'Rejected',
        'pending': 'Under Review'
    }
    
    subject = f'Membership Application {status_text[status]} - Pamoja Kenya MN'
    
    if status == 'approved':
        message = f"""
Dear {user.first_name or user.username},

Congratulations! Your {application_type} membership application has been approved.

You are now a member of Pamoja Kenya MN and can access all member benefits including:
- Share purchases
- Benefit claims
- Community events and meetings
- Member support services

Welcome to the Pamoja Kenya MN family!

Login at: http://localhost:3000/login

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    elif status == 'rejected':
        message = f"""
Dear {user.first_name or user.username},

We regret to inform you that your {application_type} membership application has been rejected.

Please contact us at pamojakeny@gmail.com for more information or to discuss reapplication.

Best regards,
Pamoja Kenya MN Team
"""
    else:  # pending
        message = f"""
Dear {user.first_name or user.username},

Thank you for submitting your {application_type} membership application.

Your application is currently under review by our team. We will notify you once a decision has been made.

Expected processing time: 3-5 business days.

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send membership status email: {e}")
        return False

def send_claim_status_email(user, claim, status):
    """Send email for claim status updates"""
    status_text = {
        'approved': 'Approved',
        'rejected': 'Rejected',
        'pending': 'Under Review'
    }
    
    subject = f'Claim {status_text[status]} - Pamoja Kenya MN'
    
    if status == 'approved':
        message = f"""
Dear {user.first_name or user.username},

Your claim has been approved!

Claim Details:
- Type: {claim.claim_type}
- Amount Requested: ${claim.amount_requested}
- Amount Approved: ${getattr(claim, 'amount_approved', claim.amount_requested)}
- Date: {claim.created_at.strftime('%B %d, %Y')}

The approved amount will be processed and sent to you within 5-7 business days.

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    elif status == 'rejected':
        message = f"""
Dear {user.first_name or user.username},

We regret to inform you that your claim has been rejected.

Claim Details:
- Type: {claim.claim_type}
- Amount Requested: ${claim.amount_requested}
- Date: {claim.created_at.strftime('%B %d, %Y')}

For more information about this decision, please contact us at pamojakeny@gmail.com.

Best regards,
Pamoja Kenya MN Team
"""
    else:  # pending
        message = f"""
Dear {user.first_name or user.username},

Thank you for submitting your claim.

Claim Details:
- Type: {claim.claim_type}
- Amount Requested: ${claim.amount_requested}
- Date: {claim.created_at.strftime('%B %d, %Y')}

Your claim is currently under review. We will notify you once a decision has been made.

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send claim status email: {e}")
        return False

def send_announcement_email(users, announcement):
    """Send announcement to multiple users"""
    subject = f'New Announcement - {announcement.title}'
    message = f"""
Dear Pamoja Kenya MN Members,

{announcement.title}

{announcement.content}

Published: {announcement.created_at.strftime('%B %d, %Y')}

Login to view more details: http://localhost:3000/login

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    user_emails = [user.email for user in users if user.email]
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, user_emails)
        return True
    except Exception as e:
        print(f"Failed to send announcement email: {e}")
        return False

def send_meeting_notification(users, meeting):
    """Send meeting notification to users"""
    subject = f'Meeting Invitation - {meeting.title}'
    message = f"""
Dear Pamoja Kenya MN Members,

You are invited to attend our upcoming meeting:

Meeting: {meeting.title}
Date: {meeting.date.strftime('%B %d, %Y')}
Time: {meeting.date.strftime('%I:%M %p')}
Type: {meeting.type}
Meeting Link: {meeting.meeting_link or 'To be provided'}

Description:
{meeting.description}

Please join us for this important meeting.

Best regards,
Pamoja Kenya MN Team
pamojakeny@gmail.com
"""
    
    user_emails = [user.email for user in users if user.email]
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, user_emails)
        return True
    except Exception as e:
        print(f"Failed to send meeting notification: {e}")
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    subject = "Welcome to Pamoja Kenya MN!"
    
    message = f"""
Dear {user.first_name or user.username},

Welcome to Pamoja Kenya MN! We're excited to have you join our community.

Your account has been successfully created with the following details:
- Username: {user.username}
- Email: {user.email}
- Registration Date: {user.date_joined.strftime('%B %d, %Y')}

Next Steps:
1. Login to your account at our website
2. Complete your profile information
3. Apply for membership to access all benefits
4. Purchase shares to strengthen our community

If you have any questions, please don't hesitate to contact us.

Welcome aboard!

Best regards,
Pamoja Kenya MN Team
Email: pamojakeny@gmail.com
Phone: (612) 261-5786
"""
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}: {e}")
        return False

def send_registration_pending_email(user):
    """Send email to user after registration - waiting for activation"""
    subject = "Registration Successful - Awaiting Activation"
    
    message = f"""
Dear {user.first_name or user.username},

Thank you for registering with Pamoja Kenya MN!

Your account has been created successfully but requires admin activation before you can access all features.

Account Details:
- Username: {user.username}
- Email: {user.email}
- Registration Date: {user.date_joined.strftime('%B %d, %Y')}

Next Steps:
1. Wait for admin activation (usually within 24-48 hours)
2. You will receive an activation email once approved
3. After activation, you can login and access all features

If you have any questions, please contact us at pamojakeny@gmail.com

Thank you for your patience!

Best regards,
Pamoja Kenya MN Team
Email: pamojakeny@gmail.com
Phone: (612) 261-5786
"""
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send registration pending email to {user.email}: {e}")
        return False

def send_shares_deduction_notification(users, amount, reason):
    """Send email to all members about shares deduction"""
    subject = "Community Support - Shares Deduction Notice"
    
    message = f"""
Dear Pamoja Kenya MN Members,

We hope this message finds you well.

Due to a community emergency, we have deducted {amount} shares from all member accounts to provide support during this difficult time.

Reason: {reason}
Amount Deducted: {amount} shares per member
Date: {timezone.now().strftime('%B %d, %Y')}

This deduction helps us fulfill our commitment to support our community members in times of need. Your contribution makes a difference in someone's life.

You can view your updated share balance by logging into your account.

Thank you for your understanding and continued support.

Best regards,
Pamoja Kenya MN Team
Email: pamojakeny@gmail.com
Phone: (612) 261-5786
"""
    
    user_emails = [user.email for user in users if user.email]
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            user_emails,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send shares deduction notification: {e}")
        return False

def send_auto_deactivation_email(user):
    """Send email when user is auto-deactivated due to low shares"""
    subject = "Account Deactivated - Low Shares Balance"
    
    message = f"""
Dear {user.first_name or user.username},

Your account has been automatically deactivated due to insufficient shares balance.

Current Shares: {user.shares_owned}
Minimum Required: 20 shares

To reactivate your account:
1. Purchase additional shares to bring your balance above 20
2. Contact admin for account reactivation
3. Make payment and provide evidence

Your account will remain deactivated until your shares balance is restored.

To purchase shares or get help, contact us at pamojakeny@gmail.com

Best regards,
Pamoja Kenya MN Team
Email: pamojakeny@gmail.com
Phone: (612) 261-5786
"""
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send auto deactivation email to {user.email}: {e}")
        return False

def send_payment_notification_to_admin(user, payment_type, amount, evidence_file=None):
    """Send payment notification to admin"""
    subject = f"Payment Notification - {user.username}"
    
    message = f"""
New payment notification from user:

User: {user.first_name} {user.last_name} ({user.username})
Email: {user.email}
Payment Type: {payment_type}
Amount: ${amount}
Date: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}

{f'Evidence file attached: {evidence_file}' if evidence_file else 'No evidence file provided'}

Please review and update the user's account accordingly.

Admin Panel: http://localhost:3000/admin-dashboard

Pamoja Kenya MN System
"""
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['pamojakeny@gmail.com'],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send payment notification to admin: {e}")
        return False

def send_payment_approval_email(payment):
    """Send payment approval email to user"""
    user = payment.user
    
    if payment.type == 'activation_fee':
        subject = "Membership Activated - Welcome to Pamoja Kenya MN!"
        message = f"""
Dear {user.first_name or user.username},

Great news! Your activation fee payment of ${payment.amount} has been approved and your membership is now active!

Membership Details:
- Status: Active Member
- Activation Date: {payment.updated_at.strftime('%B %d, %Y')}
- Payment Method: {payment.payment_method}
- Transaction ID: {payment.transaction_id or 'N/A'}

You can now:
✓ Purchase shares
✓ Submit benefit claims
✓ Participate in community meetings
✓ Access all member services

Login to your account: http://localhost:3000/login

Welcome to the Pamoja Kenya MN family!

Best regards,
Pamoja Kenya MN Team
"""
    elif payment.type == 'share_purchase':
        subject = "Share Purchase Approved - Pamoja Kenya MN"
        message = f"""
Dear {user.first_name or user.username},

Your share purchase has been approved!

Purchase Details:
- Amount Paid: ${payment.amount}
- Shares Assigned: {payment.shares_assigned}
- Current Total Shares: {user.shares_owned}
- Available Shares: {user.available_shares}
- Share Value: $100 per share

Your shares are now active and you can use them for:
- Emergency claims
- Community support
- Voting rights in meetings

Thank you for strengthening our community!

Best regards,
Pamoja Kenya MN Team
"""
    else:
        subject = f"Payment Approved - {payment.get_type_display()}"
        message = f"""
Dear {user.first_name or user.username},

Your payment has been approved!

Payment Details:
- Type: {payment.get_type_display()}
- Amount: ${payment.amount}
- Status: Approved
- Date: {payment.updated_at.strftime('%B %d, %Y')}

{payment.admin_notes if payment.admin_notes else ''}

Thank you for your payment.

Best regards,
Pamoja Kenya MN Team
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send payment approval email: {e}")
        return False

def send_payment_rejection_email(payment):
    """Send payment rejection email to user"""
    user = payment.user
    subject = f"Payment Rejected - {payment.get_type_display()}"
    
    message = f"""
Dear {user.first_name or user.username},

We regret to inform you that your payment has been rejected.

Payment Details:
- Type: {payment.get_type_display()}
- Amount: ${payment.amount}
- Submitted: {payment.created_at.strftime('%B %d, %Y')}
- Rejected: {payment.updated_at.strftime('%B %d, %Y')}

Reason for rejection:
{payment.admin_notes or 'Please contact admin for more details.'}

Next Steps:
1. Review the rejection reason above
2. Correct any issues with your payment
3. Resubmit your payment if needed
4. Contact us if you have questions

Contact Information:
Email: pamojakeny@gmail.com
Phone: (612) 261-5786

Best regards,
Pamoja Kenya MN Team
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send payment rejection email: {e}")
        return False

def send_share_deduction_email(user, shares_deducted, remaining_shares, reason):
    """Send email notification for share deduction"""
    subject = "Share Deduction Notification - Pamoja Kenya MN"
    
    message = f"""
Dear {user.first_name or user.username},

This is to notify you that shares have been deducted from your account for community support.

Deduction Details:
- Shares Deducted: {shares_deducted}
- Remaining Shares: {remaining_shares}
- Available Shares: {user.available_shares}
- Current Share Value: ${remaining_shares * 100}
- Reason: {reason}
- Date: {timezone.now().strftime('%B %d, %Y')}

This deduction helps us support community members in need. Your contribution makes a difference.

{f'Warning: Your share balance is low ({remaining_shares}). Consider purchasing more shares to maintain full benefits.' if remaining_shares < 25 else ''}

Thank you for your continued support of our community.

Best regards,
Pamoja Kenya MN Team
Email: pamojakeny@gmail.com
Phone: (612) 261-5786
"""
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return True
    except Exception as e:
        print(f"Failed to send share deduction email: {e}")
        return False