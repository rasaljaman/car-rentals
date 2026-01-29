"""
Supabase configuration and client initialization.
Handles connection to Supabase database and storage.
"""

import os
from decouple import config
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = config('SUPABASE_URL', default=None)
SUPABASE_KEY = config('SUPABASE_KEY', default=None)
SUPABASE_SERVICE_ROLE_KEY = config('SUPABASE_SERVICE_ROLE_KEY', default=None)

# Initialize Supabase client
supabase_client: Client = None

def initialize_supabase():
    """Initialize and return Supabase client."""
    global supabase_client
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables. "
            "Get them from Supabase Dashboard → Settings → API"
        )
    
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized successfully")
        return supabase_client
    except Exception as e:
        print(f"❌ Error initializing Supabase client: {str(e)}")
        raise


def get_supabase_client() -> Client:
    """Get the initialized Supabase client."""
    global supabase_client
    
    if supabase_client is None:
        supabase_client = initialize_supabase()
    
    return supabase_client


def test_supabase_connection():
    """Test Supabase connection and database access."""
    try:
        client = get_supabase_client()
        
        # Test connection by querying a table
        response = client.table('accounts_customuser').select('*').limit(1).execute()
        
        print("✅ Supabase connection successful!")
        print(f"   URL: {SUPABASE_URL}")
        print(f"   Response: {response.data if response else 'No data'}")
        
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        return False


def get_storage_client():
    """Get Supabase storage client for file uploads."""
    try:
        client = get_supabase_client()
        return client.storage
    except Exception as e:
        print(f"❌ Error getting storage client: {str(e)}")
        return None


def upload_file_to_supabase(bucket_name: str, file_path: str, file_content):
    """
    Upload file to Supabase storage.
    
    Args:
        bucket_name: Name of the storage bucket (e.g., 'car_images', 'documents')
        file_path: Path within the bucket (e.g., 'cars/car_1/image.jpg')
        file_content: File content (bytes or file-like object)
    
    Returns:
        dict: Response from Supabase with file URL
    """
    try:
        client = get_supabase_client()
        storage = client.storage
        
        # Upload file
        response = storage.from_(bucket_name).upload(file_path, file_content)
        
        # Get public URL
        public_url = storage.from_(bucket_name).get_public_url(file_path)
        
        return {
            'success': True,
            'path': file_path,
            'url': public_url,
            'response': response
        }
    except Exception as e:
        print(f"❌ Error uploading file: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def delete_file_from_supabase(bucket_name: str, file_path: str):
    """
    Delete file from Supabase storage.
    
    Args:
        bucket_name: Name of the storage bucket
        file_path: Path of the file to delete
    
    Returns:
        bool: True if successful
    """
    try:
        client = get_supabase_client()
        storage = client.storage
        
        response = storage.from_(bucket_name).remove([file_path])
        
        print(f"✅ File deleted: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error deleting file: {str(e)}")
        return False
