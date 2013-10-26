from django.test import TestCase

from core.models import Engine

from utils import tracking_utils

import json

import datetime


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
