import pytest
from fastapi.testclient import TestClient  
from app.main import app

@pytest.mark.asyncio
async def test_rankings_pagination():
    client = TestClient(app)
    
    # First page with limit of 10
    response = client.get("/rank/rankings?skip=0&limit=5")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10 
    
    response = client.get("/rank/rankings?skip=5&limit=5")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10 
