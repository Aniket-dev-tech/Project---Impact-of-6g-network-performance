"""
Deployment Guide & System Information
6G Network Performance Manufacturing Analytics Platform
"""

DEPLOYMENT_GUIDE = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         DEPLOYMENT GUIDE                                      ║
║   6G Network Performance Manufacturing Analytics Platform                    ║
║   Production-Ready Installation & Deployment Instructions                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. LOCAL DEVELOPMENT SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIREMENTS:
• Python 3.8 or higher
• pip (Python package manager)
• 2GB RAM minimum (4GB recommended)
• 500MB disk space for dependencies

INSTALLATION STEPS:

Step 1: Clone/Download Project
───────────────────────────────
$ cd "Impact of 6G Network Performance on Manufacturing Efficiency in Smart Factories"

Step 2: Create Virtual Environment
──────────────────────────────────────
# Windows
$ python -m venv venv
$ venv\\Scripts\\activate

# macOS/Linux
$ python3 -m venv venv
$ source venv/bin/activate

Step 3: Install Dependencies
──────────────────────────────
$ pip install -r requirements.txt

# List installed packages
$ pip list

Step 4: Verify Installation
─────────────────────────────
$ python -c "import streamlit; import pandas; import plotly; print('\\n✓ All dependencies installed successfully!')"

Step 5: Run Application
─────────────────────────
$ streamlit run app.py

# Application will open at: http://localhost:8501


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. DOCKER DEPLOYMENT (Recommended for Production)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create Dockerfile:
──────────────────
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.headless", "true"]


