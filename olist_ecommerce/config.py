from pathlib import Path
import sys
from dotenv import load_dotenv
from loguru import logger
import os

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Project Root
# --------------------------------------------------
PROJ_ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------
# Core Directories
# --------------------------------------------------
SRC_DIR = PROJ_ROOT / "olist_ecommerce"
PIPELINE_DIR = SRC_DIR / "pipeline"
MODELING_DIR = SRC_DIR / "modeling"
DB_DIR = SRC_DIR / "db"

# Pipeline Subfolders
CLEANING_DIR = PIPELINE_DIR / "cleaning"
FEATURE_DIR = PIPELINE_DIR / "feature_engineering"
INGESTION_DIR = PIPELINE_DIR / "data_ingestion"   # ✅ fixed typo

# Data
DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Models
MODELS_DIR = PROJ_ROOT / "models"

# Logs
LOGS_DIR = PROJ_ROOT / "logs"

# Reports
REPORTS_DIR = PROJ_ROOT / "reports"

# Backend (optional)
BACKEND_DIR = PROJ_ROOT / "backend"

# --------------------------------------------------
# Create Essential Directories Only
# --------------------------------------------------
for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    LOGS_DIR,
    REPORTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Validate ENV Variables (IMPORTANT)
# --------------------------------------------------
REQUIRED_ENV_VARS = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD"
]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"Missing environment variables: {missing_vars}")

# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logger.remove()

# Console Logging
try:
    from tqdm import tqdm
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    logger.add(sys.stdout, colorize=True)

# File Logging
logger.add(
    LOGS_DIR / "app_{time}.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
)

logger.success("✅ Project configuration loaded successfully")