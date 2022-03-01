from common import Config
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

root = Config.get_root_path()
print("[+] Connection String: " + root)
print("[+] Exists ? ", os.path.exists(root))

if os.name != 'nt':
    db_sc = "sqlite:////%s/cross-domain-service.db" % root
else:
    db_sc = r"sqlite:///%s\cross-domain-service.db" % root

__engine = create_engine(db_sc, convert_unicode=True)
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
