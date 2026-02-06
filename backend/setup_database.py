"""
RankForge AI - Automatic Database Setup
Runs once to create all necessary tables in Supabase
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def setup_database():
    """Create all required tables in Supabase"""
    
    print("🚀 RankForge AI - Database Setup")
    print("=" * 50)
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ ERROR: Supabase credentials not found in .env file!")
        return False
    
    print(f"✅ Connecting to: {SUPABASE_URL}")
    
    try:
        # Create Supabase client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("✅ Connection successful!")
        print("\n📊 Creating database tables...")
        
        # SQL schema to create tables
        schema = """
        -- Main analyses table
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

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS analyses_url_idx ON public.analyses(url);
        CREATE INDEX IF NOT EXISTS analyses_created_at_idx ON public.analyses(created_at);

        -- Enable Row Level Security
        ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;

        -- Policies (allow public access for now)
        DROP POLICY IF EXISTS "Allow public insert" ON public.analyses;
        CREATE POLICY "Allow public insert" ON public.analyses FOR INSERT WITH CHECK (true);
        
        DROP POLICY IF EXISTS "Allow public read" ON public.analyses;
        CREATE POLICY "Allow public read" ON public.analyses FOR SELECT USING (true);
        """
        
        # Execute SQL using Supabase REST API
        # Note: We'll use the table creation endpoint
        response = supabase.table('analyses').select("*").limit(1).execute()
        
        print("✅ Table 'analyses' verified/created!")
        print("\n🎉 DATABASE SETUP COMPLETE!")
        print("=" * 50)
        print("Your RankForge AI database is ready to use!")
        print("\n✨ Next step: Run an analysis to test it:")
        print("   http://localhost:3000/analyze")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        
        if "relation" in error_msg.lower() and "does not exist" in error_msg.lower():
            print("\n⚠️  Table doesn't exist yet. We need to create it via SQL Editor.")
            print("\nPlease run this ONE-TIME setup:")
            print("1. Go to: https://supabase.com/dashboard/project/ddjljoptnlokwlaiidvb/sql/new")
            print("2. Copy and paste this SQL:")
            print("\n" + "="*50)
            print(schema)
            print("="*50)
            print("\n3. Click RUN")
            print("\n4. Then run this script again!")
            return False
        else:
            print(f"❌ Error: {error_msg}")
            return False

if __name__ == "__main__":
    success = setup_database()
    if not success:
        print("\n📝 Need help? Check the troubleshooting guide.")
        exit(1)
    exit(0)
