import os
import sys
import json
import urllib.request
import urllib.error


def main() -> int:
    has_openai_sdk = True
    try:
        from openai import OpenAI
    except Exception as e:
        has_openai_sdk = False
        print("WARN: openai SDK not available, falling back to raw HTTPS request:", repr(e))

    print("python_executable:", sys.executable)
    print("has_OPENAI_API_KEY:", bool(os.getenv("OPENAI_API_KEY")))
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY missing in environment")
        return 3

    if has_openai_sdk:
        client = OpenAI()
        try:
            resp = client.responses.create(
                model="gpt-5-mini",
                tools=[{"type": "web_search", "external_web_access": False}],
                tool_choice="auto",
                include=["web_search_call.action.sources"],
                input="Find the sunrise time in Paris today and cite the source.",
            )
        except Exception as e:
            print("ERROR: Responses API call failed:", type(e).__name__)
            print(str(e))
            return 4

        print("--- output_text ---")
        print(resp.output_text)

        sources_count = 0
        try:
            for item in getattr(resp, "output", []) or []:
                if getattr(item, "type", None) == "web_search_call":
                    action = getattr(item, "action", None)
                    sources = getattr(action, "sources", None)
                    if sources:
                        sources_count += len(sources)
        except Exception:
            pass

        print("--- web_search sources count (best-effort) ---")
        print(sources_count)
        print("--- done ---")
        return 0

    url = "https://api.openai.com/v1/responses"
    body = {
        "model": "gpt-5-mini",
        "tools": [{"type": "web_search", "external_web_access": False}],
        "tool_choice": "auto",
        "include": ["web_search_call.action.sources"],
        "input": "Find the sunrise time in Paris today and cite the source.",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8", errors="replace")
            status = getattr(r, "status", None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        print("ERROR: HTTPError", getattr(e, "code", None))
        print(raw)
        return 4
    except Exception as e:
        print("ERROR: request failed:", type(e).__name__)
        print(str(e))
        return 4

    print("http_status:", status)

    try:
        data = json.loads(raw)
    except Exception:
        print("ERROR: failed to parse JSON response")
        print(raw)
        return 5

    if isinstance(data, dict) and data.get("error"):
        print("ERROR: API returned error")
        print(json.dumps(data.get("error"), ensure_ascii=False, indent=2))
        return 6

    output_text = data.get("output_text")
    if not output_text:
        try:
            for item in data.get("output", []) or []:
                if item.get("type") == "message":
                    content = item.get("content", [])
                    if content and content[0].get("type") == "output_text":
                        output_text = content[0].get("text")
                        break
        except Exception:
            output_text = None

    print("--- output_text ---")
    print(output_text or "(no output_text extracted)")

    sources_count = 0
    try:
        for item in data.get("output", []) or []:
            if item.get("type") == "web_search_call":
                action = item.get("action") or {}
                sources = action.get("sources") or []
                sources_count += len(sources)
    except Exception:
        pass

    print("--- web_search sources count (best-effort) ---")
    print(sources_count)
    print("--- done ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
