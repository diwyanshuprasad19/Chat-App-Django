from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CustomUser
from .services import CognitoService

@receiver(post_save, sender=CustomUser)
def sync_cognito_user(sender, instance, created, **kwargs):
    if created:
        # Create user in Cognito
        CognitoService.create_or_update_cognito_user(
            phone=instance.phone,
            username=instance.username,
            phone_verified=instance.phone_verified,
            is_active=instance.is_active,
            is_staff=instance.is_staff,
            is_superuser=instance.is_superuser,
            password='TemporaryPassword123!'  # Provide a default password
        )
    else:
        # Update user in Cognito
        CognitoService.create_or_update_cognito_user(
            user_id=instance.username,
            phone=instance.phone,
            phone_verified=instance.phone_verified,
            is_active=instance.is_active,
            is_staff=instance.is_staff,
            is_superuser=instance.is_superuser
        )

@receiver(pre_delete, sender=CustomUser)
def soft_delete_user(sender, instance, **kwargs):
    if not instance.is_active:
        # Set is_active to False instead of actual delete
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        CognitoService.create_or_update_cognito_user(
            user_id=instance.username,
            phone=instance.phone,
            phone_verified=instance.phone_verified,
            is_active=instance.is_active,
            is_staff=instance.is_staff,
            is_superuser=instance.is_superuser
        )
