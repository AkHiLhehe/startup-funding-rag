"""
Sample data seeding script
Run this to populate the system with example data
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from services.mongodb_service import MongoDBService
from services.weaviate_service import WeaviateService
from services.embedding_service import DeepSeekEmbeddingService
from services.rag_pipeline import RAGPipeline
from services.llm_service import GeminiService


# Sample startup data
SAMPLE_STARTUPS = [
    {
        "startup_id": "techcorp_ai",
        "name": "TechCorp AI",
        "description": "Leading AI company building enterprise machine learning solutions",
        "industry": ["Artificial Intelligence", "Enterprise Software"],
        "stage": "Series B",
        "funding_amount": 50000000,
        "location": "San Francisco, CA",
        "founded_year": 2020,
        "team_size": 75
    },
    {
        "startup_id": "fintech_plus",
        "name": "FintechPlus",
        "description": "Digital banking platform for Gen Z",
        "industry": ["Fintech", "Banking"],
        "stage": "Series A",
        "funding_amount": 15000000,
        "location": "New York, NY",
        "founded_year": 2021,
        "team_size": 40
    },
    {
        "startup_id": "health_tech",
        "name": "HealthTech Solutions",
        "description": "Telemedicine and digital health records",
        "industry": ["Healthcare", "Technology"],
        "stage": "Seed",
        "funding_amount": 3000000,
        "location": "Boston, MA",
        "founded_year": 2022,
        "team_size": 15
    }
]

# Sample investor data
SAMPLE_INVESTORS = [
    {
        "investor_id": "sequoia",
        "name": "Sequoia Capital",
        "type": "VC",
        "investment_thesis": "We partner with bold founders who challenge convention and pursue massive opportunities",
        "industries": ["Technology", "Healthcare", "Fintech", "AI"],
        "stages": ["Seed", "Series A", "Series B", "Series C"],
        "ticket_size_min": 1000000,
        "ticket_size_max": 100000000,
        "location": "Menlo Park, CA",
        "portfolio_companies": ["techcorp_ai"]
    },
    {
        "investor_id": "accel",
        "name": "Accel Partners",
        "type": "VC",
        "investment_thesis": "We focus on early-stage companies building category-defining products",
        "industries": ["SaaS", "Fintech", "Enterprise"],
        "stages": ["Seed", "Series A"],
        "ticket_size_min": 500000,
        "ticket_size_max": 50000000,
        "location": "Palo Alto, CA",
        "portfolio_companies": ["fintech_plus"]
    },
    {
        "investor_id": "yc",
        "name": "Y Combinator",
        "type": "Accelerator",
        "investment_thesis": "We help startups grow to become large companies",
        "industries": ["Technology", "Software", "Hardware"],
        "stages": ["Pre-Seed", "Seed"],
        "ticket_size_min": 125000,
        "ticket_size_max": 500000,
        "location": "Mountain View, CA",
        "portfolio_companies": ["health_tech"]
    }
]

# Sample funding rounds
SAMPLE_FUNDING_ROUNDS = [
    {
        "round_id": "techcorp_series_b",
        "startup_id": "techcorp_ai",
        "round_type": "Series B",
        "amount": 50000000,
        "valuation": 300000000,
        "investors": ["sequoia", "accel"],
        "date": "2024-01-15T00:00:00Z",
        "announcement_url": "https://example.com/techcorp-series-b"
    },
    {
        "round_id": "fintech_series_a",
        "startup_id": "fintech_plus",
        "round_type": "Series A",
        "amount": 15000000,
        "valuation": 75000000,
        "investors": ["accel"],
        "date": "2023-11-20T00:00:00Z",
        "announcement_url": "https://example.com/fintech-series-a"
    },
    {
        "round_id": "health_seed",
        "startup_id": "health_tech",
        "round_type": "Seed",
        "amount": 3000000,
        "valuation": 15000000,
        "investors": ["yc"],
        "date": "2023-06-10T00:00:00Z",
        "announcement_url": "https://example.com/health-seed"
    }
]

# Sample documents for ingestion
SAMPLE_DOCUMENTS = [
    {
        "content": """
        TechCorp AI Raises $50M Series B to Expand Enterprise ML Platform
        
        San Francisco, January 15, 2024 - TechCorp AI, a leading artificial intelligence 
        company, today announced it has raised $50 million in Series B funding. The round 
        was led by Sequoia Capital, with participation from existing investor Accel Partners.
        
        The company, which provides enterprise machine learning solutions, plans to use 
        the funding to expand its engineering team, accelerate product development, and 
        increase sales and marketing efforts. TechCorp AI currently serves over 200 
        enterprise clients including Fortune 500 companies.
        
        "This funding validates our vision of making AI accessible to every enterprise," 
        said John Smith, CEO of TechCorp AI. "We're seeing massive demand for our platform 
        as companies race to integrate AI into their operations."
        
        Sequoia Capital partner Jane Doe will join TechCorp AI's board of directors. 
        "TechCorp AI has built an exceptional product that solves real enterprise needs," 
        she commented. "We're excited to partner with them on this journey."
        
        Founded in 2020, TechCorp AI has now raised a total of $75 million and employs 
        75 people across offices in San Francisco and New York.
        """,
        "metadata": {
            "title": "TechCorp AI Raises $50M Series B",
            "url": "https://example.com/techcorp-series-b",
            "startup_id": "techcorp_ai",
            "round_id": "techcorp_series_b",
            "published_date": "2024-01-15T00:00:00Z"
        },
        "document_type": "announcement"
    },
    {
        "content": """
        FintechPlus Secures $15M Series A Led by Accel Partners
        
        New York, November 20, 2023 - FintechPlus, a digital banking platform targeting 
        Gen Z users, announced today it has closed a $15 million Series A funding round 
        led by Accel Partners.
        
        The company offers a mobile-first banking experience with features designed for 
        young professionals, including automatic savings, investment tools, and 
        peer-to-peer payments. Since launching in 2021, FintechPlus has grown to over 
        500,000 active users.
        
        "Traditional banks haven't adapted to how young people want to manage their 
        finances," said Sarah Johnson, co-founder and CEO. "We're building the bank 
        of the future, designed from the ground up for digital natives."
        
        The new capital will be used to enhance the product, expand the team to 40 
        employees, and launch new features including cryptocurrency trading and 
        international money transfers.
        
        Accel Partners' Mike Chen commented: "FintechPlus has impressive unit economics 
        and engagement metrics. They've proven they can acquire and retain users at scale."
        """,
        "metadata": {
            "title": "FintechPlus Secures $15M Series A",
            "url": "https://example.com/fintech-series-a",
            "startup_id": "fintech_plus",
            "round_id": "fintech_series_a",
            "published_date": "2023-11-20T00:00:00Z"
        },
        "document_type": "announcement"
    },
    {
        "content": """
        Y Combinator-Backed HealthTech Solutions Raises $3M Seed Round
        
        Boston, June 10, 2023 - HealthTech Solutions, a telemedicine and digital health 
        records startup, today announced it has raised $3 million in seed funding. 
        Y Combinator led the round, with participation from several angel investors.
        
        The company provides a platform that connects patients with healthcare providers 
        through video consultations and maintains secure digital health records. 
        HealthTech Solutions aims to make healthcare more accessible and affordable.
        
        "Healthcare is broken, especially in rural and underserved areas," said 
        Dr. Emily Chen, founder and CEO. "Our platform makes it easy for anyone to 
        access quality healthcare from their phone."
        
        The startup, which graduated from Y Combinator's Winter 2023 batch, has already 
        facilitated over 10,000 consultations and partnered with 200 healthcare providers 
        across 15 states.
        
        The seed funding will support product development, regulatory compliance, and 
        expansion to new markets. The team plans to grow from 15 to 30 employees over 
        the next year.
        """,
        "metadata": {
            "title": "HealthTech Solutions Raises $3M Seed",
            "url": "https://example.com/health-seed",
            "startup_id": "health_tech",
            "round_id": "health_seed",
            "published_date": "2023-06-10T00:00:00Z"
        },
        "document_type": "announcement"
    },
    {
        "content": """
        Sequoia Capital's Investment Thesis for 2024
        
        As we enter 2024, Sequoia Capital remains focused on partnering with founders 
        who are building transformative companies. Our investment philosophy centers 
        on several key principles:
        
        1. Bold Vision: We seek founders who challenge conventional thinking and pursue 
        massive opportunities. The best companies don't just improve existing solutions 
        - they create entirely new categories.
        
        2. Product Excellence: Great companies are built on exceptional products. We 
        look for teams obsessed with product quality and user experience.
        
        3. Market Timing: The best investments combine great teams with perfect timing. 
        We analyze market dynamics to identify inflection points.
        
        Focus Areas for 2024:
        - Artificial Intelligence and Machine Learning
        - Healthcare Technology and Digital Health
        - Climate Tech and Sustainability
        - Fintech and Financial Infrastructure
        - Developer Tools and Infrastructure
        
        We typically invest across all stages from seed to growth, with check sizes 
        ranging from $1M to $100M+. Our portfolio companies receive hands-on support 
        including recruiting, go-to-market strategy, and follow-on funding.
        
        Recent investments in AI companies like TechCorp AI demonstrate our commitment 
        to supporting founders building the future of enterprise technology.
        """,
        "metadata": {
            "title": "Sequoia Capital Investment Thesis 2024",
            "url": "https://example.com/sequoia-thesis",
            "investor_id": "sequoia",
            "published_date": "2024-01-01T00:00:00Z"
        },
        "document_type": "thesis"
    }
]


async def seed_database():
    """Seed the database with sample data"""
    
    print("🌱 Starting database seeding...")
    
    # Initialize services
    mongodb = MongoDBService()
    await mongodb.connect()
    
    weaviate = WeaviateService()
    await weaviate.initialize()
    
    embedding_service = DeepSeekEmbeddingService()
    llm_service = GeminiService()
    
    rag_pipeline = RAGPipeline(
        embedding_service=embedding_service,
        vector_db=weaviate,
        mongo_db=mongodb,
        llm_service=llm_service
    )
    
    try:
        # Seed startups
        print("\n📊 Seeding startups...")
        for startup in SAMPLE_STARTUPS:
            try:
                await mongodb.create_startup(startup)
                print(f"  ✓ Created startup: {startup['name']}")
            except Exception as e:
                print(f"  ⚠️  Startup {startup['name']} might already exist: {e}")
        
        # Seed investors
        print("\n💰 Seeding investors...")
        for investor in SAMPLE_INVESTORS:
            try:
                await mongodb.create_investor(investor)
                print(f"  ✓ Created investor: {investor['name']}")
            except Exception as e:
                print(f"  ⚠️  Investor {investor['name']} might already exist: {e}")
        
        # Seed funding rounds
        print("\n💵 Seeding funding rounds...")
        for round_data in SAMPLE_FUNDING_ROUNDS:
            try:
                await mongodb.create_funding_round(round_data)
                print(f"  ✓ Created round: {round_data['round_id']}")
            except Exception as e:
                print(f"  ⚠️  Round {round_data['round_id']} might already exist: {e}")
        
        # Seed documents
        print("\n📄 Ingesting documents...")
        for doc in SAMPLE_DOCUMENTS:
            try:
                result = await rag_pipeline.ingest_document(
                    content=doc["content"],
                    metadata=doc["metadata"],
                    document_type=doc["document_type"]
                )
                print(f"  ✓ Ingested: {doc['metadata']['title']} ({result['chunks_created']} chunks)")
            except Exception as e:
                print(f"  ⚠️  Document might already exist: {e}")
        
        print("\n✅ Database seeding completed successfully!")
        print("\n📝 Summary:")
        print(f"  - Startups: {len(SAMPLE_STARTUPS)}")
        print(f"  - Investors: {len(SAMPLE_INVESTORS)}")
        print(f"  - Funding Rounds: {len(SAMPLE_FUNDING_ROUNDS)}")
        print(f"  - Documents: {len(SAMPLE_DOCUMENTS)}")
        
        print("\n🎯 Next steps:")
        print("  1. Navigate to http://localhost:3000")
        print("  2. Try searching: 'Tell me about TechCorp AI'")
        print("  3. Or: 'Which investors focus on AI startups?'")
        print("  4. Check analytics at http://localhost:3000/analytics")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        raise
    
    finally:
        await mongodb.disconnect()
        await weaviate.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
