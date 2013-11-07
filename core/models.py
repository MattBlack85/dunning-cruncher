# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.forms import ModelForm

class Vendor(models.Model):
    vname = models.CharField(max_length=200)
    vnumber = models.IntegerField(max_length=11, unique=True)
    vmail = models.CharField(max_length=100)
    vstate = models.CharField(max_length=100, null=True, blank=True)
    vstreet = models.CharField(max_length=170, null=True, blank=True)
    vcity = models.CharField(max_length=130, null=True, blank=True)
    vzip = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return '%s %s %s' %(self.vname, str(self.vnumber), str(self.vmail))

class StoredDocs(models.Model):
    dnum = models.CharField(max_length=50)
    file_upload = models.FileField(upload_to='img', blank=True)

    def __unicode__(self):
        return '%s, %s' %(self.dnum, self.file_upload)

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
        ('BE', 'Belgium'),
        ('ES', 'Spain')
        )

    CCODE_OPT = (
        ('0W', '0W'),
        ('0X', '0X'),
        ('0Y', '0Y'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('18', '18'),
        ('19', '19'),
        ('20', '21'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('34', '34'),
        ('36', '36'),
        ('42', '42'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('49', '49'),
        ('52', '52'),
        ('54', '54'),
        ('55', '55'),
        ('56', '56'),
        ('57', '57'),
        ('58', '58'),
        ('60', '60'),
        ('64', '64'),
        ('65', '65'),
        ('66', '66'),
        ('69', '69'),
        ('78', '78'),
        ('80', '80'),
        ('82', '82'),
        ('85', '85')
        )

    LEVEL_OPT = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', 'to scan'),
        ('6', 'critical'),
        ('7', 'non critical'),
        )

    INVSTATUS_OPT = (
        ('RJ', 'Rejected'),
        ('PO', 'Posted'),
        ('PD', 'Paid on'),
        ('NP', 'Not posted yet'),
        ('BL', 'Blocked'),
        ('PK', 'Parked'),
        ('NR', 'Not received'),
        ('CA', 'Cancelled'),
        ('RE', 'Reversed'),
        ('PB', 'Posted - debit balance'),
        ('OX', 'Other')
        )

    INVSTATUS_OPT_DE = (
        ('RJ', 'Abgelehnt'),
        ('PO', 'Verbucht'),
        ('PD', 'Bezahlt am'),
        ('NP', 'Noch nicht gebucht'),
        ('BL', 'Gesperrt'),
        ('PK', 'Vorerfasst'),
        ('NR', 'Nicht erhalten'),
        ('CA', 'Storniert'),
        ('PB', 'Verbucht - im sollsaldo'),
        ('OX', 'Andere')
    )

    INVSTATUS_OPT_FI = (
        ('RJ', 'Hylätty'),
        ('PO', 'Kirjattu'),
        ('PD', 'Maksettu'),
        ('NP', 'Kirjaamatta'),
        ('BL', 'Pysäytetty'),
        ('NR', 'Ei saapunut'),
        ('CA', 'Peruutettu'),
        ('RE', 'Kumottu'),
        ('PB', 'Lähetetty - velkasaldo'),
        ('OX', 'Muu')
        )

    INVSTATUS_OPT_SE = (
        ('RJ', 'Avvisat'),
        ('PO', 'Bokfört'),
        ('PD', 'Betalt den'),
        ('NP', 'Inte bokfört än'),
        ('BL', 'Blockerat'),
        ('NR', 'Inte mottagits'),
        ('CA', 'Raderad'),
        ('RE', 'Annulerat'),
        ('PB', 'Bokfört - debit balans'),
        ('OX', 'Annat')
        )

    REJ_REASONS = (
        ("MPO", "Missing Purchase Order Number"),
        ("BIX", "Bad information"),
        ("DIX", "Duplicate invoice"),
        ("OTH", "Other"),
        ("IDX", "Invalid document"),
        ("WFI", "Wrong system - Route to FI box"),
        ("WSO", "Wrong system - Route to SOS box"),
        ("WCO", "Wrong system - Route to COM box"),
        ("IPO", "Invalid Purchase Order"),
        ("WCN", "Wrong company name"),
        ("WCA", "Wrong company address"),
        ("ICX", "Incorrect currency"),
        ("MCX", "Missing currency"),
        ("WVA", "Wrong VAT amount"),
        ("MVN", "Missing VAT number"),
        ("VMX", "Value on the invoice miscalculated"),
        ("DNV", "Data on the invoice not visible"),
        ("IDM", "Invoice date missing"),
        ("INM", "Invoice number missing"),
        ("MPX", "Missing pages"),
        ("TFM", "Tax free invoice-note missing"),
        ("DEM", "Delivery date / Delivery Note Missing"),
        ("QMX", "Quantity missing"),
        ("SDM", "Service description missing"),
        ("MIA", "Missing Invoice Amount"),
        ("IIX", "Incomplete Invoice"),
        ("MAI", "Missing Accounting Information"),
        ("IAI", "Invalid Accounting Information"),
        ("MAX", "Missing Approval"),
        ("IRA", "Invalid Remit To Address"),
        ("MRA", "Missing Remit To Address"),
        ("RNL", "Remit to address not linked to vendor's record"),
        ("VMX", "Vendor Master"),
        ("MUI", "Multiple invoices"),
        ("RES", "Rescan, poor quality")
        )

    REJ_REASONS_NL = (
        ("MPO", "Ontbrekend PO nummer"),
        ("BIX", "Onjuiste informatie"),
        ("DIX", "Duplicaat"),
        ("OTH", "Overige reden"),
        ("IDX", "Ongeldig document"),
        ("WFI", "Incorrect systeem - doorgestuurd naar FIN box"),
        ("WSO", "Incorrect systeem - doorgestuurd naar SOS box"),
        ("WCO", "Incorrect systeem - doorgestuurd naar COM box"),
        ("IPO", "Ongeldig PO nummer"),
        ("WCN", "Onjuiste bedrijfsnaam"),
        ("WCA", "Onjuist bedrijsfadres"),
        ("ICX", "Onjuiste valuta"),
        ("MCX", "Ontbrekende valuta"),
        ("WVA", "Incorrect BTW bedrag"),
        ("MVN", "Ontbrekend BTW nummer"),
        ("VMX", "Miscalculatie op factuur"),
        ("DNV", "Informatie niet zichtbaar op de factuur"),
        ("IDM", "Ontbrekende factuurdatum"),
        ("INM", "Ontbrekend factuurnummer"),
        ("MPX", "Ontbrekende paginas"),
        ("TFM", "Onbrekende BTW vrijstelling "),
        ("DEM", "Ontbrekende leveringsdatum/ontbrekende vrachtbrief"),
        ("QMX", "Ontbrekende hoeveelheidsvermelding"),
        ("SDM", "Onbrekende dienstomschrijving"),
        ("MIA", "Ontbrekend factuurbedrag"),
        ("IIX", "Incomplete factuur"),
        )

    REJ_REASONS_DE = (
        ("MPO", "Bestellnummer fehlt"),
        ("BIX", "Falsche informationen"),
        ("DIX", "Doppelte rechnung"),
        ("OTH", "Sonstige"),
        ("IDX", "Ungültiges dokument"),
        ("WFI", "Falsches system - an FI-Box umleiten"),
        ("WSO", "Falsches system - an SOS-Box umleiten"),
        ("WCO", "Falsches system - an COM-Box umleiten"),
        ("IPO", "Ungültige bestellung"),
        ("WCN", "Falscher firmenname"),
        ("WCA", "Falsche firmenadresse"),
        ("ICX", "Falsche währung"),
        ("MCX", "Fehlende währung"),
        ("WVA", "Falscher steuerbetrag"),
        ("MVN", "Fehlende Steuernummer"),
        ("VMX", "Wert auf rechnung falsch berechnet"),
        ("DNV", "Daten auf rechnung nicht sichtbar"),
        ("IDM", "Rechnungsdatum fehlt"),
        ("INM", "Rechnungsnummer fehlt"),
        ("MPX", "Seiten fehlen"),
        ("TFM", "Hinweis steuerfrei fehlt"),
        ("DEM", "Menge fehlt"),
        ("QMX", "Lieferdatum/Lieferschein fehlt"),
        ("SDM", "Dienstleistungsbeschreibung fehlt"),
        ("MIA", "Rechnungsbetrag fehlt"),
        ("IIX", "Unvollständige rechnung"),
        ("MAI", "Fehlende rechnungsweseninformationen"),
        ("IAI", "Ungültige rechnungsweseninformationen"),
        ("MAX", "Fehlende genehmigung"),
        ("IRA", "Untültige avisadresse"),
        ("MRA", "Fehlende avisadresse"),
        ("RNL", "Avisadresse nicht mit lieferantenstamm verknüpft"),
        ("VMX", "Lieferantenstamm"),
        ("MUI", "Mehrere rechnungen"),
        ("RES", "Neu scannen, schlechte qualität")
        )

    CURR_OPT = (
        ("EUR", "EUR"),
        ("GBP", "GBP"),
        ("CHF", "CHF"),
        ("NOK", "NOK"),
        ("SEK", "SEK"),
        ("PLN", "PLN"),
        ("USD", "USD")
        )

    market = models.CharField(max_length=3, choices=MARKET_OPT)
    ccode = models.CharField(max_length=2, choices=CCODE_OPT)
    level = models.CharField(max_length=8, choices=LEVEL_OPT)
    clerk = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURR_OPT, null=True, blank=True)
    attachment = models.ForeignKey(StoredDocs, null=True, blank=True)
    reasonother = models.CharField(max_length=500, null=True, blank=True)
    actiondate = models.DateField()
    reminderdate = models.DateField()
    remindernumber = models.CharField(max_length=30)
    vendor = models.CharField(max_length=10)
    mailvendor = models.EmailField(null=True, blank=True)
    invoicenumber = models.CharField(max_length=20)
    invoicestatus = models.CharField(max_length=100, choices=INVSTATUS_OPT)
    actiontaken = models.CharField(max_length=100, blank=True)
    rejectreason = models.CharField(max_length=3, choices=REJ_REASONS, null=True, blank=True)
    paidon = models.DateField(null=True, blank=True)
    done = models.BooleanField()

    def __unicode__(self):
        return self.remindernumber

    def is_done(self):
        return self.done

    is_done.short_description = 'Done?'
    is_done.boolean = True

class StoredForm(ModelForm):

    class Meta:
	model = StoredDocs

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
	    'reasonother' : forms.Textarea()
            }
