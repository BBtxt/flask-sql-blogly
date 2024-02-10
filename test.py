    # FILEPATH: tests.py
import unittest
from app import app, db
from models import Users, Posts

class FlaskBloglyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Set up test database
        db.create_all()

        # Add a test user and post
        self.user = Users(first_name='Test', last_name='User')
        db.session.add(self.user)
        db.session.commit()

        self.post = Posts(title='Test Post', content='Test Content', user_id=self.user.id)
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_new_post(self):
        response = self.client.get(f'/{self.user.id}/posts/new')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.get(f'/{self.user.id}/posts/{self.post.id}')
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        response = self.client.get(f'/{self.user.id}/posts/{self.post.id}/edit')
        self.assertEqual(response.status_code, 200)

    # Add more tests...

if __name__ == '__main__':
    unittest.main()