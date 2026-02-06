"""
RankForge AI - Database Perfect Working Test
Performs comprehensive database verification:
1. Connection test
2. Write test (insert data)
3. Read test (query data)
4. Backend health check
"""

import psycopg2
from supabase import create_client
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environmental variables
load_dotenv()

# SUPABASE SETTINGS
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# PostgreSQL Direct settings
PG_URL = os.getenv("DATABASE_URL")

def test_postgresql_connection():
    """Test 1: Direct PostgreSQL Connection"""
    print("\n" + "="*60)
    print("TEST 1: PostgreSQL Direct Connection")
    print("="*60)
    
    try:
        conn = psycopg2.connect(PG_URL)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print("✅ PostgreSQL Connection: SUCCESS")
        print(f"   Database: {version[0][:50]}...")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ PostgreSQL Connection: FAILED")
        print(f"   Error: {str(e)}")
        return False

def test_table_exists():
    """Test 2: Verify Table Exists"""
    print("\n" + "="*60)
    print("TEST 2: Table Existence Check")
    print("="*60)
    
    try:
        conn = psycopg2.connect(PG_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = 'analyses'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        if columns:
            print("✅ Table 'analyses': EXISTS")
            print(f"   Columns: {len(columns)}")
            for col in columns:
                print(f"     - {col[1]} ({col[2]})")
        else:
            print("❌ Table 'analyses': NOT FOUND")
            return False
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Table Check: FAILED")
        print(f"   Error: {str(e)}")
        return False

def test_write_operation():
    """Test 3: Write Data (INSERT)"""
    print("\n" + "="*60)
    print("TEST 3: Data Write Test")
    print("="*60)
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        test_data = {
            "id": "test_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
            "url": "https://example.com",
            "keyword": "test keyword",
            "seo_score": 85,
            "overall_score": 90,
            "report_data": {"test": True, "message": "Database verification test"}
        }
        
        response = supabase.table('analyses').insert(test_data).execute()
        
        print("✅ Data INSERT: SUCCESS")
        print(f"   Test Record ID: {test_data['id']}")
        return True, test_data['id']
    except Exception as e:
        print(f"❌ Data INSERT: FAILED")
        print(f"   Error: {str(e)}")
        return False, None

def test_read_operation(test_id):
    """Test 4: Read Data (SELECT)"""
    print("\n" + "="*60)
    print("TEST 4: Data Read Test")
    print("="*60)
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        response = supabase.table('analyses').select("*").eq('id', test_id).execute()
        
        if response.data and len(response.data) > 0:
            record = response.data[0]
            print("✅ Data SELECT: SUCCESS")
            print(f"   Retrieved Record:")
            print(f"     - ID: {record['id']}")
            print(f"     - URL: {record['url']}")
            print(f"     - SEO Score: {record['seo_score']}")
            return True
        else:
            print("❌ Data SELECT: NO DATA FOUND")
            return False
    except Exception as e:
        print(f"❌ Data SELECT: FAILED")
        print(f"   Error: {str(e)}")
        return False

def test_backend_health():
    """Test 5: Backend Health Check"""
    print("\n" + "="*60)
    print("TEST 5: Backend Health Endpoint")
    print("="*60)
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        data = response.json()
        
        print("✅ Backend Health Check: SUCCESS")
        print(f"   Status: {data.get('status')}")
        print(f"   Database: {data.get('database')}")
        print(f"   Engine: {data.get('engine')}")
        
        if data.get('database') == 'connected':
            print("\n   🎉 Database shows as CONNECTED in backend!")
            return True
        else:
            print("\n   ⚠️  Database shows as disconnected in backend")
            return False
    except Exception as e:
        print(f"⚠️  Backend Health Check: Backend not running")
        print(f"   Start with: uvicorn app.main:app --reload")
        return False

def main():
    print("\n🔬 RankForge AI - PERFECT WORKING DATABASE TEST")
    print("="*60)
    print("Running 5 comprehensive tests...")
    
    results = []
    
    # Test 1: Connection
    results.append(("PostgreSQL Connection", test_postgresql_connection()))
    
    # Test 2: Table Structure
    results.append(("Table Structure", test_table_exists()))
    
    # Test 3 & 4: Write and Read
    write_ok, test_id = test_write_operation()
    results.append(("Data Write", write_ok))
    
    if write_ok and test_id:
        read_ok = test_read_operation(test_id)
        results.append(("Data Read", read_ok))
    else:
        results.append(("Data Read", False))
    
    # Test 5: Backend
    results.append(("Backend Health", test_backend_health()))
    
    # Final Report
    print("\n" + "="*60)
    print("📊 FINAL VERIFICATION REPORT")
    print("="*60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("\n✅ Your database is PERFECTLY WORKING!")
        print("\n🚀 Ready to use:")
        print("   - Frontend: http://localhost:3000")
        print("   - Backend: http://localhost:8000")
        print("   - Try analysis: http://localhost:3000/analyze")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("="*60)
        print("\nCheck the errors above for details.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
