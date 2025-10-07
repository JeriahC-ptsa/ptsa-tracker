#!/usr/bin/env python3
"""
Script to initialize PostgreSQL database with comprehensive seed data
"""
import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_postgres_db():
    """Initialize PostgreSQL database with seed data"""
    try:
        logger.info("🚀 Starting PostgreSQL database initialization...")
        
        # Add project root to path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Import app after path setup
        from wsgi import app
        from app.extensions import db
        
        with app.app_context():
            logger.info("📋 Creating database tables...")
            db.create_all()
            logger.info("✅ Database tables created successfully")
            
            # Check if data already exists
            from app.models import User, Company
            if User.query.first() is None:
                logger.info("🌱 No existing data found, running comprehensive seed...")
                try:
                    from comprehensive_seed import comprehensive_seed
                    success = comprehensive_seed()
                    if success:
                        logger.info("✅ Comprehensive seeding completed successfully!")
                    else:
                        logger.error("❌ Comprehensive seeding failed")
                        return False
                except ImportError:
                    logger.warning("No comprehensive_seed module found, creating basic admin user...")
                    from werkzeug.security import generate_password_hash
                    
                    admin = User(
                        email='info@ptsa.co.za',
                        password=generate_password_hash('info123'),
                        role='admin',
                        is_active=True
                    )
                    db.session.add(admin)
                    db.session.commit()
                    logger.info("✅ Basic admin user created")
            else:
                logger.info("ℹ️ Database already contains data, skipping seed")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_postgres_db()
    sys.exit(0 if success else 1)
