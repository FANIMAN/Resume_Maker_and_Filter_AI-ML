import pytest
from app.services.rank_service import mock_score_and_feedback, mock_photo_check


def test_mock_score_and_feedback():
    resume = "Experienced Python developer with machine learning background."
    job = "Looking for a Python developer with experience in machine learning."
    score, feedback = mock_score_and_feedback(resume, job)
    
    assert isinstance(score, int)
    assert 40 <= score <= 95
    assert "Score" in feedback


def test_mock_photo_check_valid():
    valid_png = "data:image/png;base64,aalkffa.emlnga,amdapqjafaavafafararafafafa" 
    result = mock_photo_check(valid_png)
    assert result in ["Looks professional", "Acceptable", "Not professional", "Invalid image data"]


def test_mock_photo_check_invalid():
    invalid_photo = "this-is-not-base64"
    result = mock_photo_check(invalid_photo)
    assert result == "Invalid image data"
