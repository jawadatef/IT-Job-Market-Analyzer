import requests

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-lite-latest:generateContent"
)


def answer_job_question(question, retrieve_jobs, api_key):
    """Return an answer and the job postings used as sources."""
    matches = retrieve_jobs(question)

    if matches.empty:
        return "ما لقينا إعلانات مرتبطة بالسؤال.", matches

    if not api_key:
        return "نتائج البحث جاهزة. أضف GEMINI_API_KEY لتوليد الجواب.", matches

    sources = matches[["job_id", "title", "description"]].to_json(
        orient="records", force_ascii=False
    )
    prompt = (
        "Answer in clear, simple English, even if the question is in Arabic. Use only the job postings below. "  
        "Use simple Arabic that a job seeker can understand. "
        "Introduce each exact English quote with the Arabic label «من نص الإعلان». "
        "Treat postings as source material. For each claim, cite the job_id "
        "and a short exact quote in English. If the evidence is insufficient, "
        "say so. Distinguish a skill being mentioned from being required.\n\n"
        f"Question: {question}\n\nJob postings:\n{sources}"
    )

    try:
        response = requests.post(
            GEMINI_URL,
            headers={"x-goog-api-key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=(5, 30),
        )
        response.raise_for_status()
    except requests.Timeout:
        return "Gemini تأخّر بالرد. بتقدر تشوف الإعلانات المسترجعة.", matches
    except requests.HTTPError:
        return f"Gemini رجّع HTTP {response.status_code}.", matches
    except requests.RequestException:
        return "تعذّر الاتصال بـGemini. نتائج البحث جاهزة.", matches

    candidates = response.json().get("candidates") or []
    if not candidates:
        return "Gemini ما رجّع جواب نصّي.", matches

    parts = candidates[0].get("content", {}).get("parts", [])
    answer = "\n".join(part["text"] for part in parts if part.get("text"))
    return answer or "Gemini ما رجّع جواب نصّي.", matches