import sys
import argparse
from azure.cosmos import exceptions, CosmosClient, PartitionKey

parser = argparse.ArgumentParser(description='Gets pk based on service details.')
parser.add_argument('--endpoint', dest='endpoint', required=True, action='store')
parser.add_argument('--key', dest='key', required=True, action='store')
parser.add_argument('--field1', metavar='f', dest='field1', action='store')
parser.add_argument('--field2', dest='field2', action='store')
args = parser.parse_args()

# Initialize the Cosmos client
client = CosmosClient(args.endpoint, args.key)

database_name = '<database_name'
database = client.create_database_if_not_exists(id=database_name)

container_name = '<collection_name>'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/pk"),
    offer_throughput=400
)

if (args.field1 is not None):
    query = "SELECT * FROM c WHERE c.field1 IN ('" + args.field1 + "')"
    print('query:{0}'.format(query))

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
    if (len(items) > 0):
        print('pk:{0}'.format(items[0].get("pk")))
elif (args.field2 is not None):
    query = "SELECT * FROM c WHERE c.field2 IN ('" + args.field2 + "')"
    print('query:{0}'.format(query))

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
    if (len(items) > 0):
        print('pk:{0}'.format(items[0].get("pk")))
else:
    print('Invalid arguments')