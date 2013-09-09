from django.db import models
from django import forms
from django.forms import ModelForm

class Vendor(models.Model):
    vname = models.CharField(max_length=50)
    vnumber = models.IntegerField(max_length=11, unique=True)
    vmail = models.EmailField(unique=True)
    vstate = models.CharField(max_length=20)
    vstreet = models.CharField(max_length=70)
    vcity = models.CharField(max_length=30)
    vnumber = models.CharField(max_length=20)
    vzip = models.CharField(max_length=10)

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
        ('NL', 'Netherland'),
        ('PT', 'Portugal'),
        ('PL', 'Poland'),
        ('GB', 'Great Britain'),
        ('CH', 'Switzerland'),
        ('BE', 'Belgium')
        )

    CCODE_OPT = (
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('18', '18'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('52', '52'),
        ('55', '55'),
        ('60', '60'),
        ('64', '64'),
        ('66', '66')
        )

    LEVEL_OPT = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', 'to scan'),
        )

    INVSTATUS_OPT = (
        ('RJ', 'Rejected'),
        ('PO', 'Posted'),
        ('PD', 'Paid on'),
        ('NP', 'Not posted yet'),
        ('BL', 'Blocked'),
        ('NR', 'Not received'),
        ('CA', 'Cancelled'),
        ('RE', 'Reversed')
        )

    REJ_REASONS = (
        ('MPO', 'Missing PO'),
        )

    market = models.CharField(max_length=3, choices=MARKET_OPT)
    ccode = models.CharField(max_length=2, choices=CCODE_OPT)
    level = models.CharField(max_length=8, choices=LEVEL_OPT)
    clerk = models.CharField(max_length=50)
    actiondate = models.DateField()
    reminderdate = models.DateField()
    remindernumber = models.CharField(max_length=30)
    vendor = models.CharField(max_length=10)
    mailvendor = models.EmailField()
    invoicenumber = models.CharField(max_length=20)
    invoicestatus = models.CharField(max_length=100, choices=INVSTATUS_OPT)
    actiontaken = models.CharField(max_length=1000)
    rejectreason = models.CharField(max_length=3, choices=REJ_REASONS)
    paidon = models.DateField()

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

class TrackingForm(ModelForm):

    class Meta:
	model = Engine
	widgets = {
	    'actiontaken' : forms.Textarea()
            }
