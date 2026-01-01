import asyncio
from services.weaviate_service import WeaviateService

async def check_data():
    svc = WeaviateService()
    await svc.initialize()
    
    collections = ['StartupDocument', 'InvestorDocument', 'FundingDocument']
    for collection_name in collections:
        try:
            collection = svc.client.collections.get(collection_name)
            result = collection.query.fetch_objects(limit=100)
            count = len(result.objects)
            print(f'{collection_name}: {count} objects')
            if count > 0:
                print(f'  Sample: {result.objects[0].properties.get("source_title", "N/A")}')
        except Exception as e:
            print(f'{collection_name}: Error - {e}')
            import traceback
            traceback.print_exc()
    
    svc.client.close()

asyncio.run(check_data())
