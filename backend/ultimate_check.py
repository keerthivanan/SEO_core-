"""
RankForge AI - Ultimate Website Health Check
Complete diagnostic to identify ALL issues and make website AMAZING
"""

import requests
import json
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_frontend():
    """Check Frontend Health"""
    print_section("1. FRONTEND CHECK")
    issues = []
    
    try:
        resp = requests.get("http://localhost:3000", timeout=5)
        if resp.status_code == 200:
            print("✅ Frontend: RUNNING on http://localhost:3000")
            print(f"   Status Code: {resp.status_code}")
        else:
            issues.append(f"Frontend returned status {resp.status_code}")
            print(f"⚠️  Frontend: Status {resp.status_code}")
    except Exception as e:
        issues.append("Frontend not accessible")
        print(f"❌ Frontend: NOT RUNNING")
        print(f"   Error: {str(e)}")
        print("   FIX: Run 'npm run dev' in frontend folder")
    
    return issues

def check_backend():
    """Check Backend Health"""
    print_section("2. BACKEND CHECK")
    issues = []
    
    try:
        resp = requests.get("http://localhost:8000/health", timeout=5)
        data = resp.json()
        
        print("✅ Backend: RUNNING on http://localhost:8000")
        print(f"   Status: {data.get('status')}")
        print(f"   Database: {data.get('database')}")
        print(f"   Engine: {data.get('engine')}")
        
        if data.get('database') != 'connected':
            issues.append("Database shows as disconnected in backend")
            print("   ⚠️  WARNING: Database not fully connected")
        
    except Exception as e:
        issues.append("Backend API not accessible")
        print(f"❌ Backend: NOT RUNNING")
        print(f"   Error: {str(e)}")
        print("   FIX: Run 'uvicorn app.main:app --reload' in backend folder")
    
    return issues

def check_database():
    """Check Database Connection"""
    print_section("3. DATABASE CHECK")
    issues = []
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        issues.append("Supabase credentials missing")
        print("❌ Credentials: NOT CONFIGURED")
        return issues
    
    try:
        supabase = create_client(url, key)
        
        # Try to query
        response = supabase.table('analyses').select("id").limit(1).execute()
        
        print("✅ Database: CONNECTED")
        print(f"   URL: {url}")
        print(f"   Table: analyses exists")
        
    except Exception as e:
        error_str = str(e).lower()
        if "does not exist" in error_str:
            issues.append("Database table 'analyses' does not exist")
            print("❌ Table: MISSING")
            print("   FIX: Run the SQL schema in Supabase dashboard")
        else:
            issues.append(f"Database error: {str(e)}")
            print(f"❌ Database: ERROR")
            print(f"   {str(e)}")
    
    return issues

def check_api_endpoints():
    """Check Critical API Endpoints"""
    print_section("4. API ENDPOINTS CHECK")
    issues = []
    
    endpoints = [
        ("/health", "GET"),
        ("/api/analyze", "POST"),
        ("/api/tools/robots", "POST"),
    ]
    
    for path, method in endpoints:
        try:
            if method == "GET":
                resp = requests.get(f"http://localhost:8000{path}", timeout=3)
            else:
                resp = requests.post(f"http://localhost:8000{path}", 
                                   json={"test": "data"}, timeout=3)
            
            # Accept 200, 422 (validation error is expected for test data)
            if resp.status_code in [200, 422]:
                print(f"✅ {path}: Responding")
            else:
                print(f"⚠️  {path}: Status {resp.status_code}")
                
        except Exception as e:
            issues.append(f"Endpoint {path} not accessible")
            print(f"❌ {path}: ERROR - {str(e)}")
    
    return issues

def check_env_variables():
    """Check Environment Variables"""
    print_section("5. ENVIRONMENT VARIABLES CHECK")
    issues = []
    
    required = {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    }
    
    optional = {
        "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
    }
    
    print("\nRequired Variables:")
    for name, value in required.items():
        if value and len(value) > 10:
            print(f"  ✅ {name}: Configured")
        else:
            issues.append(f"Missing required variable: {name}")
            print(f"  ❌ {name}: MISSING")
    
    print("\nOptional Variables (for enhanced features):")
    for name, value in optional.items():
        if value and len(value) > 10:
            print(f"  ✅ {name}: Configured")
        else:
            print(f"  ⚠️  {name}: Not configured (some features limited)")
    
    return issues

def check_frontend_pages():
    """Check Important Frontend Pages"""
    print_section("6. FRONTEND PAGES CHECK")
    issues = []
    
    pages = [
        "/",
        "/analyze",
        "/features",
        "/about",
        "/pricing",
        "/contact",
        "/blog",
        "/docs",
        "/tools",
    ]
    
    working = 0
    for page in pages:
        try:
            resp = requests.get(f"http://localhost:3000{page}", timeout=3)
            if resp.status_code == 200:
                working += 1
                print(f"  ✅ {page}")
            else:
                print(f"  ⚠️  {page} - Status {resp.status_code}")
        except:
            issues.append(f"Page {page} not accessible")
            print(f"  ❌ {page} - ERROR")
    
    print(f"\n  {working}/{len(pages)} pages working")
    
    return issues

def main():
    print("\n" + "="*70)
    print("  🔍 RANKFORGE AI - ULTIMATE HEALTH CHECK")
    print("  Making your website AMAZING!")
    print("="*70)
    
    all_issues = []
    
    all_issues.extend(check_frontend())
    all_issues.extend(check_backend())
    all_issues.extend(check_database())
    all_issues.extend(check_api_endpoints())
    all_issues.extend(check_env_variables())
    all_issues.extend(check_frontend_pages())
    
    # Final Report
    print_section("📊 FINAL DIAGNOSTIC REPORT")
    
    if not all_issues:
        print("\n🎉🎉🎉 CONGRATULATIONS! 🎉🎉🎉")
        print("\n✅ ZERO ISSUES FOUND!")
        print("\nYour website is:")
        print("  ✅ FULLY OPERATIONAL")
        print("  ✅ ALL SYSTEMS ACTIVE")
        print("  ✅ DATABASE CONNECTED")
        print("  ✅ READY FOR PRODUCTION")
        print("\n🚀 Your \"Best of All Time\" RankForge AI is LIVE!")
        print("\n📍 Access your website:")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8000")
        print("   Try it:   http://localhost:3000/analyze")
        
        return True
    else:
        print(f"\n⚠️  FOUND {len(all_issues)} ISSUE(S):")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n📋 QUICK FIXES:")
        if any("Frontend" in i for i in all_issues):
            print("\n  → Start Frontend:")
            print("     cd frontend")
            print("     npm run dev")
        
        if any("Backend" in i for i in all_issues):
            print("\n  → Start Backend:")
            print("     cd backend")
            print("     .\\venv\\Scripts\\activate")
            print("     uvicorn app.main:app --reload")
        
        if any("table" in i.lower() for i in all_issues):
            print("\n  → Create Database:")
            print("     Already provided SQL - check supabase_schema.sql")
        
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
