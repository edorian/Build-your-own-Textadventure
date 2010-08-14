from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from website.profile.models import Profile


class ProfileTests(TestCase):
    def test_profile_creation(self):
        foo = User.objects.create(username='foo', email='bar@example.com')
        self.assertEquals(Profile.objects.filter(user__username='foo').count(), 1)
        self.assertEquals(foo.profile, Profile.objects.get(user__username='foo'))

    def test_profile_only_for_loggedin_users(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('auth_login') +
        '?next=/profile/')
