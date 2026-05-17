from pathlib import Path
import sys
from loguru import logger

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
PROJ_ROOT = Path(__file__).resolve().parents[1]

# --------------------------------------------------
# CORE DIRECTORIES
# --------------------------------------------------
SRC_DIR = PROJ_ROOT / "olist_ecommerce"

PIPELINE_DIR = SRC_DIR / "pipeline"
MODELING_DIR = SRC_DIR / "modeling"
DB_DIR = SRC_DIR / "db"

# --------------------------------------------------
# PIPELINE SUBFOLDERS
# --------------------------------------------------
CLEANING_DIR = PIPELINE_DIR / "cleaning"

FEATURE_DIR = PIPELINE_DIR / "feature_engineering"

INGESTION_DIR = PIPELINE_DIR / "data_ingestion"

# --------------------------------------------------
# DATA DIRECTORIES
# --------------------------------------------------
DATA_DIR = PROJ_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

# --------------------------------------------------
# MODELS
# --------------------------------------------------
MODELS_DIR = PROJ_ROOT / "models"

# --------------------------------------------------
# LOGS
# --------------------------------------------------
LOGS_DIR = PROJ_ROOT / "logs"

# --------------------------------------------------
# REPORTS
# --------------------------------------------------
REPORTS_DIR = PROJ_ROOT / "reports"

# --------------------------------------------------
# OPTIONAL BACKEND
# --------------------------------------------------
BACKEND_DIR = PROJ_ROOT / "backend"

# --------------------------------------------------
# CREATE DIRECTORIES
# --------------------------------------------------
for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_DIR,
    LOGS_DIR,
    REPORTS_DIR,
]:
    directory.mkdir(
        parents=True,
        exist_ok=True
    )

# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------
logger.remove()

# Console Logging
try:
    from tqdm import tqdm

    logger.add(
        lambda msg: tqdm.write(msg, end=""),
        colorize=True
    )

except ModuleNotFoundError:

    logger.add(
        sys.stdout,
        colorize=True
    )

# File Logging
logger.add(
    LOGS_DIR / "app_{time}.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} - "
        "{message}"
    ),
)

logger.success(
    "✅ Project configuration loaded successfully"
)