# from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
#
#
# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a User with the given email and password.
#         """
#         if not email:
#             raise ValueError(_('The Email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_super_user(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_system_user', True)
#         extra_fields.setdefault('is_super_user', True)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_locked', False)
#         return self.create_user(email, password, **extra_fields)
#
#     def create_system_user(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault('is_system_user', True)
#         extra_fields.setdefault('is_super_user', False)
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('is_locked', False)
#         return self.create_user(email, password, **extra_fields)