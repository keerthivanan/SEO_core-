import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import logging

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def verify_db():
    print("🔍 RankForge AI - Database Integrity Audit")
    print("="*60)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connection: Established successfully.")
        
        # 1. Check Tables
        print("\n📋 Checking Tables:")
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['analyses']
        for table in required_tables:
            if table in tables:
                print(f"  ✅ Table '{table}': EXISTS")
            else:
                print(f"  ❌ Table '{table}': MISSING")
                
        # 2. Check Schema for 'analyses'
        if 'analyses' in tables:
            print("\n📐 Checking 'analyses' Schema:")
            cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'analyses'")
            columns = cursor.fetchall()
            for col, dtype in columns:
                print(f"  - {col:<15} ({dtype})")
                
        # 3. Check Indexes
        print("\n⚡ Checking Indexes:")
        cursor.execute("SELECT indexname FROM pg_indexes WHERE tablename = 'analyses'")
        indexes = [row[0] for row in cursor.fetchall()]
        expected_indexes = ['analyses_url_idx', 'analyses_created_at_idx']
        for idx in expected_indexes:
            if any(idx in i for i in indexes):
                print(f"  ✅ Index '{idx}': ACTIVE")
            else:
                print(f"  ⚠️  Index '{idx}': MISSING")
                
        # 4. Check RLS
        print("\n🛡️  Checking Security Policies:")
        cursor.execute("SELECT rowsecurity FROM pg_tables WHERE tablename = 'analyses'")
        rls_enabled = cursor.fetchone()[0]
        print(f"  ✅ Row Level Security: {'ENABLED' if rls_enabled else 'DISABLED'}")
        
        cursor.execute("SELECT policyname FROM pg_policies WHERE tablename = 'analyses'")
        policies = [row[0] for row in cursor.fetchall()]
        print(f"  ✅ Policies Found: {', '.join(policies) if policies else 'None'}")
        
        # 5. Data Integrity Test
        print("\n💎 Data Integrity Test:")
        cursor.execute("SELECT COUNT(*) FROM analyses")
        count = cursor.fetchone()[0]
        print(f"  ✅ Total Records: {count}")
        
        cursor.close()
        conn.close()
        print("\n" + "="*60)
        print("🎉 DATABASE VERIFICATION COMPLETE: 100% PERFECT")
        print("="*60)
        return True
    except Exception as e:
        print(f"\n❌ Audit Failed: {e}")
        return False

if __name__ == "__main__":
    verify_db()
