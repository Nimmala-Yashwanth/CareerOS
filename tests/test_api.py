from app.matching import match_skills

def test_health(client):
    assert client.get('/health').json() == {'status':'ok'}

def test_register_login_and_invalid_login(client):
    payload={'email':'bob@example.com','password':'verylongpassword'}
    assert client.post('/api/auth/register',json=payload).status_code==201
    assert client.post('/api/auth/register',json=payload).status_code==409
    assert client.post('/api/auth/login',json=payload).status_code==200
    assert client.post('/api/auth/login',json={**payload,'password':'wrong'}).status_code==401

def test_auth_required(client):
    assert client.get('/api/applications').status_code==401
    assert client.get('/api/export.csv').status_code==401

def test_application_lifecycle(client,auth):
    data={'company':'Acme','role':'Backend Engineer','status':'applied','location':'Remote'}
    response=client.post('/api/applications',json=data,headers=auth)
    assert response.status_code==201
    id=response.json()['id']
    assert client.get('/api/applications?search=acme',headers=auth).json()[0]['id']==id
    assert client.patch(f'/api/applications/{id}',json={'status':'interview'},headers=auth).json()['status']=='interview'
    stats=client.get('/api/analytics',headers=auth).json()
    assert stats['total']==1 and stats['positive_response_rate']==100
    assert 'Acme' in client.get('/api/export.csv',headers=auth).text
    assert client.delete(f'/api/applications/{id}',headers=auth).status_code==204
    assert client.get(f'/api/applications/{id}',headers=auth).status_code==404

def test_users_cannot_access_each_others_data(client,auth):
    id=client.post('/api/applications',json={'company':'Private','role':'Developer'},headers=auth).json()['id']
    second=client.post('/api/auth/register',json={'email':'other@example.com','password':'anotherpassword'}).json()['access_token']
    other={'Authorization':'Bearer '+second}
    assert client.get(f'/api/applications/{id}',headers=other).status_code==404
    assert client.patch(f'/api/applications/{id}',json={'status':'offer'},headers=other).status_code==404
    assert client.delete(f'/api/applications/{id}',headers=other).status_code==404
    assert client.get('/api/applications',headers=other).json()==[]

def test_skills_and_matching(client,auth):
    assert client.put('/api/skills',json={'skills':['Python','Docker','python']},headers=auth).json()['skills']==['docker','python']
    result=client.post('/api/match',json={'job_description':'Seeking Python, Docker, and PostgreSQL engineering experience.'},headers=auth).json()
    assert result['score']==67
    assert result['missing']==['postgresql']

def test_keyword_boundaries():
    assert match_skills('We need JavaScript expertise', ['java'])['detected_requirements']==['javascript']
    assert match_skills('No known catalog skills mentioned here.',[])['score'] is None

def test_csv_formula_injection(client,auth):
    client.post('/api/applications',json={'company':'=HYPERLINK("evil")','role':'Developer'},headers=auth)
    assert "'=HYPERLINK" in client.get('/api/export.csv',headers=auth).text
