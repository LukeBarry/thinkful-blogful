import os
import unittest
from urllib.parse import urlparse

from werkzeug.security import generate_password_hash

# Configure your app to use the testing database
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog.database import Base, engine, session, User, Entry

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create an example user
        self.user = User(name="Alice", email="alice@example.com",
                         password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)
        
        def simulate_login(self):
            with self.client.session_transaction() as http_session:
                http_session["user_id"] = str(self.user.id)
                http_session["_fresh"] = True

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True
    
    def test_add_entry(self):
        self.simulate_login()

        response = self.client.post("/entry/add", data={
            "title": "Test Entry",
            "content": "Test content"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        entries = session.query(Entry).all()
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertEqual(entry.title, "Test Entry")
        self.assertEqual(entry.content, "Test content")
        self.assertEqual(entry.author, self.user)    
        
    def test_add_entry_not_authenticated(self): 
        response = self.client.get("/entry/add")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/login")
        
    def test_delete_entry(self): 
        self.simulate_login()
        
        user1 = User(name="Jared", email="example@gmail.com", password="password")
        user2 = User(name="Anne", email="example123@gmail.com", password="password")
        
        entry1 = Entry(title="Entry1", content="Some content", author_id=1)
        entry2 = Entry(title="Entry2", content="Some content", author_id=1)
        
        session.add_all([user1, user2, entry1, entry2])
        session.commit()
        
        response = self.client.post("/entry/2/delete")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        
        entry = session.query(Entry).filter(Entry.title == 'Entry2').first()
        
        self.assertEqual(entry, None)
        
    def test_delete_entry_not_author(self): 
        self.simulate_login()
        
        user1 = User(name="Jared", email="example@gmail.com", password="password")
        user2 = User(name="Anne", email="example123@gmail.com", password="password")
        
        entry1 = Entry(title="Entry1", content="Some content", author_id=2)
        entry2 = Entry(title="Entry2", content="Some content", author_id=2)
        
        session.add_all([user1, user2, entry1, entry2])
        session.commit()
        
        response = self.client.get("/entry/2/delete")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")    
        

if __name__ == "__main__":
    unittest.main()