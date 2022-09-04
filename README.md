### Following requirements are added in this branch:
- **Added custom user model with fields**
    - email (required for both)
    - mobile (optional for admin)
    - first name (optional for admin)
    - last name (optional for admin)
    - country
    - mobile otp (optional for admin)
    - otp_generated_at
- **Added custom user admin**
- **Added user register serializer**
- **Added user register view**


## auth branch

- **Installed pyjwt**
- **Created token encoder property in models.py**
- **Created login serializer**
- **Created custom user backend**
- **Created login view**

### Functionality

- User can login with right credentials
- Return Invalid credentials if wrong mobile number or otp given
- Generated jwt token for logged in user