from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}









# from fastapi import APIRouter, status
# from sqlalchemy.exc import SQLAlchemyError
# from app.db.session import SessionLocal  

# router = APIRouter()

# @router.get("/health")
# def health_check():
#     db_status = "ok"
#     try:
#         db = SessionLocal()
#         db.execute("SELECT 1") 
#     except SQLAlchemyError:
#         db_status = "error"

#     return {
#         "status": "ok" if db_status == "ok" else "degraded",
#         "database": db_status
#     }









