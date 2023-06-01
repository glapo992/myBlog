"""used to run some unit test. first used to check followers feature.

the finctions that executes tests must be called "tast_<funct_name>
run in terminal : python3 tests.py"""
import os
from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import Users, Posts

# unittest uses another database so it not mess with original datas
os.environ['DATABASE_URL'] = 'sqlite://'

class UserModelCase(unittest.TestCase):

    def setUp(self) -> None:
        """set the context of the test, executed the beginning, the context stays in memory and is not saved"""
        self.app_context = app.app_context()  # create a new application context
        self.app_context.push()
        db.create_all()   # creates all db tables

    def tearDown(self) -> None:
        """clean the context of the test. executed at the end of the test by unittest"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """check password hashing, compare to a wrong pw and than with the correct one"""
        u = Users(username = 'susan')  # crete a user
        u.set_password('cat')           # assign a password 
        self.assertFalse(u.check_password('dog')) # check if the password'hash is not the same for another pw
        self.assertTrue(u.check_password('cat'))  # check if the ash for the same pw is always the same

    def test_avatar(self):
        u = Users(username = 'dr', email='john@example.com')  # crete a user
        self.assertEqual(u.avatar(128),('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=robohash&s=128&r=r') )

    def test_follow(self):
        u1 = Users(username = 'john' , email = 'dr@email.com')
        u2 = Users(username = 'susan', email = 'susan@exe.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        #check that u1 has no followers and is not followed
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        # create the relationship
        u1.follow(u2) 
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        # remove relationship
        u1.unfollow(u2) 
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),0)
        self.assertEqual(u2.followers.count(),0)


    def test_follow_posts(self):
        # create four users
        u1 = Users(username='john', email='john@example.com')
        u2 = Users(username='susan', email='susan@example.com')
        u3 = Users(username='mary', email='mary@example.com')
        u4 = Users(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Posts(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Posts(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Posts(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Posts(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=3)
