from fastapi import APIRouter, Depends, Query, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.ranking import Ranking
from app.schemas.ranking import RankRequest, RankResponse, RankingOut
from app.services.rank_service import extract_text_from_resume, gemini_score_and_feedback, mock_photo_check, process_image_for_gemini
from fastapi import Form
from typing import Optional


router = APIRouter()

@router.post("/rank", response_model=RankResponse)
def rank_resume(data: RankRequest, db: Session = Depends(get_db)):
    # score, feedback = mock_score_and_feedback(data.resume_text, data.job_description)
    score, feedback = gemini_score_and_feedback(data.resume_text, data.job_description)


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





# @router.post("/rank-file", response_model=RankResponse)
# async def rank_resume_file(
#     resume_file: UploadFile = File(...),
#     job_description: str = Form(...),
#     photo_base64: Optional[str] = Form(None),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Extract resume text from uploaded PDF
#         resume_text = await extract_text_from_resume(resume_file)

#         # Score and feedback via Gemini
#         score, feedback = gemini_score_and_feedback(resume_text, job_description)

#         # Optionally check photo
#         photo_check = None
#         if photo_base64:
#             photo_check = mock_photo_check(photo_base64)

#         # Save to DB
#         ranking = Ranking(
#             resume_text=resume_text,
#             job_description=job_description,
#             score=score,
#             feedback=feedback,
#             photo_check=photo_check,
#         )
#         db.add(ranking)
#         db.commit()
#         db.refresh(ranking)
#         return ranking

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    


# Working with dummy image analysis

# @router.post("/rank-resume-text", response_model=RankResponse)
# async def rank_resume_file(
#     file: UploadFile = File(...),
#     job_description: str = Form(...),
#     image: UploadFile = File(None),
#     db: Session = Depends(get_db),
# ):
#     try:
#         # Step 1: Extract resume text
#         resume_text = await extract_text_from_resume(file)

#         # Step 2: Score using Gemini
#         score, feedback = gemini_score_and_feedback(resume_text, job_description)

#         # Step 3: Image check (optional)
#         photo_check = None
#         if image:
#             photo_check = process_image_from_analysis(image)

#         # Step 4: Save result to DB
#         ranking = Ranking(
#             resume_text=resume_text,
#             job_description=job_description,
#             score=score,
#             feedback=feedback,
#             photo_check=photo_check,
#         )
#         db.add(ranking)
#         db.commit()
#         db.refresh(ranking)

#         return ranking

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# Working with gemini text and  image analysis
@router.post("/rank-resume-text", response_model=RankResponse)
async def rank_resume_text(
    resume_text: str = Form(...),
    job_description: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Step 1: Generate score & feedback using Gemini

        score, feedback = gemini_score_and_feedback(resume_text, job_description)

        # Step 3: Image check (optional)
        photo_check = None
        if image:
            photo_check = process_image_for_gemini(image)

        # Step 4: Save result to DB
        ranking = Ranking(
            resume_text=resume_text,
            job_description=job_description,
            score=score,
            feedback=feedback,
            photo_check=photo_check,
        )
        db.add(ranking)
        db.commit()
        db.refresh(ranking)

        return ranking

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# With Gemini for image

@router.post("/rank-resume-file", response_model=RankResponse)
async def rank_resume_file(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    try:
        # Step 1: Extract resume text
        resume_text = await extract_text_from_resume(file)

        # Step 2: Score using Gemini
        score, feedback = gemini_score_and_feedback(resume_text, job_description)

        # Step 3: Image check (optional)
        photo_check = None
        if image:
            photo_check = process_image_for_gemini(image)

        # Step 4: Save result to DB
        ranking = Ranking(
            resume_text=resume_text,
            job_description=job_description,
            score=score,
            feedback=feedback,
            photo_check=photo_check,
        )
        db.add(ranking)
        db.commit()
        db.refresh(ranking)

        return ranking

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))






# @router.post("/rank-file", response_model=RankResponse)
# async def rank_resume_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     try:
#         # Extract text from the uploaded resume file
#         resume_text = await extract_text_from_resume(file)
#         job_description = "Example job description"  # You can adjust this part

#         # Analyze the resume with Gemini API
#         score, feedback = gemini_score_and_feedback(resume_text, job_description)

#         # Store the ranking result
#         ranking = Ranking(
#             resume_text=resume_text,
#             job_description=job_description,
#             score=score,
#             feedback=feedback,
#         )
#         db.add(ranking)
#         db.commit()
#         db.refresh(ranking)
#         return ranking

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
