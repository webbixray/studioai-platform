import io
import datetime
import jwt
import pytest
from flask import Flask
from app import app as flask_app

# helper JWT
SECRET="***"
ALGORITHM="HS256"

def demo_token():
    payload={"sub":"tester","role":"admin","exp":int(datetime.datetime.utcnow().timestamp())+3600}
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

@pytest.fixture
def client():
    flask_app.config["TESTING"]=True
    with flask_app.test_client() as c:
        yield c

def _upload(client, token, content, fname="sample.txt"):
    data={
        'name':'test-artifact',
        'description':'integration test',
        'visibility':'public',
    }
    data['file']=(io.BytesIO(content), fname)
    return client.post('/api/marketplace/upload',data=data,headers={'Authorization':f'Bearer {token}'},content_type='multipart/form-data')

def test_upload_download(client):
    token=demo_token()
    r=_upload(client,token,b'hello world')
    assert r.status_code in (200,201)
    # list
    l=client.get('/api/marketplace/list')
    assert l.status_code==200
    artifacts=l.json.get('artifacts',[])
    aid=next(a['id'] for a in artifacts if a['name']=='test-artifact')
    # download
    d=client.get(f'/api/marketplace/download/{aid}')
    assert d.status_code==200
    assert d.data==b'hello world'
