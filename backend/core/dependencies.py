from backend.database.session import SessionLocal


def get_db():
    """FastAPI dependency that yields a database session per request
    and always closes it, even if the request errors out.

    Usage in a route:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
