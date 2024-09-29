from azure.cosmos import CosmosClient, PartitionKey, exceptions

HOST = 'your-cosmos-db-endpoint'
MASTER_KEY = 'your-master-key'
DATABASE_ID = 'your-database-id'
CONTAINER_ID = 'your-container-id'

client = CosmosClient(HOST, MASTER_KEY)
database = client.get_database_client(DATABASE_ID)
container = database.get_container_client(CONTAINER_ID)

# Create Item
def create_item(item):
    container.create_item(body=item)

# Read Item
def read_item(item_id, partition_key):
    return container.read_item(item=item_id, partition_key=partition_key)

# Update Item
def update_item(item):
    container.replace_item(item=item['id'], body=item)

# Delete Item
def delete_item(item_id, partition_key):
    container.delete_item(item=item_id, partition_key=partition_key)

# Example Usage
item = {
    'id': '3',
    'partitionKey': '000003',
    'name': 'Sample Event'
}

create_item(item)
print(read_item('3', '000003'))
item['name'] = 'Updated Event'
update_item(item)
delete_item('1', 'event1')