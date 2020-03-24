# from unittest import TestCase
# from server import app

# class FlaskTests(TestCase):

#   def setUp(self):
#       """Stuff to do before every test."""

#       self.client = app.test_client()
#       app.config['TESTING'] = True

#       with self.client as c:
#       with c.session_transaction() as sess:
#       sess['user_id'] = 1

#   def tearDown(self):
#       """To do after each test."""

#   def test_user's_homepage_page(self):
#       """Test user's journal homepage."""

#       result = self.client.get("/user_journal/<int:user_id>")
#       self.assertEqual(result.status_code, 200)
#       self.assertIn(b"You are a valued user", result.data)


#   def test2(self):
#       """Test if user's entry exists."""

#       result = self.client.get("/entry/<int:entry_id>")
#       self.assertEqual(result.status_code, 200)
#       self.assertIn(b"Your entry is here", result.data)