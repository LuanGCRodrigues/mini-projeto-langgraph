from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import DATABASE_URL, SQLALCHEMY_ECHO

engine = create_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
