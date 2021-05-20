from bson.objectid import ObjectId

from .database import assignment_collection


async def all():
  output = []
  async for assignment in  assignment_collection.find():
    output.append(assignment)
  return output


async def get(id: str) -> dict:
  return await assignment_collection.find({'_id': ObjectId(id)})


async def create(assignment_data: dict) -> dict:
  assignment = await assignment_collection.insert_one(assignment_data)
  return {
    **assignment_data,
    'id': assignment.inserted_id,
  }

