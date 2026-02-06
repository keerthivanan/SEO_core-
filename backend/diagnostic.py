"""
RankForge AI - Complete System Diagnostic
Checks every component: Backend, Frontend, Database, APIs
"""

import os
import sys
import requests
from supabase import create_client
from dotenv import load_dotenv

# Load environment
load_dotenv()

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_backend():
    """Check if backend is running"""
    print_header("BACKEND STATUS")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        data = response.json()
        print(f"✅ Backend: RUNNING on port 8000")
        print(f"   Status: {data.get('status', 'unknown')}")
        print(f"   Database: {data.get('database', 'unknown')}")
        print(f"   Version: {data.get('version', 'unknown')}")
        return True, data.get('database') == 'connected'
    except Exception as e:
        print(f"❌ Backend: NOT RUNNING")
        print(f"   Error: {str(e)}")
        return False, False

def check_frontend():
    """Check if frontend is running"""
    print_header("FRONTEND STATUS")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print(f"✅ Frontend: RUNNING on port 3000")
            return True
        else:
            print(f"⚠️  Frontend: Responding but status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend: NOT RUNNING")
        print(f"   Error: {str(e)}")
        return False

def check_database():
    """Check Supabase database connection and tables"""
    print_header("DATABASE STATUS")
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Credentials: NOT CONFIGURED")
        print("   SUPABASE_URL or SUPABASE_KEY missing from .env")
        return False, []
    
    print(f"✅ Credentials: CONFIGURED")
    print(f"   URL: {url}")
    
    try:
        supabase = create_client(url, key)
        print(f"✅ Connection: SUCCESS")
        
        # Try to query the analyses table
        try:
            response = supabase.table('analyses').select("id").limit(1).execute()
            print(f"✅ Table 'analyses': EXISTS")
            print(f"   Records: {len(response.data)}")
            return True, ['analyses']
        except Exception as table_error:
            error_str = str(table_error)
            if "does not exist" in error_str or "relation" in error_str:
                print(f"❌ Table 'analyses': DOES NOT EXIST")
                print(f"   This table MUST be created!")
                return True, []  # Connection works but table missing
            else:
                print(f"⚠️  Table 'analyses': ERROR")
                print(f"   {error_str}")
                return True, []
                
    except Exception as e:
        print(f"❌ Connection: FAILED")
        print(f"   Error: {str(e)}")
        return False, []

def check_api_keys():
    """Check if required API keys are configured"""
    print_header("API KEYS STATUS")
    
    keys = {
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "Serper": os.getenv("SERPER_API_KEY"),
        "Google": os.getenv("GOOGLE_API_KEY"),
    }
    
    for name, value in keys.items():
        if value and len(value) > 10:
            print(f"✅ {name}: CONFIGURED")
        else:
            print(f"⚠️  {name}: NOT CONFIGURED (analysis may be limited)")
    
    return True

def main():
    print("\n🔍 RankForge AI - Complete System Diagnostic")
    print("="*60)
    
    # Run all checks
    backend_ok, db_connected = check_backend()
    frontend_ok = check_frontend()
    db_ok, tables = check_database()
    api_ok = check_api_keys()
    
    # Final summary
    print_header("SUMMARY")
    
    issues = []
    
    if not backend_ok:
        issues.append("Backend is not running")
    if not frontend_ok:
        issues.append("Frontend is not running")
    if not db_ok:
        issues.append("Database connection failed")
    elif not tables:
        issues.append("Database tables not created")
    
    if issues:
        print("❌ PROBLEMS FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print("\n📋 FIXES NEEDED:")
        
        if not backend_ok:
            print("\n   → Start Backend:")
            print("     cd backend")
            print("     .\\venv\\Scripts\\activate")
            print("     uvicorn app.main:app --reload")
        
        if not frontend_ok:
            print("\n   → Start Frontend:")
            print("     cd frontend")
            print("     npm run dev")
        
        if db_ok and not tables:
            print("\n   → Create Database Tables:")
            print("     Run this SQL in Supabase SQL Editor:")
            print("     https://supabase.com/dashboard/project/ddjljoptnlokwlaiidvb/sql/new")
            print("\n     SQL Code:")
            print('''
     CREATE TABLE IF NOT EXISTS public.analyses (
       id TEXT PRIMARY KEY,
       user_id UUID,
       url TEXT NOT NULL,
       keyword TEXT NOT NULL,
       seo_score INTEGER DEFAULT 0,
       overall_score INTEGER DEFAULT 0,
       report_data JSONB,
       created_at TIMESTAMPTZ DEFAULT NOW()
     );
     
     CREATE INDEX IF NOT EXISTS analyses_url_idx ON public.analyses(url);
     ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;
     CREATE POLICY IF NOT EXISTS "Allow public insert" ON public.analyses FOR INSERT WITH CHECK (true);
     CREATE POLICY IF NOT EXISTS "Allow public read" ON public.analyses FOR SELECT USING (true);
            ''')
        
        return False
    else:
        print("✅ ALL SYSTEMS OPERATIONAL!")
        print("\n🚀 Your website is ready!")
        print("   Frontend: http://localhost:3000")
        print("   Backend: http://localhost:8000")
        print("   Try an analysis: http://localhost:3000/analyze")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
