import json
import os
import random
import urllib.error
import urllib.request


HF_SPACE_URL = os.getenv("HF_SPACE_URL", "").rstrip("/")
API_KEY = os.getenv("API_KEY", "")

PROMPTS = [
    "Ping",
    "Hello",
    "Give me one short tip.",
    "What is one useful fact?",
    "Summarize the word active.",
]


def main() -> int:
    if not HF_SPACE_URL:
        print("HF_SPACE_URL is not set")
        return 2
    if not API_KEY:
        print("API_KEY is not set")
        return 2

    # Random prompt to simulate daily usage.
    prompt = random.choice(PROMPTS)
    payload = json.dumps(
        {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        f"{HF_SPACE_URL}/v1/jobs",
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", "replace")
            print(f"Status: {resp.status}")
            print(f"Prompt: {prompt}")
            print(f"Response: {body}")
            if 200 <= resp.status < 300:
                return 0
            return 1
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print(f"HTTP error: {e.code}")
        print(f"Response: {body}")
        return 1
    except Exception as e:
        print("Request failed:", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
