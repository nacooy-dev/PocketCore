"""
内存管理模块
"""
import sqlite3
import json
from typing import Dict, Any, List
from datetime import datetime
from config import Config

class MemoryManager:
    """内存管理器"""
    
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or Config.DATABASE_URL.replace("sqlite:///", "")
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建交互历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建上下文表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_interaction(self, query: str, response: str):
        """保存交互历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions (query, response)
            VALUES (?, ?)
        ''', (query, response))
        
        conn.commit()
        conn.close()
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的交互历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT query, response, timestamp
            FROM interactions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "query": row[0],
                "response": row[1],
                "timestamp": row[2]
            }
            for row in results
        ]
    
    def save_context(self, key: str, value: Any):
        """保存上下文"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 将值转换为JSON字符串存储
        value_str = json.dumps(value, ensure_ascii=False)
        
        cursor.execute('''
            INSERT OR REPLACE INTO context (key, value)
            VALUES (?, ?)
        ''', (key, value_str))
        
        conn.commit()
        conn.close()
    
    def get_context(self, key: str) -> Any:
        """获取上下文"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT value
            FROM context
            WHERE key = ?
        ''', (key,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            try:
                return json.loads(result[0])
            except json.JSONDecodeError:
                return result[0]
        return None
    
    def get_all_context(self) -> Dict[str, Any]:
        """获取所有上下文"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value FROM context')
        results = cursor.fetchall()
        conn.close()
        
        context = {}
        for key, value_str in results:
            try:
                context[key] = json.loads(value_str)
            except json.JSONDecodeError:
                context[key] = value_str
        
        return context
    
    def clear_memory(self):
        """清空内存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM interactions')
        cursor.execute('DELETE FROM context')
        
        conn.commit()
        conn.close()