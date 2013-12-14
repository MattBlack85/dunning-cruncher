from django.test import TestCase, Client

from core.models import Engine

from utils import tracking_utils

from django.contrib.auth.models import User, Group

import json

import datetime

class TestUser(TestCase):
    @classmethod
    def setUp(self):
        # Let's create a dummy user for our tests.
        create_test_user(self)

class AnotherTest(TestUser):
    def test_no_group(self):
        self.assertEqual(self.testuser.groups.count(), 0)

    def test_group_RU(self):
        self.testuser.groups.add(1)
        client = Client()
        client.post('/login/', {'uname': 'testuser', 'passw':'password'})
        response = client.get('/reporting/2013/49/')
        self.assertEqual(self.testuser.groups.get().name, 'RU')
        self.assertEqual(response.status_code, 403)


    def destroy_group(self):
        delete_group(self)
        print self.testuser.groups.count()
        self.assertEqual(self.testuser.groups.count(), 0)
        
        

class EngineTest(TestCase):

    def test_track_new_item(self):
        """
        Tests if a new basic item is tracked successfuly into DB.
        """
        item = Engine(
            market='IT',
            ccode='15',
            level='2',
            clerk ='John Doe',
            amount='1000.01',
            currency='EUR',
            attachment=None,
            reasonother='Other',
            actiondate='2013-10-15',
            reminderdate='2013-10-11',
            remindernumber='123456',
            vendor='100123456',
            mailvendor='john.doe@noone.com',
            invoicenumber='987654321',
            invoicestatus='PO',
            done=0
        )

        item.full_clean()
        item.save()

        self.assertNotEqual(item.pk, None)

def create_test_user(cls):
    cls.testuser = User.objects.create_user('testuser', 'test@test.com', 'password')
    Group.objects.create(name='RU')

def delete_test_user(cls):
    User.objects.filter(username='testuser').delete()

def delete_group(cls):
    Group.objects.all().delete()
