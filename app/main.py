from fastapi import FastAPI
from app.api.endpoints import rank, health
from app.db.session import engine
from app.models import ranking  # Triggers table creation

app = FastAPI(
    title="Mini Resume Ranker",
    version="1.0.0",
    docs_url="/docs"
)

# Include Routers
app.include_router(rank.router, prefix="/rank", tags=["Rank"])
app.include_router(health.router, tags=["Health"])

# Create DB tables at startup
@app.on_event("startup")
def on_startup():
    ranking.Base.metadata.create_all(bind=engine)
