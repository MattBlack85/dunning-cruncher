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
        ('23', '23'),
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

    INVSTATUS_OPT_NL = (
        ('RJ', 'Afgewezen'),
        ('PO', 'Verwerkt'),
        ('PD', 'Betaald'),
        ('NP', 'Nog niet goedgekeurd'),
        ('BL', 'Geblokkeerd'),
        ('NR', 'Niet ontvangen'),
        ('RE', 'Teruggeboekt'),
        ('PB', 'Verwerkt - negatief saldo'),
        ('OX', 'Overige redden')
    )

    INVSTATUS_OPT_FR = (
        ('RJ', 'Refusé'),
        ('PO', 'Comptabilisé'),
        ('PD', 'Payé'),
        ('NP', 'En cours de traitement'),
        ('BL', 'Anomalie sur la commande'),
        ('NR', 'Non reçu'),
        ('RE', 'En cours de traitement'),
        ('PB', 'comptabilisé - compte créditeur'),
        ('OX', 'Autres')
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

    INVSTATUS_OPT_FI = (
        ('RJ', 'Hylätty'),
        ('PO', 'Kirjattu'),
        ('PD', 'Maksettu'),
        ('NP', 'Kirjaamatta'),
        ('BL', 'Pysäytetty'),
        ('NR', 'Ei saapunut'),
        ('CA', 'Peruutettu'),
        ('RE', 'Kumottu'),
        ('PB', 'Kirjattu - velkasaldo'),
        ('OX', 'Muu')
    )

    INVSTATUS_OPT_IT = (
        ('RJ', 'Rifiutato'),
        ('PO', 'Registrato'),
        ('PD', 'Pagato'),
        ('NP', 'Non ancora registrato'),
        ('BL', 'Bloccato'),
        ('NR', 'Non pervenuto'),
        ('PB', 'Registrato - saldo debitore'),
        ('OX', 'Altro')
    )

    INVSTATUS_OPT_PT = (
        ('RJ', 'Rejetada'),
        ('PO', 'Lançada na conta'),
        ('PD', 'Paga no dia '),
        ('NP', 'Ainda não está lançada'),
        ('PK', 'Está a esperar para aprovação'),
        ('BL', 'Bloqueada'),
        ('NR', 'Não recebida'),
        ('CA', 'Lançada e posteriormente anulada'),
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

    REJ_REASONS_IT = (
        ("MPO", "Numero d'ordine mancante"),
        ("BIX", "Informazione errata"),
        ("DIX", "Fattura duplicato"),
        ("OTH", "Altro"),
        ("IDX", "Documento non valido"),
        ("WFI", "Sistema errato, girare su FI"),
        ("WSO", "Sistema errato, girare su SOS"),
        ("WCO", "Sistema errato, girare su COM"),
        ("IPO", "Numero d'ordine errato"),
        ("WCN", "Nome dell'azienda errato"),
        ("WCA", "Indirizzo dell'azienda errato"),
        ("ICX", "Valuta errata"),
        ("MCX", "Valuta mancante"),
        ("WVA", "Importo iva errato"),
        ("MVN", "Importo iva mancante"),
        ("VMX", "Importo della fattura erroneamente calcolato"),
        ("DNV", "Dati del documento non visibili"),
        ("IDM", "Data documento mancante"),
        ("INM", "Numero documento mancante"),
        ("MPX", "Pagine mancanti"),
        ("TFM", "Fattura esente da tasse - nota mancante"),
        ("DEM", "Data/Nota di consegna errate"),
        ("QMX", "Quantità mancante"),
        ("SDM", "Descrizione servizio mancante"),
        ("MIA", "Importo della fattura mancante"),
        ("IIX", "Documento incompleto"),
        ("MAI", "Dati contabili mancanti"),
        ("IAI", "Dati contabili errati"),
        ("MAX", "Autorizzazione mancante"),
        ("IRA", "Indirizzo spedizione errato"),
        ("MRA", "Indirizzo di spedizione mancante"),
        ("RNL", "Indirizzo di spedizione non corrisponde ai dati del fornitore"),
        ("VMX", "Dati fornitore"),
        ("MUI", "Fatture multiple"),
        ("RES", "Da reinserire - pessima qualità")
    )

    REJ_REASONS_PT = (
        ("MPO", "Recursar e devolver ao fornecedor - Falta n pedido"),
        ("BIX", "Recursar e devolver ao fornecedor - Informações incorrectas"),
        ("DIX", "Recursar - Factura dupla"),
        ("OTH", "Outros"),
        ("IDX", "Documento inválido"),
        ("IPO", "Pedido inválido"),
        ("WCN", "Nome da empresa errado"),
        ("WCA", "Endereço da empresa errado"),
        ("ICX", "Moeda incorrecta "),
        ("MCX", "Moeda inexistente "),
        ("WVA", "Montante IVA errado "),
        ("MVN", "Número  IVA inexistente"),
        ("VMX", "Valor na fatura calculado errado"),
        ("DNV", "Dados na fatura não visíveis"),
        ("IDM", "Data fatura inexistente"),
        ("INM", " Número  fatura inexistente"),
        ("MPX", "Páginas inexistentes"),
        ("TFM", "Nota fatura sem imposto inexistente"),
        ("DEM", "Data remessa / Nota remessa inexistente"),
        ("QMX", "Quantidade en falta"),
        ("SDM", "Descrição do serviço inexistente"),
        ("MIA", "Montante fatura inexistente"),
        ("IIX", "Fatura incompleta"),
        ("MAI", "Rejeitar – Informações de contabilidade inexistentes"),
        ("IAI", " Rejeitar – Informações de contabilidade  inválidas"),
        ("MAX", "Rejeitar – Aprovação inexistente"),
        ("VMX", "Dados da empresa incorrectos "),
        ("MUI", "Várias faturas"),
        ("RES", "qualidade baixa")
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

    REJ_REASONS_FI = (
        ("MPO", "Ostotilausnumero puuttuu"),
        ("BIX", "Väärä info"),
        ("DIX", "Tuplalasku"),
        ("OTH", "Muu"),
        ("IDX", "Viallinen tiedosto"),
        ("WFI", "Väärä järjestelmä - Ohjaa FI laatikkoon"),
        ("WSO", "Väärä järjestelmä - Ohjaa SOS laatikkoon"),
        ("WCO", "Väärä järjestelmä - Ohjaa COM laatikkoon"),
        ("IPO", "Viallinen Ostotilausnumero"),
        ("WCN", "Väärä yritysnimi"),
        ("WCA", "Väärä yritysosoite"),
        ("ICX", "Virheellinen valuutta"),
        ("MCX", "Puuttuva valuutta"),
        ("WVA", "Väärä ALV"),
        ("MVN", "Puuttuva ALV"),
        ("VMX", "Laskun summa laskettu virheellisesti"),
        ("DNV", "Laskun tiedot eivät ole näkyvissä"),
        ("IDM", "Laskupäivämäärä puuttuu"),
        ("INM", "Laskunumero puuttuu"),
        ("MPX", "Sivuja puuttuu"),
        ("TFM", "Verovapaa lasku-huomautus puuttuu"),
        ("DEM", "Toimituspäivä / Toimitusviesti puuttuu"),
        ("QMX", "Määrä puuttuu"),
        ("SDM", "Palvelunkuvaus puuttuu"),
        ("MIA", "Laskun summa puuttuu"),
        ("IIX", "Epätäydellinen lasku"),
        ("MAI", "Puuttuva kirjanpitotieto"),
        ("IAI", "Virheellinen kirjanpitotieto"),
        ("MAX", "Puuttuva hyväksyntä"),
        ("IRA", "Virheellinen Lasku Lähettäkää osoitteeseen"),
        ("MRA", "Puuttuva Lähettäkää osoitteeseen"),
        ("RNL", "Lähettäkää osoitteeseen ei yhdistetty toimittajan rekisteriin"),
        ("VMX", "Toimittajahallinta"),
        ("MUI", "Monta laskua"),
        ("RES", "Scannaa uudelleen - huono laatu")
    )

    REJ_REASONS_SE = (
        ("MPO", "Inköpsordernummer saknas"),
        ("BIX", "Fel info"),
        ("DIX", "Dublett"),
        ("OTH", "Annat"),
        ("IDX", "Felaktig dokument"),
        ("WFI", "Fel system - Vidarebefodra till FI box"),
        ("WSO", "Fel system - Vidarebefodra till SOS box"),
        ("WCO", "Fel system - Vidarebefodra till COM box"),
        ("IPO", "Felaktig Inköpsordernummer"),
        ("WCN", "Fel företagsnamn"),
        ("WCA", "Fel företagsadress"),
        ("ICX", "Felaktig Valuta"),
        ("MCX", "Valuta saknas"),
        ("WVA", "Fel MOMS"),
        ("MVN", "MOMS saknas"),
        ("VMX", "Fakturavärde felberäknat"),
        ("DNV", "Fakturainformation ej synlig"),
        ("IDM", "Fakturadatum saknas"),
        ("INM", "Fakturanummer saknas"),
        ("MPX", "Sidor saknas"),
        ("TFM", "Skattefri faktura - notering saknas"),
        ("DEM", "Leveransdatum / Leveransnotering saknas"),
        ("QMX", "Kvantitet saknas"),
        ("SDM", "Tjänstebeskrivning saknas"),
        ("MIA", "Fakturavärde saknas"),
        ("IIX", "Ej fullständig faktura"),
        ("MAI", "Redovisningsinformation saknas"),
        ("IAI", "Felaktig redovisningsinformation"),
        ("MAX", "Saknar acceptans"),
        ("IRA", "Felaktig adress att skicka till"),
        ("MRA", "Saknas adressen att skicka till"),
        ("RNL", "Adressen att skicka till ej kopplad till leverantörsregister"),
        ("VMX", "Leverantörsregister"),
        ("MUI", "Många fakturor"),
        ("RES", "Skanna om - dålig kvalite")
    )

    CURR_OPT = (
        ("EUR", "EUR"),
        ("GBP", "GBP"),
        ("CHF", "CHF"),
        ("NOK", "NOK"),
        ("SEK", "SEK"),
        ("PLN", "PLN"),
        ("USD", "USD"),
        ("DKK", "DKK")
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
    invoicedate = models.DateField(null=True, blank=True)
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
