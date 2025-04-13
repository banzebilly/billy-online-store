from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom user manager to handle user and superuser creation logic
class MyAccountManager(BaseUserManager):

    # Method to create a regular user
    def create_user(self, first_name, last_name, email, username, password=None):
        # Ensure email and username are provided
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        # Create a new user instance with normalized email
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        # Set the user's password securely
        user.set_password(password)
        # Save the user to the database
        user.save(using=self._db)
        return user

    # Method to create a superuser (admin account)
    def create_superuser(self, first_name, last_name, email, username, password):
        # Create a base user first
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Grant all admin permissions
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

# Custom user model extending Django's AbstractBaseUser
class Account(AbstractBaseUser):
    # Basic user information
    first_name      = models.CharField(max_length=50)  # User's first name
    last_name       = models.CharField(max_length=50)  # User's last name
    username        = models.CharField(max_length=50, unique=True)  # Unique username
    email           = models.EmailField(max_length=100, unique=True)  # Unique email used for login
    phone_number    = models.CharField(max_length=50)  # Optional phone number field

    # System-level fields for user status and tracking
    date_joined     = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created
    last_login      = models.DateTimeField(auto_now_add=True)  # Timestamp of the user's last login
    is_staff        = models.BooleanField(default=False)  # Can access Django admin site
    is_admin        = models.BooleanField(default=False)  # Has admin privileges
    is_active       = models.BooleanField(default=False)  # Can login if active
    is_superadmin   = models.BooleanField(default=False)  # Has full system access

    # Set the email as the unique identifier for authentication instead of username
    USERNAME_FIELD  = 'email'
    # Required fields when creating a user via createsuperuser
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Assign custom user manager
    objects = MyAccountManager()

    # String representation of the user
    def __str__(self):
        return self.email

    # Returns the full name of the user
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Determines if the user has a specific permission (required by Django)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Determines if the user has permissions to access a specific app
    def has_module_perms(self, add_label):
        return True


# =========================== User profile model starts here ===========================

# A separate profile model linked one-to-one with the custom user model
class UserProfile(models.Model):
    # Link profile to user account
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    # Optional address fields
    address_line_1 = models.CharField(blank=True, max_length=100)  # Street address line 1
    address_line_2 = models.CharField(blank=True, max_length=100)  # Street address line 2
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')  # Optional profile image
    city = models.CharField(blank=True, max_length=20)  # City name
    state = models.CharField(blank=True, max_length=20)  # State name
    country = models.CharField(blank=True, max_length=20)  # Country name

    # String representation of the profile (display user's first name)
    def __str__(self):
        return self.user.first_name

    # Returns a formatted full address
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
