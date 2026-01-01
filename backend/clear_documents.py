import asyncio
from services.mongodb_service import MongoDBService

async def clear():
    svc = MongoDBService()
    await svc.connect()
    result = await svc.db['documents'].delete_many({})
    print(f'✅ Deleted {result.deleted_count} documents from MongoDB')
    await svc.close()

asyncio.run(clear())
