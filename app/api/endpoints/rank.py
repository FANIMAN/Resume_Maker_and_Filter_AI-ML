from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.ranking import Ranking
from app.schemas.ranking import RankRequest, RankResponse, RankingOut
from app.services.rank_service import mock_score_and_feedback, mock_photo_check

router = APIRouter()

@router.post("/rank", response_model=RankResponse)
def rank_resume(data: RankRequest, db: Session = Depends(get_db)):
    score, feedback = mock_score_and_feedback(data.resume_text, data.job_description)

    photo_check = None
    if data.photo_base64:
        photo_check = mock_photo_check(data.photo_base64)

    ranking = Ranking(
        resume_text=data.resume_text,
        job_description=data.job_description,
        score=score,
        feedback=feedback,
        photo_check=photo_check,
    )
    db.add(ranking)
    db.commit()
    db.refresh(ranking)
    return ranking

@router.get("/rankings", response_model=list[RankingOut])
def get_rankings(
    db: Session = Depends(get_db),
    min_score: int = Query(None),
    search: str = Query(None),
    page: int = 1,
    per_page: int = 10
):
    query = db.query(Ranking)
    if min_score is not None:
        query = query.filter(Ranking.score >= min_score)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            Ranking.resume_text.ilike(search_pattern) |
            Ranking.job_description.ilike(search_pattern)
        )

    rankings = query.order_by(Ranking.created_at.desc()) \
                    .offset((page - 1) * per_page) \
                    .limit(per_page) \
                    .all()
    return rankings
