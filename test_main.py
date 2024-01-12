import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app  

@pytest.fixture
def test_client():
    return TestClient(app)

# Test for root endpoint
def test_root_endpoint(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Test for user registration
def test_register_user(test_client):
    
    user_data = {
        "first_name": "siddd",
        "last_name": "verma",
        "email": "svvv@gmail.com",
        "mobile": "828540",
        "password": "svv123",
        "isAdmin": False,
        "address": "delhi",
        "bloodGroup": "a+",
        
        "hospital_id": 0,
        "isAlive": False,
       
    }

    response = test_client.post("/registerUser", json=user_data)
    assert response.status_code == 200
      
    
#Test for single user

def test_getuserByToken(test_client):
    user_id=1
    
    response = test_client.get(f"/getUsersByTokenId?user_id={user_id}")
    assert response.status_code == 200
    
# Test for user authentication
def test_authentication(test_client):
   
        user_data ={
  "first_name": "rahul",
  "last_name": "kumar",
  "email": "admin@gmail.com",
  "mobile": "828540",
  "password": "root",
  "isAdmin": False,
  "address": "delhi",
  "bloodGroup": "a+",
  "hospital_id": 0,
  "isAlive": False
}
        response = test_client.post(f"/authenticateUser?email={user_data['email']}&password={user_data['password']}",json={"email": user_data["email"], "password": user_data["password"]})

        assert response.status_code == 200


def test_forgot_password(test_client):
    email = "svvv@gmail.com"
    
    
    with patch('smtplib.SMTP') as mock_smtp:
        # Specify the expected return values for the mocked methods
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.starttls.return_value = None
        mock_smtp_instance.login.return_value = None
        mock_smtp_instance.sendmail.return_value = None
        mock_smtp_instance.quit.return_value = None

       
        response = test_client.put(f"/forgotPassword?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": "Temporary password sent successfully"}

def test_get_organs(test_client):
    response = test_client.get("/getOrgans")
    assert response.status_code == 200


def test_get_hospital(test_client):
    response = test_client.get("/getHospital")
    assert response.status_code == 200
 
    
def test_get_previous_contributions(test_client):
   
    user_id = 1
    response = test_client.get(f"/previousContributions/{user_id}")
    assert response.status_code == 200
    
def test_contribute_organ(test_client):
   
    user_id = 1
    organ_id = 1
    response = test_client.put(f"/contribute/{user_id}/{organ_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Contribution Placed successfully"}

def test_request_organ(test_client):
    user_id = 1
    organ_id = 1
    reason = "Urgent need"
    response = test_client.put(f"/request/{user_id}/{organ_id}?reason={reason}")
    assert response.status_code == 200
    assert response.json() == {"message": "Request Placed successfully"}
    
def test_get_available_organs_for_donation(test_client):
    response = test_client.get("/getAvailableOrgansForDonation")
    assert response.status_code == 200
    
def test_get_requests(test_client):
    response = test_client.get("/getRequests")
    assert response.status_code == 200
    
