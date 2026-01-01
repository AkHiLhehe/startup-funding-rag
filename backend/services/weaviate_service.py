"""
Weaviate vector database service
"""
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Any, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

from core.config import settings


class WeaviateService:
    def __init__(self):
        self.client = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    async def initialize(self):
        """Initialize Weaviate client and create schema"""
        try:
            if settings.WEAVIATE_USE_EMBEDDED:
                self.client = weaviate.connect_to_embedded()
            else:
                # Parse host and port from URL
                url = settings.WEAVIATE_URL.replace("http://", "").replace("https://", "")
                if ":" in url:
                    host, port = url.split(":")
                    self.client = weaviate.connect_to_local(
                        host=host,
                        port=int(port)
                    )
                else:
                    self.client = weaviate.connect_to_local(host=url)
            
            # Create collections if they don't exist
            await self._create_collections()
            print("✅ Weaviate initialized successfully")
            
        except Exception as e:
            print(f"❌ Failed to initialize Weaviate: {e}")
            raise
    
    async def _create_collections(self):
        """Create Weaviate collections for different data types"""
        collections = [
            {
                "name": "StartupDocument",
                "description": "Documents related to startups",
                "properties": [
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="source_id", data_type=DataType.TEXT),
                    Property(name="source_type", data_type=DataType.TEXT),
                    Property(name="source_title", data_type=DataType.TEXT),
                    Property(name="source_url", data_type=DataType.TEXT),
                    Property(name="chunk_index", data_type=DataType.INT),
                    Property(name="startup_id", data_type=DataType.TEXT, skip_vectorization=True),
                    Property(name="round_id", data_type=DataType.TEXT, skip_vectorization=True),
                    Property(name="published_date", data_type=DataType.DATE),
                ]
            },
            {
                "name": "InvestorDocument",
                "description": "Documents related to investors and VCs",
                "properties": [
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="source_id", data_type=DataType.TEXT),
                    Property(name="source_type", data_type=DataType.TEXT),
                    Property(name="source_title", data_type=DataType.TEXT),
                    Property(name="source_url", data_type=DataType.TEXT),
                    Property(name="chunk_index", data_type=DataType.INT),
                    Property(name="investor_id", data_type=DataType.TEXT, skip_vectorization=True),
                    Property(name="published_date", data_type=DataType.DATE),
                ]
            },
            {
                "name": "FundingDocument",
                "description": "Documents about funding rounds and announcements",
                "properties": [
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="source_id", data_type=DataType.TEXT),
                    Property(name="source_type", data_type=DataType.TEXT),
                    Property(name="source_title", data_type=DataType.TEXT),
                    Property(name="source_url", data_type=DataType.TEXT),
                    Property(name="chunk_index", data_type=DataType.INT),
                    Property(name="round_id", data_type=DataType.TEXT, skip_vectorization=True),
                    Property(name="startup_id", data_type=DataType.TEXT, skip_vectorization=True),
                    Property(name="published_date", data_type=DataType.DATE),
                ]
            }
        ]
        
        # Create collections
        
        for collection_config in collections:
            try:
                if not self.client.collections.exists(collection_config["name"]):
                    self.client.collections.create(
                        name=collection_config["name"],
                        description=collection_config["description"],
                        vectorizer_config=Configure.Vectorizer.none(),
                        properties=collection_config["properties"]
                    )
                    print(f"✅ Created collection: {collection_config['name']}")
            except Exception as e:
                print(f"⚠️  Collection {collection_config['name']} might already exist: {e}")
    
    async def add_documents(self, collection_name: str, documents: List[Dict[str, Any]], vectors: List[List[float]]):
        """Add documents with their vectors to a collection"""
        try:
            print(f"🔍 Adding {len(documents)} documents to {collection_name}")
            collection = self.client.collections.get(collection_name)
            
            # Insert documents one by one to debug
            inserted_count = 0
            for idx, (doc, vector) in enumerate(zip(documents, vectors)):
                try:
                    uuid = collection.data.insert(
                        properties=doc,
                        vector=vector
                    )
                    inserted_count += 1
                    print(f"  ✅ Inserted document {idx + 1}/{len(documents)}: {uuid}")
                except Exception as e:
                    print(f"  ❌ Failed to insert document {idx + 1}: {e}")
            
            print(f"✅ Successfully inserted {inserted_count}/{len(documents)} documents to {collection_name}")
            return True
        except Exception as e:
            print(f"❌ Error adding documents: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    async def search(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents in a collection"""
        try:
            collection = self.client.collections.get(collection_name)
            
            response = collection.query.near_vector(
                near_vector=query_vector,
                limit=limit,
                return_metadata=MetadataQuery(distance=True)
            )
            
            results = []
            for obj in response.objects:
                result = {
                    "uuid": str(obj.uuid),
                    "properties": obj.properties,
                    "distance": obj.metadata.distance if obj.metadata else None
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ Error searching: {e}")
            raise
    
    async def hybrid_search(
        self,
        collection_name: str,
        query_text: str,
        query_vector: List[float],
        limit: int = 10,
        alpha: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Hybrid search combining vector and keyword search"""
        try:
            # Use GraphQL directly to avoid client deserialization issues
            import requests
            
            print(f"🔍 Performing hybrid search on {collection_name}")
            print(f"   Query: '{query_text[:50]}...'")
            print(f"   Alpha: {alpha}, Limit: {limit}")
            
            # Build collection-specific fields
            common_fields = """
                  content
                  source_id
                  source_type
                  source_title
                  source_url
                  chunk_index
                  published_date
            """
            
            # Add collection-specific fields
            if collection_name == "StartupDocument":
                specific_fields = "startup_id\n                  round_id"
            elif collection_name == "InvestorDocument":
                specific_fields = "investor_id"
            elif collection_name == "FundingDocument":
                specific_fields = "round_id\n                  startup_id"
            else:
                specific_fields = ""
            
            query = """
            {
              Get {
                %s(
                  hybrid: {
                    query: "%s",
                    alpha: %f,
                    vector: %s
                  }
                  limit: %d
                ) {
                  %s
                  %s
                  _additional {
                    id
                    score
                    distance
                  }
                }
              }
            }
            """ % (collection_name, query_text.replace('"', '\\"'), alpha, str(query_vector), limit, common_fields, specific_fields)
            
            response = requests.post(
                f"{settings.WEAVIATE_URL}/v1/graphql",
                json={"query": query}
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"   GraphQL errors: {data['errors']}")
            
            results = []
            if "data" in data and "Get" in data["data"] and collection_name in data["data"]["Get"]:
                objects = data["data"]["Get"][collection_name]
                print(f"   Found {len(objects)} objects in GraphQL response")
                for obj in objects:
                    additional = obj.pop("_additional", {})
                    # Convert score to float (GraphQL returns strings)
                    score = additional.get("score")
                    if score is not None:
                        score = float(score)
                    result = {
                        "uuid": additional.get("id"),
                        "properties": obj,
                        "score": score
                    }
                    results.append(result)
            
            print(f"✅ Returning {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Error in hybrid search: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    async def close(self):
        """Close the Weaviate client connection"""
        if self.client:
            self.client.close()
            print("✅ Weaviate connection closed")
