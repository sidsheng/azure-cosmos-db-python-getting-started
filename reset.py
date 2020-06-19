import sys
import argparse
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

parser = argparse.ArgumentParser(description='Reset fields in Azure table storage.')
parser.add_argument('--dryRun', dest='dryRun', action='store_true')
parser.add_argument('--accountName', dest='accountName', required=True, action='store')
parser.add_argument('--accountKey', dest='accountKey', required=True, action='store')
parser.add_argument('--type', dest='type', required=True, action='store',
                    choices=['option1', 'option2', 'option3'])
parser.add_argument('--timestamp', dest='timestamp', required=True, action='store')
args = parser.parse_args()

table_service = TableService(args.accountName, args.accountKey)

filterString = "RowKey eq '" + args.type + "' and Timestamp lt datetime'" + args.timestamp + "'"
tasks = table_service.query_entities(
    '<table>', filter=filterString)

if len(tasks.items) == 0:
    print('No entities found.')
    quit()

for task in tasks:
    print(task.PartitionKey)
    task.field1 = False
    if args.dryRun == False:
        table_service.update_entity('<table>', task)
