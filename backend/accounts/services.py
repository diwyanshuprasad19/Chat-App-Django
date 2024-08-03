import boto3
from django.conf import settings


class CognitoService:
    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=settings.AWS_REGION)

    def register_user(self, phone, username, password):
        response = self.client.sign_up(
            ClientId=settings.COGNITO_USER_POOL_CLIENT_ID,
            Username=phone,
            Password=password,
            UserAttributes=[
                {'Name': 'phone_number', 'Value': phone},
                {'Name': 'preferred_username', 'Value': username}
            ]
        )
        return response

    def login_user(self, phone, password):
        response = self.client.initiate_auth(
            ClientId=settings.COGNITO_USER_POOL_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': phone,
                'PASSWORD': password
            }
        )
        return response

    def logout_user(self, access_token):
        try:
            self.client.global_sign_out(
                AccessToken=access_token
            )
        except Exception as e:
            raise Exception(f"Error logging out user from Cognito: {str(e)}")

    def delete_user(self, phone):
        try:
            self.client.admin_delete_user(
                UserPoolId=settings.AWS_USER_POOL_ID,
                Username=phone
            )
        except Exception as e:
            raise Exception(f"Error deleting user from Cognito: {str(e)}")

    def create_or_update_user(self, phone, username, phone_verified, is_active, is_staff, is_superuser, password=None):
        try:
            response = self.client.admin_get_user(
                UserPoolId=settings.AWS_USER_POOL_ID,
                Username=phone
            )
            # Update user if exists
            self.client.admin_update_user_attributes(
                UserPoolId=settings.AWS_USER_POOL_ID,
                Username=phone,
                UserAttributes=[
                    {'Name': 'phone_number', 'Value': phone},
                    {'Name': 'preferred_username', 'Value': username},
                    {'Name': 'phone_verified', 'Value': str(phone_verified).lower()},
                    {'Name': 'is_active', 'Value': str(is_active).lower()},
                    {'Name': 'is_staff', 'Value': str(is_staff).lower()},
                    {'Name': 'is_superuser', 'Value': str(is_superuser).lower()}
                ]
            )
        except self.client.exceptions.UserNotFoundException:
            # Create new user if not found
            self.register_user(phone, username, password)
            self.client.admin_update_user_attributes(
                UserPoolId=settings.AWS_USER_POOL_ID,
                Username=phone,
                UserAttributes=[
                    {'Name': 'phone_verified', 'Value': str(phone_verified).lower()},
                    {'Name': 'is_active', 'Value': str(is_active).lower()},
                    {'Name': 'is_staff', 'Value': str(is_staff).lower()},
                    {'Name': 'is_superuser', 'Value': str(is_superuser).lower()}
                ]
            )