Build & Run Container:
──────────────────────
$ docker build -t 6g-manufacturing-analytics .
$ docker run -p 8501:8501 -v $(pwd)/:/app 6g-manufacturing-analytics


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. CLOUD DEPLOYMENT (AWS/Azure/GCP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STREAMLIT CLOUD (Simplest Option):
──────────────────────────────────

1. Push code to GitHub repository
2. Go to share.streamlit.io
3. Connect your GitHub account
4. Select repository and branch
5. Platform automatically deploys and provides public URL
6. Logs and monitoring available in dashboard

Example URL: https://your-username-repo-app-xxxxx.streamlit.app


HEROKU DEPLOYMENT:
──────────────────

1. Create Procfile:
   web: streamlit run app.py --server.port=$PORT --server.headless true

2. Create runtime.txt:
   python-3.10.13

3. Deploy:
   $ heroku create your-app-name
   $ git push heroku main


AWS EC2 DEPLOYMENT:
───────────────────

1. Launch Ubuntu 20.04 LTS instance
2. Install Python and dependencies
3. Clone repository
4. Create systemd service file
5. Configure nginx reverse proxy
6. Set up SSL certificate (Let's Encrypt)
7. Configure security groups


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. PERFORMANCE OPTIMIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Caching Strategies:
───────────────────
• @st.cache_resource: Cache heavy data loading (data processor, KPI calculator)
• @st.cache_data: Cache visualization data
• Session state for user interactions

Load Testing Metrics:
─────────────────────
• Dashboard load time: <3 seconds (optimized)
• Concurrent users supported: 10-20 (local machine)
• Memory usage: ~400-500MB base + 50MB per user
• Network: 1-2 Mbps bandwidth per user

Optimization Checklist:
──────────────────────
☐ Enable Streamlit caching (st.cache_resource, st.cache_data)
☐ Use CDN for static assets
☐ Enable gzip compression
☐ Optimize image sizes
☐ Minimize re-runs with session state
☐ Use connection pooling for databases
☐ Enable read-only access for production


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. MAINTENANCE & MONITORING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Health Checks:
──────────────
• Data availability: Verify CSV file exists and is readable
• Dependency versions: pip check --quiet
• Database connections: Test connectivity if using external databases
• Uptime monitoring: Ping application endpoint every 5 minutes

Logging Setup:
──────────────
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

Log Rotation:
─────────────
# Use logrotate on Linux
/var/log/app/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. SECURITY CONSIDERATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Authentication & Authorization:
────────────────────────────────
• For Streamlit Cloud: Built-in OAuth support
• For self-hosted: Implement authentication layer
  - Option 1: nginx with Apache auth
  - Option 2: Streamlit-authenticator library
  - Option 3: OAuth2 proxy

Data Security:
───────────────
• Encrypt sensitive data at rest
• Use HTTPS/TLS for all connections (port 443)
• Implement API rate limiting
• Regular security audits
• NIST/ISO compliance for manufacturing data

Environment Variables:
──────────────────────
# .env file (add to .gitignore)
DATABASE_URL=postgresql://user:pass@host:5432/db
API_KEY=your-api-key
SECRET_KEY=your-secret-key

# Load in app:
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL')


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: CSV file not found
────────────────────────
Solution:
$ verify file exists: ls -la Thales_Group_Manufacturing.csv
$ Check path: Adjust in data_preprocessing.py if needed
$ Ensure permissions: chmod 644 Thales_Group_Manufacturing.csv


Issue: Import errors (module not found)
──────────────────────────────────────
Solution:
$ pip install --upgrade pip
$ pip install -r requirements.txt --force-reinstall
$ python -m pip check


Issue: Out of memory
────────────────────
Solution:
$ Increase available RAM
$ Use data chunking for large datasets
$ Implement database backend instead of CSV
$ Clear app cache: rm -rf .streamlit/cache/


Issue: Slow performance
──────────────────────
Solution:
$ Monitor with: htop
$ Profile code: python -m cProfile app.py
$ Cache expensive operations
$ Optimize SQL queries if using database


Issue: Port already in use
──────────────────────────
Solution:
$ Change port: streamlit run app.py --server.port 8502
$ Kill existing process: lsof -i :8501 | grep -v PID | awk '{print $2}' | xargs kill -9


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. BACKUP & DISASTER RECOVERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backup Strategy:
─────────────────
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/manufacturing-analytics"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf "$BACKUP_DIR/backup_$TIMESTAMP.tar.gz" \\
    Thales_Group_Manufacturing.csv \\
    *.py \\
    requirements.txt

# Keep last 30 days
find "$BACKUP_DIR" -type f -mtime +30 -delete

# Execute daily via cron
0 2 * * * /path/to/backup_script.sh


Recovery Procedure:
───────────────────
1. Stop application
2. Restore from backup: tar -xzf backup_*.tar.gz
3. Verify data integrity
4. Restart application
5. Validate dashboard functionality


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. SCALING STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Horizontal Scaling:
──────────────────
• Load balancer (nginx, HAProxy)
• Multiple app instances
• Shared data store (database)
• Session state management

Vertical Scaling:
─────────────────
• Increase server resources
• Optimize database queries
• Implement caching layer (Redis)
• Use connection pooling

Database Migration:
───────────────────
For large datasets, move from CSV to database:

from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost/manufacturing')
df.to_sql('manufacturing_data', engine, if_exists='replace', index=False)

# In app.py
con = engine.connect()
df = pd.read_sql('SELECT * FROM manufacturing_data', con)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. COMPLIANCE & DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Required Documentation:
───────────────────────
☐ System architecture diagram
☐ Data flow documentation
☐ API specifications
☐ Security policy
☐ Disaster recovery plan
☐ User manual
☐ Administrator guide

Compliance Checklist:
─────────────────────
☐ GDPR compliance (if EU data)
☐ ISO/IEC 27001 (information security)
☐ ISO/IEC 27035 (incident management)
☐ Manufacturing data standards (MES/ISA-95)
☐ Audit trail implementation
☐ Data retention policy


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUPPORT & RESOURCES:
- Streamlit Documentation: https://docs.streamlit.io
- Plotly Documentation: https://plotly.com/python/
- Python Official Docs: https://docs.python.org/
- Thales Group: https://www.thalesgroup.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

if __name__ == "__main__":
    print(DEPLOYMENT_GUIDE)
