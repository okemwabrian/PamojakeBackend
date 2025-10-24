# Run this command to create the migration:
# python manage.py makemigrations applications --name add_new_application_models

# Then add these models to your applications/models.py file:

"""
Add these imports to the top of applications/models.py:
from django.contrib.auth.models import User

Then add these models to applications/models.py:
"""

NEW_MODELS_CODE = '''
class SingleApplication(models.Model):
    # Personal Information
    firstName = models.CharField(max_length=100)
    middleName = models.CharField(max_length=100, blank=True)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    phoneMain = models.CharField(max_length=20)
    
    # Address Information
    address1 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    stateProvince = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    
    # Family Information
    spouse = models.CharField(max_length=100, blank=True)
    spousePhone = models.CharField(max_length=20, blank=True)
    spouseCellPhone = models.CharField(max_length=20, blank=True)
    authorizedRep = models.CharField(max_length=100, blank=True)
    
    # Children
    child1 = models.CharField(max_length=100, blank=True)
    child2 = models.CharField(max_length=100, blank=True)
    child3 = models.CharField(max_length=100, blank=True)
    child4 = models.CharField(max_length=100, blank=True)
    child5 = models.CharField(max_length=100, blank=True)
    
    # Parents
    parent1 = models.CharField(max_length=100, blank=True)
    parent2 = models.CharField(max_length=100, blank=True)
    spouseParent1 = models.CharField(max_length=100, blank=True)
    spouseParent2 = models.CharField(max_length=100, blank=True)
    
    # Siblings
    sibling1 = models.CharField(max_length=100, blank=True)
    sibling2 = models.CharField(max_length=100, blank=True)
    
    # Documents
    id_document = models.FileField(upload_to='applications/single/')
    declarationAccepted = models.BooleanField(default=False)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications_singleapplication'
    
    def __str__(self):
        return f"{self.firstName} {self.lastName} - Single Application"

class DoubleApplication(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    confirm_email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Address Information
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    zip_postal = models.CharField(max_length=20)
    
    # Family Information
    spouse_name = models.CharField(max_length=100, blank=True)
    spouse_phone = models.CharField(max_length=20, blank=True)
    authorized_rep = models.CharField(max_length=100, blank=True)
    
    # Children
    child_1 = models.CharField(max_length=100, blank=True)
    child_2 = models.CharField(max_length=100, blank=True)
    child_3 = models.CharField(max_length=100, blank=True)
    child_4 = models.CharField(max_length=100, blank=True)
    child_5 = models.CharField(max_length=100, blank=True)
    
    # Parents
    parent_1 = models.CharField(max_length=100, blank=True)
    parent_2 = models.CharField(max_length=100, blank=True)
    spouse_parent_1 = models.CharField(max_length=100, blank=True)
    spouse_parent_2 = models.CharField(max_length=100, blank=True)
    
    # Step Parents
    step_parent_1 = models.CharField(max_length=100, blank=True)
    step_parent_2 = models.CharField(max_length=100, blank=True)
    
    # Siblings
    sibling_1 = models.CharField(max_length=100, blank=True)
    sibling_2 = models.CharField(max_length=100, blank=True)
    sibling_3 = models.CharField(max_length=100, blank=True)
    
    # Step Siblings
    step_sibling_1 = models.CharField(max_length=100, blank=True)
    step_sibling_2 = models.CharField(max_length=100, blank=True)
    step_sibling_3 = models.CharField(max_length=100, blank=True)
    
    # Documents
    id_document = models.FileField(upload_to='applications/double/')
    constitution_agreed = models.BooleanField(default=False)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications_doubleapplication'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - Double Application"
'''

print("To integrate these models:")
print("1. Copy the models from new_application_models.py to applications/models.py")
print("2. Copy the serializers from new_application_serializers.py to applications/serializers.py")
print("3. Copy the views from new_application_views.py to applications/views.py")
print("4. Update applications/urls.py with the new URL patterns")
print("5. Run: python manage.py makemigrations applications")
print("6. Run: python manage.py migrate")
print("7. Push to GitHub and pull on PythonAnywhere")