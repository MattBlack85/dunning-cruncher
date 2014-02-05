from core.models import Engine

from django.core.management.base import NoArgsCommand

from dunning_cruncher import settings

from datetime import date

import csv


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        '''
        This function will retrieve all items in DB (done and not done)
        during the previous month and will save them into a CSV file.
        '''
        csv_list = []

        tyear = date.today().year
        prev_month = date.today().month -1
        data_csv = Engine.objects.filter(actiondate__year=tyear, actiondate__month=prev_month).values()
        csvfile = csv.writer(open('All_data_'+str(prev_month)+str(tyear)+'.csv', 'wb'))

        status_dict = dict(Engine.INVSTATUS_OPT)

        for item in data_csv:
            item['reasonother'] = item['reasonother'].encode('utf-8')
            item['remindernumber'] = item['remindernumber'].encode('utf-8')
            item['invoicestatus'] = status_dict.get(item['invoicestatus'])
            csv_list.append(item)

        headers = csv_list[0].keys()
        csvfile.writerow(headers)

        for item in csv_list:
            csvfile.writerow(item.values())
