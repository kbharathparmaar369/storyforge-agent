import os
import sys
os.environ["PYTHONENCODING"]="utf-8"
os.environ["PYTHONUTF8"]="1"

def validate_topic(topic: str)->tuple[bool,str]:
    if not topic or not topic.strip():
        return False,"Topic cannot be empty , please enter a topic"

    if len(topic.strip())<3:
        return False,"Topic is too short"

    if len(topic.strip()) > 200:
        return False,"Topic is too long. Please keep it under 200 character"

    clean=topic.replace(" ","").replace("-","").replace("_","")
    if not any(c.isalpha() for c in clean):
        return False,"Topic must contain actual words"

    return True, ""

def validate_platform(platform: str) -> str:
    valid=["educational","funny","dramatic","casual"]
    return tone if tone in valid else "educational"

def santitze_topic(topic: str) -> str:
    safe="".join(c for c in topic if c.isalnum() or c in (" ","-","_"))
    return safe.strip()[:100]
def validate_search_results(search_data: dict) -> tuple[bool, str]:
    """
    Checks if search results are usable.
    Returns (is_valid, error_message)
    """
    if not search_data:
        return False, "Search returned no data."

    if search_data.get("error"):
        return False, f"Search error: {search_data['error']}"

    if search_data.get("total_results", 0) == 0:
        return False, "No search results found for this topic. Try a different or broader topic."

    return True, ""


def validate_script_output(script_data: dict) -> tuple[bool, str]:
    """
    Checks if generated script is usable.
    Returns (is_valid, error_message)
    """
    if not script_data:
        return False, "Script generation returned no data."

    if script_data.get("error"):
        return False, f"Script generation error: {script_data['error']}"

    script = script_data.get("script", "")

    if not script or script == "Script generation failed.":
        return False, "Script generation failed. Please try again."

    if len(script.split()) < 30:
        return False, "Generated script is too short. Please try again."

    return True, ""


# ── Rate limit handler ────────────────────────────────────

import time

def retry_with_backoff(func, max_retries: int = 3, *args, **kwargs):
    """
    Retries a function with exponential backoff.
    Useful for handling API rate limits.
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_str = str(e).lower()

            # Rate limit errors
            if "rate limit" in error_str or "429" in error_str:
                wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue

            # Auth errors — no point retrying
            if "auth" in error_str or "api key" in error_str or "401" in error_str:
                raise Exception(f"API authentication failed. Check your API keys in .env file.")

            # Connection errors
            if "connection" in error_str or "timeout" in error_str:
                wait_time = (2 ** attempt)
                time.sleep(wait_time)
                continue

            # Unknown error on last attempt
            if attempt == max_retries - 1:
                raise e

    raise Exception(f"Failed after {max_retries} attempts.")


# ── Friendly error messages ───────────────────────────────

def get_friendly_error(error: Exception) -> str:
    """
    Converts technical errors into
    user-friendly messages.
    """
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
