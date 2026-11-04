import re

# Explainable baseline: explicit skill phrases, no external model or hidden scoring.
SKILL_CATALOG = [
    'python','java','javascript','typescript','react','next.js','node.js','fastapi',
    'spring boot','postgresql','mysql','mongodb','redis','docker','kubernetes',
    'aws','azure','gcp','kafka','airflow','sql','git','github actions',
    'rest api','graphql','machine learning','pytorch','tensorflow','pandas',
    'spark','ci/cd','linux','microservices','testing','pytest','html','css'
]

def normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text.lower())

def contains_skill(text: str, skill: str) -> bool:
    return re.search(r'(?<![\w])' + re.escape(skill) + r'(?![\w])', normalize(text)) is not None

def match_skills(description: str, owned: list[str]) -> dict:
    required = sorted(s for s in SKILL_CATALOG if contains_skill(description, s))
    owned_normalized = {s.strip().lower() for s in owned}
    matched = sorted(set(required) & owned_normalized)
    missing = sorted(set(required) - owned_normalized)
    score = round(100 * len(matched) / len(required)) if required else None
    return {'score': score, 'matched': matched, 'missing': missing, 'detected_requirements': required,
            'method': 'Transparent keyword matching against a fixed skill catalog; not an ATS prediction.'}
