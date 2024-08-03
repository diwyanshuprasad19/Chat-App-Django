from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    """

    def _create_user(self, phone, username, password, **extra_fields):
        """
        Creates and saves a User with the given phone number, username, and password.
        """
        if not phone:
            raise ValueError('The Phone field must be set')
        
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, username, password=None, **extra_fields):
        """
        Creates a regular user with the given phone number, username, and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone, username, password, **extra_fields)

    def create_superuser(self, phone, username, password=None, **extra_fields):
        """
        Creates a superuser with the given phone number, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, username, password, **extra_fields)
