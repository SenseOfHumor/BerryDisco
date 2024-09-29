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

# Set your Cosmos DB configurations
HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
CONTAINER_ID = config.settings['container_id']

#Function to create a valid event ID/Code

def generate_event_id(container):
    while True:
        event_id = f"{random.randint(0, 999999):06d}"
        query = f"SELECT VALUE c.eventId FROM c WHERE c.eventId = '{event_id}'"
        existing_ids = list(container.query_items(query=query, enable_cross_partition_query=True))

        if not existing_ids:  # If no existing IDs found, the generated ID is unique
            return event_id
        
def get_event_id_by_name(container, event_name):
    try:
        # Query to find the event based on eventName
        query = f"SELECT c.eventId FROM c WHERE c.eventName = '{event_name}'"
        results = list(container.query_items(query=query, enable_cross_partition_query=True))

        if results:
            # Assuming you're getting the first result
            event_id = results[0]['eventId']
            return event_id
        else:
            print(f"No event found with eventName: {event_name}")
            return None

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred while querying event with eventName {event_name}. Error: {e.message}")
        return None

def get_event_name_by_id(container, event_id):
    try:
        # Query to find the event based on eventId
        query = f"SELECT c.eventName FROM c WHERE c.eventId = '{event_id}'"
        results = list(container.query_items(query=query, enable_cross_partition_query=True))

        if results:
            # Assuming you're getting the first result
            event_name = results[0]['eventName']
            return event_name
        else:
            print(f"No event found with eventId: {event_id}")
            return None

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred while querying event with eventId {event_id}. Error: {e.message}")
        return None


#Function to create an event
def create_event(container, event_id, event_name, songs):
    # Check if an event with the same event_id already exists
    existing_query = f"SELECT VALUE c.id FROM c WHERE c.eventId = '{event_id}'"
    existing_events = list(container.query_items(query=existing_query, enable_cross_partition_query=True))
    
    if existing_events:
        print(f"Event with eventId '{event_id}' already exists. Cannot create duplicate.")
        return  # Exit the function or handle it as needed
    
    # If no existing event, proceed to create a new one
    query = "SELECT VALUE c.id FROM c ORDER BY c.id DESC"
    try:
        events = list(container.query_items(query=query, enable_cross_partition_query=True))
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error querying events: {e.message}")
        events = []

    if events:
        # Get the last event's id and increment it
        last_id = int(events[0])  # Convert to integer
        new_id = str(last_id + 1) # New id as a string
    else:
        # If no events exist, start with id = 1
        new_id = "1"
    
    # Create the new event item with the new id
    event_item = {
        "id": new_id,             # Auto-generated id
        "eventId": event_id,      # Partition key based on eventId
        "eventName": event_name,  # Name of the event
        "songs": songs,           # List of songs for this event
        "partitionKey": event_id   # Set partition key to eventId
    }
    
    container.create_item(body=event_item)
    print(f"Created event: {event_item}")

def add_song_to_event(container, event_id, new_song):
    try:
        # Read the existing event by its partition key (eventId)
        query = f"SELECT * FROM c WHERE c.eventId = '{event_id}'"
        event = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if not event:
            print(f"Event with eventId {event_id} not found.")
            return
        
        event = event[0]  # Get the first (and should be the only) item
        
        # Add the new song to the existing list of songs
        event['songs'].append(new_song)

        # Replace the updated event back in the container
        container.replace_item(item=event['id'], body=event)  # Use the auto-generated id for replacement
        print(f"Added new song to event {event_id}: {new_song}")

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred: {e.message}")

def get_song_list(container, event_id):
    try:
        # Use the eventId to query the event
        query = f"SELECT * FROM c WHERE c.eventId = '{event_id}'"
        results = list(container.query_items(query=query, enable_cross_partition_query=True))

        if results:
            # Assuming you're getting the first result
            event = results[0]
            # Return the list of songs with their names and genres
            return [
                {
                    "songName": song.get('songName'),
                }
                for song in event.get('songs', [])
            ]
        else:
            return []

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred while querying event with eventId {event_id}. Error: {e.message}")
        return None

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error occurred while querying event with eventId {event_id}. Error: {e.message}")
        return None


# TESTS functions==========================
songs_list = [
    {

        "songName": "Tropical Paradise",

    },

    {

        "songName": "Island Vibes",
        
    }
]

# Define the new song to add
new_song = {           
    "songName": "Test Funk",   # Name of the new song
}

#add_song_to_event(container, "000003", new_song) # TEST the function to add the new song to the event with eventId "000003"

create_event(container, "000004", "German Party", songs_list) # TEST the create_event function

new_event_id = generate_event_id(container) ##TEST the creat event id fucntion
print(f"Generated Unique Event ID: {new_event_id}")

songs = get_song_list(container, "000003")  # Replace with the event ID you want to check
print("Songs for event 000003:", songs)

event_id = get_event_id_by_name(container, "Tropical Party")##Testing getting event id func
if event_id:
    print(f"Event ID for 'Tropical Party': {event_id}")
else:
    print("Event not found.")

event_name = get_event_name_by_id(container, "000003")##testing getting event name func
if event_name:
    print(f"Event Name for ID '000003': {event_name}")
else:
    print("Event not found.")

