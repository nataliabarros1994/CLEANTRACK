#!/bin/bash
#
# CleanTrack Production Deployment Script
# =========================================
# Run this script on your production server to deploy/update CleanTrack
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}CleanTrack Production Deployment${NC}"
echo -e "${GREEN}========================================${NC}"

# Configuration
PROJECT_DIR="/opt/cleantrack"
USER="cleantrack"
GROUP="cleantrack"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}" 
   exit 1
fi

# Navigate to project directory
cd $PROJECT_DIR

echo -e "${YELLOW}[1/8] Pulling latest code from Git...${NC}"
sudo -u $USER git pull origin main

echo -e "${YELLOW}[2/8] Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}[3/8] Installing/updating dependencies...${NC}"
pip install -r requirements.txt --upgrade

echo -e "${YELLOW}[4/8] Running database migrations...${NC}"
python manage.py migrate --settings=cleantrack.settings_production

echo -e "${YELLOW}[5/8] Collecting static files...${NC}"
python manage.py collectstatic --noinput --settings=cleantrack.settings_production

echo -e "${YELLOW}[6/8] Clearing expired sessions...${NC}"
python manage.py clearsessions --settings=cleantrack.settings_production

echo -e "${YELLOW}[7/8] Restarting CleanTrack service...${NC}"
systemctl restart cleantrack

echo -e "${YELLOW}[8/8] Reloading Nginx...${NC}"
systemctl reload nginx

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Service status:"
systemctl status cleantrack --no-pager -l

echo ""
echo -e "${GREEN}CleanTrack is now live!${NC}"
