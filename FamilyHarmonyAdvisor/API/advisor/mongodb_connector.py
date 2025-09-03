# # mongodb_connector.py
# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv

# load_dotenv()

# class MongoDBConnector:
#     _instance = None
#     _client = None
#     _db = None
    
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(MongoDBConnector, cls).__new__(cls)
#             cls._instance._initialize_connection()
#         return cls._instance
    
#     def _initialize_connection(self):
#         try:
#             MONGODB_URI = os.environ.get(
#                 'MONGODB_ATLAS_CLUSTER', 
#                 'mongodb+srv://indeewara5678_db_user:o0uF2qjVFB3JTN1k@cluster0.lkgjgsq.mongodb.net/'
#             )
            
#             self._client = MongoClient(MONGODB_URI)
#             # Test the connection
#             self._client.admin.command('ping')
#             self._db = self._client['FamilyHarmonyDB']
#             print("✓ MongoDB connection successful!")
#         except Exception as e:
#             print(f"✗ MongoDB connection failed: {e}")
#             self._client = None
#             self._db = None
    
#     def get_database(self):
#         return self._db
    
#     def get_client(self):
#         return self._client
    
#     def close_connection(self):
#         if self._client:
#             self._client.close()
#             self._client = None
#             self._db = None

# # Global instance
# mongodb_connector = MongoDBConnector()