def test_ai_requires_auth(client):
    r = client.post('/api/ai/feedback', json={
        'job_description': 'We need Python, React and PostgreSQL developers with experience.',
        'matched': ['python'], 'missing': ['postgresql']})
    assert r.status_code in (401, 403)
