import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import config

# Set up Cosmos client using URI and master key
client = cosmos_client.CosmosClient(config.settings['host'], config.settings['master_key'])

# Access your specific database and container
database = client.get_database_client(config.settings['database_id'])
container = database.get_container_client(config.settings['container_id'])

# Set your Cosmos DB configurations
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']


def create_event(container, event_id, event_name, songs):
    """
    Create a new event with a list of songs.
    """
    event_item = {
        "id": str(event_id),         # Cosmos requires 'id' field for unique identification
        "eventId": event_id,         # Partition key based on eventId
        "eventName": event_name,     # Name of the event
        "songs": songs,              # List of songs for this event
        "partitionKey": event_id     # Set partition key to eventId
    }
    container.create_item(body=event_item)
    print(f"Created event: {event_item}")


def update_event(container, event_id, new_event_name=None, new_songs=None):
    """
    Update an event's name or replace its song list.
    """
    try:
        # Read the existing event by its id and partition key (eventId)
        event = container.read_item(item=str(event_id), partition_key=event_id)
        
        # If there's a new event name, update it
        if new_event_name:
            event['eventName'] = new_event_name
        
        # If new songs are provided, replace the old song list
        if new_songs is not None:
            event['songs'] = new_songs
        
        # Replace the updated event back in the container
        container.replace_item(item=str(event_id), body=event)
        print(f"Updated event: {event}")

    except exceptions.CosmosHttpResponseError as e:
        print(f"Event with id {event_id} not found. Error: {e.message}")


def add_song_to_event(container, event_id, new_song):
    """
    Add a new song to the song list of an event.
    """
    try:
        # Read the existing event by its id and partition key (eventId)
        event = container.read_item(item=str(event_id), partition_key=event_id)

        # Add the new song to the existing list of songs
        event['songs'].append(new_song)

        # Replace the updated event back in the container
        container.replace_item(item=str(event_id), body=event)
        print(f"Added new song to event {event_id}: {new_song}")

    except exceptions.CosmosHttpResponseError as e:
        print(f"Event with id {event_id} not found. Error: {e.message}")