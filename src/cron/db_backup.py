"""
Script intended to be ran as a cron job to backup the database.
"""

import os
import datetime
from dotenv import load_dotenv
load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
BACKUP_DIR = os.getenv("DB_BACKUP_DIR")
MAX_BACKUPS = os.getenv("DB_MAX_BACKUPS")

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_backup_{TIMESTAMP}.sql")


backup_command = f"mysqldump --user={DB_USER} --password={DB_PASSWORD} {DB_NAME} > {backup_file}"
os.system(backup_command)


while len(os.listdir(BACKUP_DIR)) > MAX_BACKUPS:
    """
    Removes the oldest backup file while the number of backups exceeds the maximum.
    """
    oldest_backup = min(os.listdir(BACKUP_DIR))
    os.remove(os.path.join(BACKUP_DIR, oldest_backup))
