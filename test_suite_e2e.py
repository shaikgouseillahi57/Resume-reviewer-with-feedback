import httpx
import json
import os
import sys

BASE_URL = "http://127.0.0.1:8000"
SAMPLE_PDF = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_resumes", "sample_frontend_resume.pdf"))

passed = 0
failed = 0

def log_test(name, success, details=""):
    global passed, failed
    if success:
        passed += 1
        print(f"[PASS] {name} | {details}")
    else:
        failed += 1
        print(f"[FAIL] {name} | {details}")

print(f"--- Starting Full E2E Test Suite against {BASE_URL} ---")

client = httpx.Client(timeout=60.0)

# 1. Health check
try:
    r = client.get(f"{BASE_URL}/")
    data = r.json()
    log_test("GET / (Health Check)", r.status_code == 200 and data.get("status") == "online", f"Status: {r.status_code}, data: {data}")
except Exception as e:
    log_test("GET / (Health Check)", False, str(e))

# 2. Analyze Resume Upload (PDF)
try:
    with open(SAMPLE_PDF, "rb") as f:
        files = {"file": ("sample_frontend_resume.pdf", f, "application/pdf")}
        data = {"target_role": "Frontend Developer", "analysis_mode": "with_target_role"}
        r = client.post(f"{BASE_URL}/analyze-resume", files=files, data=data)
        res_data = r.json()
        valid = (
            r.status_code == 200 and 
            "resume_score" in res_data and 
            "detected_skills" in res_data and
            "strengths" in res_data and
            "weaknesses" in res_data
        )
        score = res_data.get("resume_score")
        role = res_data.get("target_role")
        log_test("POST /analyze-resume (Upload & Score)", valid, f"Score: {score}/100, Role: {role}, Skills: {len(res_data.get('detected_skills', []))}")
except Exception as e:
    log_test("POST /analyze-resume (Upload & Score)", False, str(e))

# 3. Analyze Resume Auto-Role (without target role)
try:
    with open(SAMPLE_PDF, "rb") as f:
        files = {"file": ("sample_frontend_resume.pdf", f, "application/pdf")}
        data = {"analysis_mode": "without_target_role"}
        r = client.post(f"{BASE_URL}/analyze-resume", files=files, data=data)
        res_data = r.json()
        auto_role = res_data.get("target_role")
        valid = r.status_code == 200 and res_data.get("is_auto_role") is True
        log_test("POST /analyze-resume (Auto-Detect Role Mode)", valid, f"Auto-detected role: {auto_role}")
except Exception as e:
    log_test("POST /analyze-resume (Auto-Detect Role Mode)", False, str(e))

# 4. Job Matcher (/match-job)
try:
    with open(SAMPLE_PDF, "rb") as f:
        files = {"file": ("sample_frontend_resume.pdf", f, "application/pdf")}
        data = {
            "job_description": "We are seeking a Frontend Engineer proficient in React, JavaScript, HTML, CSS, TypeScript, and Git to build scalable responsive user interfaces."
        }
        r = client.post(f"{BASE_URL}/match-job", files=files, data=data)
        res_data = r.json()
        match_score = res_data.get("match_score")
        valid = r.status_code == 200 and "match_score" in res_data and "matched_skills" in res_data
        log_test("POST /match-job (Job Description Matcher)", valid, f"Match Score: {match_score}%, Matched Skills: {len(res_data.get('matched_skills', []))}")
except Exception as e:
    log_test("POST /match-job (Job Description Matcher)", False, str(e))

# 5. Format Analyzer (/analyze-format)
try:
    with open(SAMPLE_PDF, "rb") as f:
        files = {"file": ("sample_frontend_resume.pdf", f, "application/pdf")}
        r = client.post(f"{BASE_URL}/analyze-format", files=files)
        res_data = r.json()
        fmt_score = res_data.get("format_score")
        valid = r.status_code == 200 and "format_score" in res_data and "bullet_analysis" in res_data
        log_test("POST /analyze-format (Resume Format Audit)", valid, f"Format Score: {fmt_score}/100, Bullets: {res_data.get('bullet_analysis', {}).get('total')}")
except Exception as e:
    log_test("POST /analyze-format (Resume Format Audit)", False, str(e))

# 6. Rewrite Bullet Point (/rewrite-bullet)
try:
    payload = {
        "bullet": "Worked on frontend user interfaces using React and JavaScript.",
        "target_role": "Frontend Developer"
    }
    r = client.post(f"{BASE_URL}/rewrite-bullet", json=payload)
    res_data = r.json()
    variations = res_data.get("variations", [])
    valid = r.status_code == 200 and len(variations) > 0
    sample_text = variations[0].get("rewritten", "") if variations else ""
    log_test("POST /rewrite-bullet (Live Bullet Optimizer)", valid, f"Generated {len(variations)} variations. Top: {sample_text[:50]}...")
except Exception as e:
    log_test("POST /rewrite-bullet (Live Bullet Optimizer)", False, str(e))

# 7. Generate Cover Letter (/generate-cover-letter)
try:
    payload = {
        "resume_text": "Experienced Frontend Engineer with 4 years building React, TypeScript, and modern responsive web apps.",
        "job_description": "Frontend Engineer wanted for leading SaaS product team. Requires React and TypeScript.",
        "target_role": "Frontend Developer"
    }
    r = client.post(f"{BASE_URL}/generate-cover-letter", json=payload)
    res_data = r.json()
    letter = res_data.get("cover_letter")
    valid = r.status_code == 200 and bool(letter)
    log_test("POST /generate-cover-letter (AI Cover Letter Generator)", valid, f"Letter Length: {len(letter) if letter else 0} chars")
except Exception as e:
    log_test("POST /generate-cover-letter (AI Cover Letter Generator)", False, str(e))

# 8. History Endpoint (/history)
try:
    r = client.get(f"{BASE_URL}/history")
    valid = r.status_code == 200
    log_test("GET /history (Supabase / Local History)", valid, f"Status: {r.status_code}")
except Exception as e:
    log_test("GET /history (Supabase / Local History)", False, str(e))

print(f"\n==========================================")
print(f"Results: {passed} PASSED, {failed} FAILED")
print(f"==========================================")

if failed > 0:
    sys.exit(1)
