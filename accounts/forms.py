# Import required modules
from typing import Any
from django import forms
from .models import Account, UserProfile

# ========================== Registration Form ==========================

class RegistrationForm(forms.ModelForm):
    # Password field with masked input
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    
    # Confirm password field with masked input
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))

    class Meta:
        # Link the form to the custom Account model
        model = Account
        # Fields to include in the form
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        # Initialize the form and customize field attributes
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Set placeholder text for input fields
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'

        # Apply consistent styling to all fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # Custom validation method to ensure password and confirm_password match
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Raise a validation error if the passwords do not match
        if password != confirm_password:
            raise forms.ValidationError('Password does not match!')


# ========================== User & UserProfile Forms ==========================

# Form to update user basic info (first name, last name, phone number)
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        # Initialize the form and apply consistent styling
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# Form to update additional profile information
class UserProfileForm(forms.ModelForm):
    # Profile picture field allowing file uploads, not required
    profile_picture = forms.ImageField(
        required=False,
        error_messages={'invalid': ("Image files only")},
        widget=forms.FileInput
    )

    class Meta:
        model = UserProfile
        fields = (
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'profile_picture',
        )

    def __init__(self, *args, **kwargs):
        # Initialize the form and apply Bootstrap class to all fields
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
