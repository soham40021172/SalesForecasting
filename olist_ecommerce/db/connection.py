from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseConnection:
    def __init__(self):
        try:
            self.host = os.getenv("DB_HOST")
            self.port = os.getenv("DB_PORT")
            self.db = os.getenv("DB_NAME")
            self.user = os.getenv("DB_USER")
            self.password = os.getenv("DB_PASSWORD")

            self.database_url = (
                f"postgresql+psycopg2://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.db}"
            )

            self.engine = create_engine(self.database_url, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)

            logger.success("Database connection initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing DB connection: {e}")
            raise

    def get_engine(self):
        return self.engine

    def get_session(self):
        return self.SessionLocal()

db_connection = DatabaseConnection()

engine = db_connection.get_engine()
SessionLocal = db_connection.get_session()