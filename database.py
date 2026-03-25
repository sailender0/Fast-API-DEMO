
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

db_url = "postgresql://postgres:S%40keth67@localhost:5432/sailender"
engine= create_engine(db_url)
sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)