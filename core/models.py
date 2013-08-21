from django.db import models
from django import forms

class Vendor(models.Model):
    vname = models.CharField(max_length=50)
    vnumber = models.IntegerField(max_length=11, unique=True)
    vmail = models.EmailField(unique=True)

    def __unicode__(self):
        return '%s %s %s' %(self.vname, str(self.vnumber), str(self.vmail))

class Engine(models.Model):
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
        ('CH', 'Switzerland'),
    )

    CCODE_OPT = (
        ('10', '10'),
        ('11', '11'),
        ('13', '13'),
        ('15', '15'),
    )

    LEVEL_OPT = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('9', 'to scan'),
    )

    INVSTATUS_OPT = (
        ('PA', 'Paid'),
        ('RTV', 'RTV'),
        ('MI', 'Missing'),
    )

    market = models.CharField(max_length=3, choices=MARKET_OPT)
    ccode = models.CharField(max_length=2, choices=CCODE_OPT)
    level = models.CharField(max_length=8, choices=LEVEL_OPT)
    apclerk = models.CharField(max_length=50)
    actiondate = models.DateTimeField(auto_now_add=True)
    reminderdate = models.DateTimeField()
    remindernumber = models.CharField(max_length=30)
    vendor = models.IntegerField()
    mailvendor = models.EmailField()
    invoicenumber = models.IntegerField(max_length=20)
    invoicestatus = models.CharField(max_length=100, choices=INVSTATUS_OPT)
    actiontaken=models.CharField(max_length=1000)
    
    def is_super(self):
	'''SUPER'''
	return self.user_type == "SUPER"
      
class Login(forms.Form):

    """ Basic login form

    This form renders into a very simple login field, with fields identified
    differently, both for styling and the optional javascript by-name
    handling. Whilst this form is extremely simple, coding one each and
    every time we wish to use one is just dumb and it's much easier to code it
    once and import it into our project.
    """

    uname = forms.CharField(label="Username:")

    uname.widget.attrs.update({'class': 'login-form','id': 'login-user'})

    passw = forms.CharField(label="Password:",widget=forms.PasswordInput())

    passw.widget.attrs.update({'class': 'login-form','id': 'login-password'})
