import requests
import os
from dotenv import load_dotenv

class APIClient(requests.Session):
  def __init__(self, userId, userPassKey):
    # Loading .env
    load_dotenv()

    super(APIClient, self).__init__()
    self.verify = False
    
    # Auth info
    self.userId = userId
    self.userPassKey = userPassKey
    self.baseUrl = os.environ.get('APP_API_BASE_URL')
    self.headers = {
        'Content-Type': 'application/json'
    }
    
    self.__get_token()
  
  def __get_token(self):
    response = self.post_req(url='/User/Login', data={ 'userName': self.userId, 'password': self.userPassKey})
    token = response.json().get('token')
    self.headers['Authorization'] = f'Bearer {response.json().get("token")}'

  def get_req(self, url, data=None):
    return self.get(self.baseUrl + url, headers=self.headers, json=data)
  def post_req(self, url, data=None):
    return self.post(self.baseUrl + url, headers=self.headers, json=data)
  def put_req(self, url, data=None):
    return self.put(self.baseUrl + url, headers=self.headers, json=data)
  def delete_req(self, url, data=None):
    return self.delete(self.baseUrl + url, headers=self.headers, json=data)
  