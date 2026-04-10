import sqlite3
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import pandas as pd
from backend.models.models import Listing
import os

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('roommate.db')
        self.create_tables()
        try:
            openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-ada-002"
            )
            self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
            self.collection = self.chroma_client.get_or_create_collection(
                name="listings_openai",
                embedding_function=openai_ef
            )
            self.chroma_available = True
        except Exception as e:
            print(f"ChromaDB initialization failed: {e}. Continuing without vector search.")
            self.chroma_available = False

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY,
                location TEXT,
                rent INTEGER,
                deposit INTEGER,
                num_roommates INTEGER,
                vacancy_count INTEGER,
                lifestyle_tags TEXT,
                contact_info TEXT,
                urgency TEXT,
                trust_score INTEGER,
                description TEXT
            )
        ''')
        self.conn.commit()

    def load_mock_data(self):
        # Check if data already loaded
        cursor = self.conn.execute('SELECT COUNT(*) FROM listings')
        if cursor.fetchone()[0] > 0:
            return  # Already loaded
        
        df = pd.read_csv('data/mock_listings.csv')
        documents = []
        metadatas = []
        ids = []
        for _, row in df.iterrows():
            listing = Listing(**row.to_dict())
            # Insert into SQLite
            self.conn.execute('''
                INSERT INTO listings (id, location, rent, deposit, num_roommates, vacancy_count, lifestyle_tags, contact_info, urgency, trust_score, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (listing.id, listing.location, listing.rent, listing.deposit, listing.num_roommates, listing.vacancy_count, listing.lifestyle_tags, listing.contact_info, listing.urgency, listing.trust_score, listing.description))
            documents.append(listing.description)
            metadatas.append({
                "id": listing.id,
                "location": listing.location,
                "rent": listing.rent,
                "deposit": listing.deposit,
                "num_roommates": listing.num_roommates,
                "vacancy_count": listing.vacancy_count,
                "lifestyle_tags": listing.lifestyle_tags,
                "contact_info": listing.contact_info,
                "urgency": listing.urgency,
                "trust_score": listing.trust_score
            })
            ids.append(str(listing.id))
        self.conn.commit()
        
        # Load into ChromaDB if available
        if self.chroma_available:
            try:
                if not self.collection.count():
                    self.collection.add(
                        documents=documents,
                        metadatas=metadatas,
                        ids=ids
                    )
            except Exception as e:
                print(f"Warning: Could not load data into ChromaDB: {e}")
                self.chroma_available = False

    def get_all_listings(self):
        cursor = self.conn.execute('SELECT * FROM listings')
        rows = cursor.fetchall()
        return [Listing(**dict(zip([col[0] for col in cursor.description], row))) for row in rows]

    def add_listing(self, listing: Listing):
        self.conn.execute('''
            INSERT INTO listings (id, location, rent, deposit, num_roommates, vacancy_count, lifestyle_tags, contact_info, urgency, trust_score, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (listing.id, listing.location, listing.rent, listing.deposit, listing.num_roommates, listing.vacancy_count, listing.lifestyle_tags, listing.contact_info, listing.urgency, listing.trust_score, listing.description))
        self.conn.commit()
        # Add to ChromaDB
        self.collection.add(
            documents=[listing.description],
            metadatas=[{
                "id": listing.id,
                "location": listing.location,
                "rent": listing.rent,
                "deposit": listing.deposit,
                "num_roommates": listing.num_roommates,
                "vacancy_count": listing.vacancy_count,
                "lifestyle_tags": listing.lifestyle_tags,
                "contact_info": listing.contact_info,
                "urgency": listing.urgency,
                "trust_score": listing.trust_score
            }],
            ids=[str(listing.id)]
        )

db = Database()