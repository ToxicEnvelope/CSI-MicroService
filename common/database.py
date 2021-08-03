from common import config
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

root = config.get_root_path()
print("[+] Connection String: " + root)
print("[+] Exists ? ", os.path.exists(root))

__engine = create_engine(f"sqlite:////{root}/cross-domain-service.db", convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=__engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    try:
        Base.metadata.create_all(bind=__engine)
        print("[+] Connected to Database successfully.")
    except:
        return False
    return True
