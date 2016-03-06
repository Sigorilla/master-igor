import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Post


class PostMethodTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() should return False for posts whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_post = Post(
            title='Test post',
            intro='Test intro',
            pub_date=time
        )
        self.assertEqual(future_post.was_published_recently(), False)
