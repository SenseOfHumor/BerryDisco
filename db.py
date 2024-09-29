import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import config
import random

# Set up Cosmos client using URI and master key
client = cosmos_client.CosmosClient(config.settings['host'], config.settings['master_key'])

# Access your specific database and container
database = client.get_database_client(config.settings['database_id'])
container = database.get_container_client(config.settings['container_id'])

# exposing the container to the app.py
__all__ = ["container", "create_event", "get_songs", "add_song_to_event", "get_event_name"]

# Function to generate a unique 6-digit event ID
def generate_event_id(container):
    while True:
        event_id = f"{random.randint(0, 999999):06d}"
        query = f"SELECT VALUE c.id FROM c WHERE c.id = '{event_id}'"
        existing_ids = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if not existing_ids:  # If no existing IDs found, the generated ID is unique
            return event_id

# Function to create a new event with a default name and empty song list
def create_event(container, ename ):
    event_id = generate_event_id(container)

    if ename == "":
        event_name = f"Event {event_id}" # Default event name
    else:
        event_name = ename  

    songs = []  # Empty song list

    # Create the new event item
    event_item = {
        "id": event_id,        # Use eventId as the document id and partition key
        "event_name": event_name,  # Name of the event
        "songs": songs         # Empty list of songs for this event
    }

    # Add the event to the container
    container.create_item(body=event_item)
    print(f"Created event with ID {event_id} and default name '{event_name}'")
    return event_id

# Function to get the list of songs for a given event ID
def get_songs(container, event_id):
    try:
        # Query the event by its id
        query = f"SELECT * FROM c WHERE c.id = '{event_id}'"
        event = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if not event:
            print(f"Event with id {event_id} not found.")
            return []
        
        event = event[0]  # Get the first (and should be the only) item
        return event.get('songs', [])  # Return the list of songs
        
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred while querying event with id {event_id}. Error: {e.message}")
        return []

# Function to add a song to an event
def add_song_to_event(container, event_id, song_name):
    try:
        # Read the existing event by its partition key (id)
        query = f"SELECT * FROM c WHERE c.id = '{event_id}'"
        event = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if not event:
            print(f"Event with id {event_id} not found.")
            return
        
        event = event[0]  # Get the first (and should be the only) item
        
        # Add the new song to the existing list of songs
        event['songs'].append(song_name)

        # Replace the updated event back in the container
        container.replace_item(item=event['id'], body=event)
        print(f"Added new song to event {event_id}: {song_name}")
        
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred: {e.message}")

# Function to get the event name by ID
def get_event_name(container, event_id):
    try:
        # Query the event by its id
        query = f"SELECT * FROM c WHERE c.id = '{event_id}'"
        event = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if not event:
            print(f"Event with id {event_id} not found.")
            return None
        
        event = event[0]  # Get the first (and should be the only) item
        return event.get('event_name')  # Return the event name
        
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred while querying event with id {event_id}. Error: {e.message}")
        return None

# # Test code
# if __name__ == "__main__":
#     # Create a new event
#     new_event_id = create_event(container, "Swapnil")

#     # Add some songs to the newly created event
#     add_song_to_event(container, new_event_id, "Song 1")
#     add_song_to_event(container, new_event_id, "Song 2")
    
#     # Get the list of songs for the event
#     songs = get_songs(container, '133928')
#     print(f"Songs for event {new_event_id}: {songs}")

#     # Get the event name by ID
#     event_name = get_event_name(container, new_event_id)
#     print(event_name)
