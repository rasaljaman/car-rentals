"""
Supabase utilities for database operations.
Provides helper functions for common database operations using Supabase.
"""

from typing import List, Dict, Any, Optional
from apps.core.supabase_config import get_supabase_client
import json


class SupabaseDB:
    """Helper class for Supabase database operations."""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    # ===================== READ OPERATIONS =====================
    
    def select_all(self, table: str, limit: int = 100):
        """
        Select all records from a table.
        
        Args:
            table: Table name
            limit: Maximum number of records to return
        
        Returns:
            List of records or error dict
        """
        try:
            response = self.client.table(table).select('*').limit(limit).execute()
            return {'success': True, 'data': response.data, 'count': len(response.data)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def select_by_id(self, table: str, id_value: Any, id_column: str = 'id'):
        """
        Select a single record by ID.
        
        Args:
            table: Table name
            id_value: ID value to search for
            id_column: Column name for ID (default: 'id')
        
        Returns:
            Record or error dict
        """
        try:
            response = self.client.table(table).select('*').eq(id_column, id_value).execute()
            
            if response.data:
                return {'success': True, 'data': response.data[0]}
            else:
                return {'success': False, 'error': 'Record not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def select_where(self, table: str, filters: Dict[str, Any], limit: int = 100):
        """
        Select records with filters.
        
        Args:
            table: Table name
            filters: Dictionary of column=value pairs
            limit: Maximum number of records
        
        Returns:
            List of records or error dict
        """
        try:
            query = self.client.table(table).select('*')
            
            for column, value in filters.items():
                query = query.eq(column, value)
            
            response = query.limit(limit).execute()
            return {'success': True, 'data': response.data, 'count': len(response.data)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===================== CREATE OPERATIONS =====================
    
    def insert(self, table: str, data: Dict[str, Any]):
        """
        Insert a single record.
        
        Args:
            table: Table name
            data: Dictionary of column=value pairs
        
        Returns:
            Inserted record or error dict
        """
        try:
            response = self.client.table(table).insert(data).execute()
            return {'success': True, 'data': response.data[0] if response.data else None}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]):
        """
        Insert multiple records.
        
        Args:
            table: Table name
            data_list: List of dictionaries
        
        Returns:
            Inserted records or error dict
        """
        try:
            response = self.client.table(table).insert(data_list).execute()
            return {'success': True, 'data': response.data, 'count': len(response.data)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===================== UPDATE OPERATIONS =====================
    
    def update(self, table: str, id_value: Any, data: Dict[str, Any], id_column: str = 'id'):
        """
        Update a single record.
        
        Args:
            table: Table name
            id_value: ID value of record to update
            data: Dictionary of column=value pairs to update
            id_column: Column name for ID
        
        Returns:
            Updated record or error dict
        """
        try:
            response = self.client.table(table).update(data).eq(id_column, id_value).execute()
            return {'success': True, 'data': response.data[0] if response.data else None}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_where(self, table: str, data: Dict[str, Any], filters: Dict[str, Any]):
        """
        Update records matching filters.
        
        Args:
            table: Table name
            data: Dictionary of values to update
            filters: Dictionary of filters
        
        Returns:
            Updated records or error dict
        """
        try:
            query = self.client.table(table).update(data)
            
            for column, value in filters.items():
                query = query.eq(column, value)
            
            response = query.execute()
            return {'success': True, 'data': response.data, 'count': len(response.data)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===================== DELETE OPERATIONS =====================
    
    def delete(self, table: str, id_value: Any, id_column: str = 'id'):
        """
        Delete a single record.
        
        Args:
            table: Table name
            id_value: ID value of record to delete
            id_column: Column name for ID
        
        Returns:
            Success status or error dict
        """
        try:
            response = self.client.table(table).delete().eq(id_column, id_value).execute()
            return {'success': True, 'message': f'Record deleted successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_where(self, table: str, filters: Dict[str, Any]):
        """
        Delete records matching filters.
        
        Args:
            table: Table name
            filters: Dictionary of filters
        
        Returns:
            Success status or error dict
        """
        try:
            query = self.client.table(table).delete()
            
            for column, value in filters.items():
                query = query.eq(column, value)
            
            response = query.execute()
            return {'success': True, 'message': f'Records deleted successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ===================== AGGREGATE OPERATIONS =====================
    
    def count(self, table: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Count records in a table.
        
        Args:
            table: Table name
            filters: Optional filters
        
        Returns:
            Count result or error dict
        """
        try:
            query = self.client.table(table).select('count', count='exact')
            
            if filters:
                for column, value in filters.items():
                    query = query.eq(column, value)
            
            response = query.execute()
            return {'success': True, 'count': response.count}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Create global instance
db = SupabaseDB()


# Convenience functions
def supabase_select(table: str, limit: int = 100):
    """Select all records from table."""
    return db.select_all(table, limit)


def supabase_get(table: str, id_value: Any, id_column: str = 'id'):
    """Get single record by ID."""
    return db.select_by_id(table, id_value, id_column)


def supabase_filter(table: str, filters: Dict[str, Any], limit: int = 100):
    """Get records matching filters."""
    return db.select_where(table, filters, limit)


def supabase_insert(table: str, data: Dict[str, Any]):
    """Insert single record."""
    return db.insert(table, data)


def supabase_insert_batch(table: str, data_list: List[Dict[str, Any]]):
    """Insert multiple records."""
    return db.insert_many(table, data_list)


def supabase_update(table: str, id_value: Any, data: Dict[str, Any], id_column: str = 'id'):
    """Update single record."""
    return db.update(table, id_value, data, id_column)


def supabase_delete(table: str, id_value: Any, id_column: str = 'id'):
    """Delete single record."""
    return db.delete(table, id_value, id_column)


def supabase_count(table: str, filters: Optional[Dict[str, Any]] = None):
    """Count records in table."""
    return db.count(table, filters)
