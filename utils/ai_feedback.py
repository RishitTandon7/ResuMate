import requests

def get_ai_feedback(resume_text):
    API_KEY = "AIzaSyCH4e3uW1SuQXUY7DaNAzrURAo88XMutzo"
    URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Review the following resume and give exactly 3 specific suggestions to improve it:\n\n{resume_text}"
                    }
                ]
            }
        ]
    }

    tips_payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Based on the following resume, provide 3 personalized resume writing tips:\n\n{resume_text}"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        suggestions_text = data['candidates'][0]['content']['parts'][0]['text']
        suggestions = [line.strip("•-123. ").strip() for line in suggestions_text.split("\n") if line.strip()]

        tips_response = requests.post(URL, headers=headers, json=tips_payload, timeout=10)
        tips_response.raise_for_status()
        tips_data = tips_response.json()

        tips_text = tips_data['candidates'][0]['content']['parts'][0]['text']
        tips = [line.strip("•-123. ").strip() for line in tips_text.split("\n") if line.strip()]

        return {
            "suggestions": suggestions[:3],
            "tips": tips[:3]
        }

    except requests.exceptions.RequestException as e:
        return {
            "suggestions": [f"Error contacting Gemini API: {str(e)}"],
            "tips": []
        }
    except Exception as e:
        return {
            "suggestions": [f"Unexpected error: {str(e)}"],
            "tips": []
        }

