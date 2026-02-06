import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    """Connect to PostgreSQL and create all required tables"""
    
    print("🚀 RankForge AI - Direct Database Setup")
    print("="*60)
    
    try:
        # Connect to PostgreSQL
        print("📡 Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Connection successful!")
        print("\n📊 Creating tables...")
        
        # SQL to create all tables
        schema_sql = """
        -- Main analyses table
        CREATE TABLE IF NOT EXISTS public.analyses (
          id TEXT PRIMARY KEY,
          user_id TEXT, -- Use TEXT to support both UUIDs and 'guest' strings
          url TEXT NOT NULL,
          keyword TEXT NOT NULL,
          seo_score INTEGER DEFAULT 0,
          overall_score INTEGER DEFAULT 0,
          report_data JSONB,
          created_at TIMESTAMPTZ DEFAULT NOW()
        );

        -- Migration: Fix column type if it already exists as UUID
        DO $$ 
        BEGIN 
            IF (SELECT data_type FROM information_schema.columns WHERE table_name = 'analyses' AND column_name = 'user_id') = 'uuid' THEN
                ALTER TABLE public.analyses ALTER COLUMN user_id TYPE TEXT;
            END IF;
        END $$;

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS analyses_url_idx ON public.analyses(url);
        CREATE INDEX IF NOT EXISTS analyses_created_at_idx ON public.analyses(created_at);
        CREATE INDEX IF NOT EXISTS analyses_user_id_idx ON public.analyses(user_id);

        -- Enable Row Level Security
        ALTER TABLE public.analyses ENABLE ROW LEVEL SECURITY;

        -- Drop existing policies if they exist
        DROP POLICY IF EXISTS "Allow public insert" ON public.analyses;
        DROP POLICY IF EXISTS "Allow public read" ON public.analyses;
        DROP POLICY IF EXISTS "Users can only insert their own data" ON public.analyses;
        DROP POLICY IF EXISTS "Users can only read their own data" ON public.analyses;
        DROP POLICY IF EXISTS "Users can only update their own data" ON public.analyses;
        
        -- Create new strict multi-tenant policies
        CREATE POLICY "Users can only insert their own data" ON public.analyses 
        FOR INSERT WITH CHECK (auth.uid()::text = user_id OR user_id = 'guest');
        
        CREATE POLICY "Users can only read their own data" ON public.analyses 
        FOR SELECT USING (auth.uid()::text = user_id OR user_id = 'guest');

        CREATE POLICY "Users can only update their own data" ON public.analyses 
        FOR UPDATE USING (auth.uid()::text = user_id);
        """
        
        # Execute the schema
        cursor.execute(schema_sql)
        
        print("✅ Table 'analyses' created successfully!")
        print("✅ Indexes created!")
        print("✅ Row Level Security enabled!")
        print("✅ Policies configured!")
        
        # Verify table exists
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'analyses'
        """)
        
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("\n✅ VERIFICATION: Table 'analyses' confirmed in database!")
            
            # Check if any records exist
            cursor.execute("SELECT COUNT(*) FROM public.analyses")
            record_count = cursor.fetchone()[0]
            print(f"   Current records: {record_count}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("🎉 DATABASE SETUP COMPLETE!")
        print("="*60)
        print("\n✅ Your RankForge AI database is now ready!")
        print("\n🚀 Next Steps:")
        print("   1. Restart your backend: uvicorn app.main:app --reload")
        print("   2. Visit: http://localhost:3000/analyze")
        print("   3. Run your first SEO analysis!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nThis could mean:")
        print("  - Password might be incorrect")
        print("  - Database connection string format issue")
        print("  - Network/firewall blocking connection")
        return False

if __name__ == "__main__":
    success = create_tables()
    exit(0 if success else 1)
