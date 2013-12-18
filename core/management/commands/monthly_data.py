from core.models import Engine

from django.core.management.base import NoArgsCommand

from dunning_cruncher import settings

from datetime import date

import csv


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        '''
        This function will retrieve all items in DB (done and not done)
        and will save them into a CSV file.
        '''
        csv_list = []

        tyear = date.today().year
        prev_month = date.today().month -1
        data_csv = Engine.objects.filter(actiondate__year=tyear, actiondate__month=prev_month).values()
        csvfile = csv.writer(open('All_data_'+str(prev_month)+str(tyear)+'.csv', 'wb'))

        for item in data_csv:
            csv_list.append(item)

        for x in csv_list:
            csvfile.writerow(x.values())
