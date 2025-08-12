from database import engine, Base
from models import User, Order

Base.metadata.create_all(bind=engine)
def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized and tables created.")