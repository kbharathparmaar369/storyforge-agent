import os
import sys
import time

os.environ["PYTHONENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"


def validate_topic(topic: str) -> tuple[bool, str]:
    if not topic or not topic.strip():
        return False, "Topic cannot be empty, please enter a topic"

    if len(topic.strip()) < 3:
        return False, "Topic is too short"

    if len(topic.strip()) > 200:
        return False, "Topic is too long. Please keep it under 200 characters"

    clean = topic.replace(" ", "").replace("-", "").replace("_", "")
    if not any(c.isalpha() for c in clean):
        return False, "Topic must contain actual words"

    return True, ""


def validate_platform(platform: str) -> str:
    valid = ["youtube_shorts", "instagram_reels"]
    return platform if platform in valid else "youtube_shorts"


def validate_tone(tone: str) -> str:
    valid = ["educational", "funny", "dramatic", "casual"]
    return tone if tone in valid else "educational"


def sanitize_topic(topic: str) -> str:
    safe = "".join(c for c in topic if c.isalnum() or c in (" ", "-", "_"))
    return safe.strip()[:100]


def validate_search_results(search_data: dict) -> tuple[bool, str]:
    if not search_data:
        return False, "Search returned no data."

    if search_data.get("error"):
        return False, f"Search error: {search_data['error']}"

    if search_data.get("total_results", 0) == 0:
        return False, "No search results found for this topic. Try a different or broader topic."

    return True, ""


def validate_script_output(script_data: dict) -> tuple[bool, str]:
    if not script_data:
        return False, "Script generation returned no data."

    if script_data.get("error"):
        return False, f"Script generation error: {script_data['error']}"

    script = script_data.get("script") or ""

    if not script or script == "Script generation failed.":
        return False, "Script generation failed. Please try again."

    if len(script.split()) < 30:
        return False, "Generated script is too short. Please try again."

    return True, ""


def retry_with_backoff(func, max_retries: int = 3, *args, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_str = str(e).lower()

            if "rate limit" in error_str or "429" in error_str:
                wait_time = (2 ** attempt) * 2
                print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue

            if "auth" in error_str or "api key" in error_str or "401" in error_str:
                raise Exception("API authentication failed. Check your API keys in .env file.")

            if "connection" in error_str or "timeout" in error_str:
                wait_time = (2 ** attempt)
                time.sleep(wait_time)
                continue

            if attempt == max_retries - 1:
                raise e

    raise Exception(f"Failed after {max_retries} attempts.")


def get_friendly_error(error: Exception) -> str:
    error_str = str(error).lower()

    if "api key" in error_str or "auth" in error_str or "401" in error_str:
        return "API key error. Please check your GROQ_API_KEY and TAVILY_API_KEY in your .env file."

    if "rate limit" in error_str or "429" in error_str:
        return "API rate limit reached. Please wait 30 seconds and try again."

    if "connection" in error_str or "timeout" in error_str:
        return "Connection error. Please check your internet connection and try again."

    if "quota" in error_str or "billing" in error_str:
        return "API quota exceeded. Please check your API usage limits."

    if "model" in error_str and "not found" in error_str:
        return "AI model not available. Please try again in a moment."

    return f"Something went wrong: {str(error)}. Please try again."
