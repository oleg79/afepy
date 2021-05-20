import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://fastapi-db:27017')

database = client.center

assignment_collection = database.get_collection('assignments')
external_ids_map_collection = database.get_collection('external_ids_map')