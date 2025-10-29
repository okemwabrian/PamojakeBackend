from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import models
from applications.models import Application
from claims.models import Claim
from payments.models import Payment
from shares.models import ShareTransaction
from .models import UserActivity
from applications.models import Application

User = get_user_model()

# ===== APPLICATIONS CRUD =====
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_applications(request):
    if request.method == 'GET':
        applications = Application.objects.all().order_by('-created_at')
        data = [{
            'id': app.id,
            'user': app.user.username,
            'full_name': f"{app.first_name} {app.last_name}",
            'membership_type': app.membership_type or app.type,
            'status': app.status,
            'email': app.email,
            'phone': app.phone or app.phone_main,
            'created_at': app.created_at.isoformat(),
            'admin_notes': app.admin_notes,
        } for app in applications]
        return Response({'applications': data})
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=request.data.get('user_id'))
            application = Application.objects.create(
                user=user,
                membership_type=request.data.get('membership_type'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                email=request.data.get('email'),
                phone=request.data.get('phone'),
                address=request.data.get('address', ''),
                city=request.data.get('city', ''),
                state=request.data.get('state', 'Minnesota'),
                zip_code=request.data.get('zip_code', ''),
                admin_notes=request.data.get('admin_notes', ''),
            )
            
            UserActivity.objects.create(
                user=user,
                activity_type='application_submitted',
                description=f'Admin created {application.membership_type} application for user'
            )
            
            return Response({'success': True, 'application_id': application.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_application_detail(request, app_id):
    try:
        application = Application.objects.get(id=app_id)
    except Application.DoesNotExist:
        return Response({'error': 'Application not found'}, status=404)
    
    if request.method == 'GET':
        # Return COMPLETE application data as submitted by user
        application_data = {
            # Application Info
            'id': application.id,
            'user': application.user.username,
            'user_id': application.user.id,
            'membership_type': application.membership_type or application.type,
            'status': application.status,
            'created_at': application.created_at.isoformat(),
            'updated_at': application.updated_at.isoformat(),
            'admin_notes': application.admin_notes,
            
            # Primary Applicant (from form fields)
            'first_name': application.first_name,
            'middle_name': application.middle_name,
            'last_name': application.last_name,
            'full_name': f"{application.first_name} {application.last_name}",
            'email': application.email,
            'confirm_email': application.confirm_email,
            'phone': application.phone,
            'phone_main': application.phone_main,
            'date_of_birth': application.date_of_birth.isoformat() if application.date_of_birth else None,
            'id_number': application.id_number,
            
            # Address (from form fields)
            'address': application.address,
            'address_1': application.address_1,
            'address_2': application.address_2,
            'city': application.city,
            'state': application.state,
            'state_province': application.state_province,
            'zip_code': application.zip_code,
            'zip_postal': application.zip_postal,
            
            # Emergency Contact (from form fields)
            'emergency_name': application.emergency_name,
            'emergency_phone': application.emergency_phone,
            'emergency_relationship': application.emergency_relationship,
            
            # Spouse Information (for double membership)
            'spouse_first_name': application.spouse_first_name,
            'spouse_last_name': application.spouse_last_name,
            'spouse_email': application.spouse_email,
            'spouse_phone': application.spouse_phone,
            'spouse_date_of_birth': application.spouse_date_of_birth.isoformat() if application.spouse_date_of_birth else None,
            'spouse_id_number': application.spouse_id_number,
            'spouse': application.spouse,
            'authorized_rep': application.authorized_rep,
            
            # Children Information (JSON field + legacy fields)
            'children_info': application.children_info if application.children_info else [],
            'child_1': application.child_1,
            'child_2': application.child_2,
            'child_3': application.child_3,
            'child_4': application.child_4,
            'child_5': application.child_5,
            
            # Parents Information
            'parent_1': application.parent_1,
            'parent_2': application.parent_2,
            'spouse_parent_1': application.spouse_parent_1,
            'spouse_parent_2': application.spouse_parent_2,
            
            # Siblings Information
            'sibling_1': application.sibling_1,
            'sibling_2': application.sibling_2,
            'sibling_3': application.sibling_3,
            
            # Agreements
            'declaration_accepted': application.declaration_accepted,
            'constitution_agreed': application.constitution_agreed,
            
            # Documents
            'id_document': application.id_document.url if application.id_document else None,
            'spouse_id_document': application.spouse_id_document.url if application.spouse_id_document else None,
            'payment_proof': application.payment_proof.url if application.payment_proof else None,
            
            # Payment Info
            'payment_amount': str(application.payment_amount),
            'activation_fee_paid': application.activation_fee_paid,
            'activation_fee_amount': str(application.activation_fee_amount),
            'payment_reference': application.payment_reference,
            'payment_verified': application.payment_verified,
        }
        
        return Response({'application': application_data})
    
    elif request.method == 'PUT':
        for field, value in request.data.items():
            if hasattr(application, field):
                setattr(application, field, value)
        application.save()
        
        UserActivity.objects.create(
            user=application.user,
            activity_type='application_updated',
            description=f'Admin updated application #{application.id}'
        )
        
        return Response({'success': True, 'message': 'Application updated successfully'})
    
    elif request.method == 'DELETE':
        user = application.user
        application.delete()
        
        UserActivity.objects.create(
            user=user,
            activity_type='application_deleted',
            description=f'Admin deleted application #{app_id}'
        )
        
        return Response({'success': True, 'message': 'Application deleted successfully'})

# ===== PAYMENTS CRUD =====
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_payments(request):
    if request.method == 'GET':
        payments = Payment.objects.all().order_by('-created_at')
        data = [{
            'id': payment.id,
            'user': payment.user.username,
            'payment_type': payment.payment_type,
            'amount': str(payment.amount),
            'payment_method': payment.payment_method,
            'status': payment.status,
            'created_at': payment.created_at.isoformat(),
            'admin_notes': payment.admin_notes,
        } for payment in payments]
        return Response({'payments': data})
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=request.data.get('user_id'))
            payment = Payment.objects.create(
                user=user,
                payment_type=request.data.get('payment_type'),
                amount=request.data.get('amount'),
                payment_method=request.data.get('payment_method'),
                status=request.data.get('status', 'pending'),
                admin_notes=request.data.get('admin_notes', ''),
            )
            
            UserActivity.objects.create(
                user=user,
                activity_type='payment_made',
                description=f'Admin created payment of ${payment.amount} for user'
            )
            
            return Response({'success': True, 'payment_id': payment.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_payment_detail(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)
    
    if request.method == 'GET':
        return Response({
            'payment': {
                'id': payment.id,
                'user': payment.user.username,
                'payment_type': payment.payment_type,
                'amount': str(payment.amount),
                'payment_method': payment.payment_method,
                'status': payment.status,
                'created_at': payment.created_at.isoformat(),
                'admin_notes': payment.admin_notes,
            }
        })
    
    elif request.method == 'PUT':
        old_status = payment.status
        for field, value in request.data.items():
            if hasattr(payment, field):
                setattr(payment, field, value)
        payment.save()
        
        if old_status != payment.status:
            UserActivity.objects.create(
                user=payment.user,
                activity_type='payment_updated',
                description=f'Admin changed payment #{payment.id} status from {old_status} to {payment.status}'
            )
        
        return Response({'success': True})
    
    elif request.method == 'DELETE':
        user = payment.user
        payment.delete()
        
        UserActivity.objects.create(
            user=user,
            activity_type='payment_deleted',
            description=f'Admin deleted payment #{payment_id}'
        )
        
        return Response({'success': True})

# ===== CLAIMS CRUD =====
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_claims(request):
    if request.method == 'GET':
        claims = Claim.objects.all().order_by('-created_at')
        data = [{
            'id': claim.id,
            'user': claim.user.username,
            'claim_type': claim.claim_type,
            'member_name': claim.member_name,
            'amount_requested': str(claim.amount_requested),
            'amount_approved': str(claim.amount_approved) if claim.amount_approved else None,
            'status': claim.status,
            'created_at': claim.created_at.isoformat(),
            'admin_notes': claim.admin_notes,
        } for claim in claims]
        return Response({'claims': data})
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=request.data.get('user_id'))
            claim = Claim.objects.create(
                user=user,
                claim_type=request.data.get('claim_type'),
                member_name=request.data.get('member_name'),
                relationship=request.data.get('relationship'),
                amount_requested=request.data.get('amount_requested'),
                incident_date=request.data.get('incident_date'),
                description=request.data.get('description'),
                status=request.data.get('status', 'pending'),
                admin_notes=request.data.get('admin_notes', ''),
            )
            
            UserActivity.objects.create(
                user=user,
                activity_type='claim_submitted',
                description=f'Admin created claim "{claim.claim_type}" for user'
            )
            
            return Response({'success': True, 'claim_id': claim.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_claim_detail(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=404)
    
    if request.method == 'GET':
        return Response({
            'claim': {
                'id': claim.id,
                'user': claim.user.username,
                'claim_type': claim.claim_type,
                'member_name': claim.member_name,
                'relationship': claim.relationship,
                'amount_requested': str(claim.amount_requested),
                'amount_approved': str(claim.amount_approved) if claim.amount_approved else None,
                'incident_date': claim.incident_date.isoformat(),
                'description': claim.description,
                'status': claim.status,
                'created_at': claim.created_at.isoformat(),
                'admin_notes': claim.admin_notes,
            }
        })
    
    elif request.method == 'PUT':
        old_status = claim.status
        for field, value in request.data.items():
            if hasattr(claim, field):
                setattr(claim, field, value)
        claim.save()
        
        if old_status != claim.status:
            UserActivity.objects.create(
                user=claim.user,
                activity_type='claim_updated',
                description=f'Admin changed claim #{claim.id} status from {old_status} to {claim.status}'
            )
        
        return Response({'success': True})
    
    elif request.method == 'DELETE':
        user = claim.user
        claim.delete()
        
        UserActivity.objects.create(
            user=user,
            activity_type='claim_deleted',
            description=f'Admin deleted claim #{claim_id}'
        )
        
        return Response({'success': True})

# ===== SHARES CRUD =====
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_shares(request):
    if request.method == 'GET':
        shares = ShareTransaction.objects.all().order_by('-created_at')
        data = [{
            'id': share.id,
            'user': share.user.username,
            'buyer_name': share.buyer_name,
            'quantity': share.quantity,
            'total_amount': str(share.total_amount),
            'payment_method': share.payment_method,
            'status': share.status,
            'created_at': share.created_at.isoformat(),
            'notes': share.notes,
        } for share in shares]
        return Response({'shares': data})
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=request.data.get('user_id'))
            share = ShareTransaction.objects.create(
                user=user,
                buyer_name=request.data.get('buyer_name'),
                quantity=request.data.get('quantity'),
                total_amount=request.data.get('total_amount'),
                payment_method=request.data.get('payment_method'),
                status=request.data.get('status', 'pending'),
                notes=request.data.get('notes', ''),
            )
            
            UserActivity.objects.create(
                user=user,
                activity_type='shares_purchased',
                description=f'Admin created share purchase of {share.quantity} shares for user'
            )
            
            return Response({'success': True, 'share_id': share.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_share_detail(request, share_id):
    try:
        share = ShareTransaction.objects.get(id=share_id)
    except ShareTransaction.DoesNotExist:
        return Response({'error': 'Share transaction not found'}, status=404)
    
    if request.method == 'GET':
        return Response({
            'share': {
                'id': share.id,
                'user': share.user.username,
                'buyer_name': share.buyer_name,
                'quantity': share.quantity,
                'total_amount': str(share.total_amount),
                'payment_method': share.payment_method,
                'status': share.status,
                'created_at': share.created_at.isoformat(),
                'notes': share.notes,
            }
        })
    
    elif request.method == 'PUT':
        for field, value in request.data.items():
            if hasattr(share, field):
                setattr(share, field, value)
        share.save()
        
        return Response({'success': True})
    
    elif request.method == 'DELETE':
        user = share.user
        share.delete()
        
        UserActivity.objects.create(
            user=user,
            activity_type='shares_deleted',
            description=f'Admin deleted share transaction #{share_id}'
        )
        
        return Response({'success': True})

# ===== USER ACTIVITIES =====
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_user_activities(request):
    activities = UserActivity.objects.all().order_by('-created_at')[:100]
    
    data = [{
        'id': activity.id,
        'user': activity.user.username,
        'activity_type': activity.activity_type,
        'description': activity.description,
        'ip_address': activity.ip_address,
        'created_at': activity.created_at.isoformat(),
    } for activity in activities]
    
    return Response({'activities': data})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_user_activity_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        activities = UserActivity.objects.filter(user=user).order_by('-created_at')
        
        data = [{
            'id': activity.id,
            'activity_type': activity.activity_type,
            'description': activity.description,
            'ip_address': activity.ip_address,
            'created_at': activity.created_at.isoformat(),
        } for activity in activities]
        
        return Response({
            'user': user.username,
            'activities': data
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

# ===== DASHBOARD STATS =====
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_stats(request):
    """Get comprehensive admin dashboard statistics"""
    
    # Get counts
    total_users = User.objects.count()
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status='pending').count()
    total_payments = Payment.objects.count()
    pending_payments = Payment.objects.filter(status='pending').count()
    total_claims = Claim.objects.count()
    pending_claims = Claim.objects.filter(status='pending').count()
    total_shares = ShareTransaction.objects.count()
    
    # Get recent activities
    recent_activities = UserActivity.objects.all().order_by('-created_at')[:10]
    
    # Get financial stats
    total_revenue = Payment.objects.filter(status__in=['approved', 'completed']).aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    return Response({
        'stats': {
            'users': {
                'total': total_users,
                'active': User.objects.filter(is_active=True).count(),
            },
            'applications': {
                'total': total_applications,
                'pending': pending_applications,
                'approved': Application.objects.filter(status='approved').count(),
            },
            'payments': {
                'total': total_payments,
                'pending': pending_payments,
                'total_revenue': str(total_revenue),
            },
            'claims': {
                'total': total_claims,
                'pending': pending_claims,
            },
            'shares': {
                'total': total_shares,
                'pending': ShareTransaction.objects.filter(status='pending').count(),
            }
        },
        'recent_activities': [{
            'id': activity.id,
            'user': activity.user.username,
            'activity_type': activity.activity_type,
            'description': activity.description,
            'created_at': activity.created_at.isoformat(),
        } for activity in recent_activities]
    })