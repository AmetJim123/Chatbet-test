from sqlalchemy import Table, Column, Integer, String
from app.database.database import meta, engine


users = Table(
    "users",
    meta,
    Column("id", Integer, primary_key=True),
    Column("email", String(100), nullable=False),
    Column("password", String(200), nullable=False),
    Column("status", Integer, nullable=False, default=1),
    )

meta.create_all(engine)