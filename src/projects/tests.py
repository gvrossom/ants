import datetime
import factory
import os


from django.contrib.auth import get_user_model
from django.test import TestCase

from waliki import settings

from .models import Project


User = get_user_model()


rst = """
Title
=====
some rst markup
.. raw:: html
   <script>alert()</script>
"""

rst_html = """\n    <h2>Title</h2>\n    <p>some rst markup</p>\n"""

md = """
# Hi
I'm Markdown
<script>alert()</script>
"""

md_html = """<h2 id="hi">Hi</h2>\n<p>I\'m Markdown\n</p>\n"""


class TestProject(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(
            password='sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161',
            last_login=datetime.datetime(2006, 12, 17, 7, 3, 31), is_superuser=False,
            name="wouter",
            email='test@example.com', is_staff=False, is_active=True,
            date_joined=datetime.datetime(2006, 12, 17, 7, 3, 31)
        )
        self.page = Project.objects.create(title='Title here', creator=self.u1)


    def test_content_saved_on_attribute_set(self):
        self.page.raw = rst
        self.path = os.path.join(settings.WALIKI_DATA_DIR, 'wouter/995c9b1ac3ca7356a8b4225171158e70.rst')
        self.assertEqual(self.page.abspath, self.path)
        self.assertTrue(os.path.exists(self.path))
        content = open(self.path).read()
        self.assertEqual(content, rst)

    def test_raw_empty_if_file_doesnt_exist(self):
        page = Project(path='test3.rst')
        assert not os.path.exists(page.abspath)
        self.assertEqual(page.raw, "")

    def test_slug_and_path_populated_from_name_if_not_given(self):
        self.assertEqual(self.page.slug, 'wouter/995c9b1ac3ca7356a8b4225171158e70')
        self.assertEqual(self.page.path, 'wouter/995c9b1ac3ca7356a8b4225171158e70.rst')

    # def test_slug_strip_slashes(self):
    #     page = Project(slug='/some/slug/')
    #     page.save()
    #     self.assertEqual(page.slug, 'some/slug')

    def test_update_extension(self):
        page = Project(title='test title', creator=self.u1)
        page.save()
        assert page.markup == 'reStructuredText'
        old_path = page.abspath
        assert os.path.exists(old_path)
        page.markup = 'Markdown'
        page.update_extension()
        self.assertTrue(os.path.exists(page.abspath))
        self.assertFalse(os.path.exists(old_path))
        self.assertTrue(page.path.endswith('.md'))
        # self.assertEqual(page.raw, 'Hello')