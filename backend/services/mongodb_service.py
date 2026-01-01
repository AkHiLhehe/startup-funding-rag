"""
MongoDB service for structured data storage
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any, List, Optional
from datetime import datetime

from core.config import settings


class MongoDBService:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.db = self.client[settings.MONGODB_DB_NAME]
            
            # Create indexes
            await self._create_indexes()
            
            print("✅ MongoDB connected successfully")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    async def _create_indexes(self):
        """Create indexes for collections"""
        # Startups indexes
        await self.db.startups.create_index("startup_id", unique=True)
        await self.db.startups.create_index("name")
        await self.db.startups.create_index("industry")
        
        # Investors indexes
        await self.db.investors.create_index("investor_id", unique=True)
        await self.db.investors.create_index("name")
        await self.db.investors.create_index("industries")
        
        # Funding rounds indexes
        await self.db.funding_rounds.create_index("round_id", unique=True)
        await self.db.funding_rounds.create_index("startup_id")
        await self.db.funding_rounds.create_index("date")
        
        # Documents indexes
        await self.db.documents.create_index("source_id", unique=True)
        await self.db.documents.create_index("source_type")
        await self.db.documents.create_index("published_date")
        
        print("✅ MongoDB indexes created")
    
    # Startup operations
    async def create_startup(self, startup_data: Dict[str, Any]) -> str:
        """Create a new startup profile"""
        startup_data["created_at"] = datetime.utcnow()
        startup_data["updated_at"] = datetime.utcnow()
        result = await self.db.startups.insert_one(startup_data)
        return str(result.inserted_id)
    
    async def get_startup(self, startup_id: str) -> Optional[Dict[str, Any]]:
        """Get startup by ID"""
        return await self.db.startups.find_one({"startup_id": startup_id})
    
    async def update_startup(self, startup_id: str, update_data: Dict[str, Any]) -> bool:
        """Update startup profile"""
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db.startups.update_one(
            {"startup_id": startup_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    async def search_startups(self, filters: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        """Search startups with filters"""
        cursor = self.db.startups.find(filters).limit(limit)
        return await cursor.to_list(length=limit)
    
    # Investor operations
    async def create_investor(self, investor_data: Dict[str, Any]) -> str:
        """Create a new investor profile"""
        investor_data["created_at"] = datetime.utcnow()
        investor_data["updated_at"] = datetime.utcnow()
        result = await self.db.investors.insert_one(investor_data)
        return str(result.inserted_id)
    
    async def get_investor(self, investor_id: str) -> Optional[Dict[str, Any]]:
        """Get investor by ID"""
        return await self.db.investors.find_one({"investor_id": investor_id})
    
    async def search_investors(self, filters: Dict[str, Any], limit: int = 50) -> List[Dict[str, Any]]:
        """Search investors with filters"""
        cursor = self.db.investors.find(filters).limit(limit)
        return await cursor.to_list(length=limit)
    
    # Funding round operations
    async def create_funding_round(self, funding_data: Dict[str, Any]) -> str:
        """Create a new funding round record"""
        funding_data["created_at"] = datetime.utcnow()
        result = await self.db.funding_rounds.insert_one(funding_data)
        return str(result.inserted_id)
    
    async def get_funding_rounds(self, startup_id: str) -> List[Dict[str, Any]]:
        """Get all funding rounds for a startup"""
        cursor = self.db.funding_rounds.find({"startup_id": startup_id}).sort("date", -1)
        return await cursor.to_list(length=100)
    
    # Document operations
    async def create_document(self, document_data: Dict[str, Any]) -> str:
        """Store document metadata"""
        document_data["created_at"] = datetime.utcnow()
        result = await self.db.documents.insert_one(document_data)
        return str(result.inserted_id)
    
    async def get_document(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get document by source ID"""
        return await self.db.documents.find_one({"source_id": source_id})
    
    # Query history for evaluation
    async def log_query(self, query_data: Dict[str, Any]) -> str:
        """Log query for evaluation and analytics"""
        query_data["timestamp"] = datetime.utcnow()
        result = await self.db.query_logs.insert_one(query_data)
        return str(result.inserted_id)
    
    async def get_query_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent query logs"""
        cursor = self.db.query_logs.find().sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")
