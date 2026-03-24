from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import recipes.models
import tempfile

def create_user_object():
    user = User.objects.get_or_create(username='testuser',
                                     first_name='Test',
                                     last_name='User',
                                     email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()
    return user

def create_super_user():
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

class AuthSetupTest(TestCase):
    def test_installed_apps(self):
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)

class AuthModelTests(TestCase):
    def test_userprofile_created(self):
        self.assertTrue('UserProfile' in dir(recipes.models))

        user_profile = recipes.models.UserProfile()

        expected_attributes = {
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'picture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0
        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
                
        self.assertEqual(found_count, len(expected_attributes.keys()), f"In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.")
        user_profile.save()

    