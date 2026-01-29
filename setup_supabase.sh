#!/bin/bash
# Supabase Integration Setup Script
# Run this to install dependencies and set up Supabase connection

set -e

echo "════════════════════════════════════════════════════════════"
echo "🚀 SUPABASE INTEGRATION SETUP"
echo "════════════════════════════════════════════════════════════"
echo ""

# Step 1: Install dependencies
echo "📦 Step 1: Installing Python dependencies..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Step 2: Check environment variables
echo "🔍 Step 2: Checking Supabase credentials in .env..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if grep -q "SUPABASE_URL=" .env && grep -q "SUPABASE_KEY=" .env; then
    echo "✅ Supabase credentials found in .env"
else
    echo "❌ Supabase credentials not found!"
    echo ""
    echo "Add these to your .env file:"
    echo "  SUPABASE_URL=https://your-project.supabase.co"
    echo "  SUPABASE_KEY=your-anon-public-key"
    echo ""
    echo "Get credentials from: https://supabase.com/dashboard → Settings → API"
    exit 1
fi
echo ""

# Step 3: Run migrations
echo "🗄️  Step 3: Running database migrations..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python manage.py migrate
echo "✅ Migrations completed"
echo ""

# Step 4: Initialize Supabase
echo "⚙️  Step 4: Initializing Supabase connection..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python manage.py shell << END
from apps.core.supabase_init import initialize_supabase_db
initialize_supabase_db()
END
echo ""

# Step 5: Summary
echo "════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📝 Next Steps:"
echo "  1. Create superuser:"
echo "     python manage.py createsuperuser"
echo ""
echo "  2. Create storage buckets in Supabase Dashboard:"
echo "     - car-images (public)"
echo "     - car-documents (private)"
echo "     - user-documents (private)"
echo ""
echo "  3. Set up RLS policies (see SUPABASE_SETUP.md)"
echo ""
echo "  4. Start development server:"
echo "     python manage.py runserver"
echo ""
echo "🌐 Access admin at: http://localhost:8000/admin/"
echo ""
