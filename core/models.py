from django.db import models

class Data(models.Model):

	MARKET_OPT = (
	    ('FI', 'Finland'),
	    ('DK', 'Denmark'),
	    ('SE', 'Sweden'),
	    ('NO', 'Norway'),
	    ('AT', 'Austria'),
	    ('FR', 'France'),
	    ('DE', 'Germany'),
	    ('IT', 'Italy'),
	    ('ES', 'Spain'),
	    ('PT', 'Portugal'),
	    ('PL', 'Poland'),
	    ('GB', 'Great Britain'),
	)

	CCODE_OPT = (
	    ('X', 'X'),
	)

	LEVEL_OPT = (
	    ('1', '1st'),
	    ('2', '2nd'),
	    ('3', '3rd'),
	    ('4', '4th'),
	    ('9', 'to scann'),
	)

	INVSTATUS_OPT = (
	    ('X', 'X'),
	)

	market = models.CharField(max_length=3, choices=MARKET_OPT)
	ccode = models.IntegerField(max_length=2, choices=CCODE_OPT)
	level = models.CharField(max_length=8, choices=LEVEL_OPT)
	apclerk = models.CharField(max_length=50)
	actiondate = models.DateTimeField()
	reminderdate = models.DateTimeField()
	remindernumber = models.CharField(max_length=30)
	vendor = models.IntegerField(max_length=11)
	mailvendor = models.EmailField()
	invoicenumber = models.IntegerField(max_length=20)
	invoicestatus = models.CharField(max_length=100, choices=INVSTATUS_OPT)
