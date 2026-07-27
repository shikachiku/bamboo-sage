from pathlib import Path

# =====================================================
# Project
# =====================================================

PROJECT_PATH = Path(__file__).resolve().parent

# =====================================================
# Google Drive
# =====================================================

GOOGLE_DRIVE = Path("/mnt/chromeos/shared/GoogleDrive/MyDrive")

# =====================================================
# Bamboo Sage
# =====================================================

BAMBOO_ROOT = GOOGLE_DRIVE / "BambooSage"

# =====================================================
# Data
# =====================================================

DATA_PATH = BAMBOO_ROOT / "data"

# 標準フォルダ名

RAW_DIR = "raw"

INDICATOR_DIR = "indicator"

# =====================================================
# Backup / Logs
# =====================================================

BACKUP_PATH = BAMBOO_ROOT / "backup"

LOG_PATH = BAMBOO_ROOT / "logs"

EXPORT_PATH = BAMBOO_ROOT / "export"