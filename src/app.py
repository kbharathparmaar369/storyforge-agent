from sys import platform
from re import search
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq
from utils import (
    validate_search_results,
    validate_script_output,
    retry_with_backoff,
    get_friendly_error
)

os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

def get_tavily_client():
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("TAVILY_API_KEY")
        except Exception:
            pass
    if not key:
        raise ValueError("TAVILY_API_KEY is missing. Please set TAVILY_API_KEY in your .env file or Streamlit Secrets.")
    return TavilyClient(api_key=key)

def get_groq_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
    if not key:
        raise ValueError("GROQ_API_KEY is missing. Please set GROQ_API_KEY in your .env file or Streamlit Secrets.")
    return Groq(api_key=key)

def get_realtime_info(query : str) -> dict:
    
    #search the web for real time information on a given topic.repr
    try:
        tavily_client = get_tavily_client()
        response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
        include_raw_content=False
    )

        answer=response.get("answer","No summary available")

        results=[]
        for item in response.get("results",[]):
            results.append({
            "title":item.get("title", ""),
            "url":item.get("url", ""),
            "content":item.get("content", ""),
            "score":item.get("score", 0)

        })

        if not results:
            response=tavily_client.search(
                query=query,
                search_depth="basic",
                max_result=3,
                include_answer=False,
                include_raw_content=False
            )
            for item in response.get("results",[]):
                results.append({
                    "title":item.get("title", ""),
                    "url":item.get("url", ""),
                    "content":item.get("content", ""),
                    "score":item.get("score",0)
                })

        return{
            "query":query,
            "answer":answer,
            "results":results,
            "total_results":len(results)

        }

    except Exception as e:
        return {
            "query": query,
            "answer": "Search failed",
            "results": [],
            "total_results": 0,
            "error": str(e)
        }

# 2 : function format search results

def format_search_results(search_data: dict) ->str:

    if not search_data["results"]:
        return "No info found"
    
    formatted=f"Topic : {search_data['query']}\n\n"
    formatted +=f"summary :{search_data['answer']}\n\n"
    formatted +="Detailed sources : \n"
    formatted +="-" * 40 + "\n"

    for i ,result in enumerate(search_data["results"],1):
        formatted +=f"\n[Source {i}] {result['title']}\n"
        formatted +=f"url: {result['url']}\n"
        formatted +=f"Content : {result['content'][:300]}...\n"
    
    return formatted

# 3 : generating the video scipt

def generate_video_script(
    info_text: str,
    topic : str,
    platform : str ="youtube_shorts",
    tone:str = "educational"
) -> dict:

    platform_config={
        "youtube_shorts":{
            "duration":"60 seconds",
            "words":"200-220 words",
            "name": "youtube shorts"

        },
        "instagram_reels":{
            "duration": "60 seconds",
            "words": "180-200 words",
            "name": "Instagram Reels"
        }
    }

    tone_config={
         "educational": "informative, clear, and fact-focused. Teach the viewer something valuable.",
        "funny": "humorous, witty, and entertaining. Use light jokes and fun comparisons.",
        "dramatic": "intense, suspenseful, and exciting. Build tension and awe.",
        "casual": "friendly, conversational, and relaxed. Like talking to a friend."
    }

    config=platform_config.get(platform,platform_config["youtube_shorts"])
    tone_desc=tone_config.get(tone, tone_config["educational"])


    prompt = f"""You are a viral short-form video script writer with 10 years experience writing for top YouTube creators.

Your scripts always follow this PROVEN structure:
1. HOOK (first 5 seconds): Start with a shocking fact, question, or bold statement that stops the scroll. Make it UNBELIEVABLE.
2. CONTEXT (5 seconds): Explain why this matters RIGHT NOW.
3. MAIN CONTENT (45 seconds): 5 punchy points, each explained in 2-3 detailed sentences. Provide depth and value.
4. CALL TO ACTION (5 seconds): Simple, specific action for viewer to take.

STRICT RULES:
- Aim for a word count of exactly {config['words']}.
- Every sentence must be punchy — maximum 15 words.
- No bullet points, no headers, no stage directions.
- No words like "firstly", "furthermore", "in conclusion".
- Write exactly how a human speaks out loud.
- Use "you" and "we" to talk directly to viewer.
- Each point must flow naturally into the next.
- Platform: {config['name']} ({config['duration']})
- Tone: {tone_desc}
- Output ONLY the spoken script — nothing else, no labels, no sections

RESEARCH TO USE:
{info_text}

TOPIC: {topic}

Write the script now:"""

    try:
        groq_client = get_groq_client()
        print(f"\n Generating {config['name']} script ({tone} tone) ...")

        response=groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role":"system",
                    "content":"you are a professional youtube and instagram content creator who writes viral short-form video scripts. "
                    },
                    {
                        "role":"user",
                        "content":prompt
                    }
            ],
            temperature=0.7,
            max_tokens=500
        )

        script=response.choices[0].message.content.strip()

        word_count=len(script.split())

        title_response=groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                "role":"user",
                "content": f"Generate 3 catchy video titles for a {config['name']} about: {topic}. Return only the 3 titles, numbered 1-3, nothing else."
                }
            ],
            temperature=0.9,
            max_tokens=120
        )
        titles=title_response.choices[0].message.content.strip()
       
        hashtag_response=groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                "role":"user",
                "content": f"""Generate 15 hashtags for a {config['name']} about: {topic}
                Mix of:
                - 5 broad hashtags (high volume like #shorts #viral)
                - 5 topic specific hashtags
                - 5 niche hashtags (low competition)
                - Return ONLY hashtags separated by spaces, nothing else"""
                }
            ],
                temperature=0.6,
                max_tokens=100
        )
        hashtags=hashtag_response.choices[0].message.content.strip()

        print(f"Scripts generated ! ({word_count} words)")
        return {

            "script":script,
            "word_count":word_count,
            "platform":config["name"],
            "tone":tone,
            "topic":topic,
            "titles":titles,
            "hashtags":hashtags,
            "estimated_duration":f"{round(word_count/2.5)} seconds"
        }

    except Exception as e:
        print(f" Script generation error: {e}")
        return {
            "script": "Script generation failed.",
            "word_count": 0,
            "error": str(e)
        }


# 4 : Full  pipeline

def run_pipeline(
    topic: str,
    platform: str="youtube_shorts",
    tone: str="educational"
) -> dict:
    print(f"\n Starting StoryForge pipeline for: '{topic}'")
    print("="*50)

    search_data=get_realtime_info(topic)
    info_text=format_search_results(search_data)

    script_data=generate_video_script(
        info_text=info_text,
        topic=topic,
        platform=platform,
        tone=tone
    )

    result={
        "topic":topic,
        "platform":script_data.get("platform"),
        "tone":tone,
        "script":script_data.get("script"),
        "word_count":script_data.get("word_count"),
        "estimated_duration":script_data.get("estimated_duration"),
        "titles":script_data.get("titles"),
        "hashtags":script_data.get("hashtags"),
        "sources":[r["url"] for r in search_data.get("results",[])],
        "search_summary":search_data.get("answer"),
        "error": script_data.get("error") or search_data.get("error")
        }
    
    print("\n Pipeline compeleted !")
    return result

# test block

if __name__=="__main__":
    result=run_pipeline(
        topic="black hole expalined",
         platform="youtube_shorts",  
         tone="educational" 
    )

    print("\n" + "="*50)
    print("GENERATED SCRIPT :")
    print(result["script"])
    print("SUGGESTED TITLES : ")
    print(result["titles"])
    print("\n HASHTAGS :")
    print(result["hashtags"])
    print(f"\n Word Count : {result['word_count']}")
    print(f"Estimated duration :{result['estimated_duration']}")
    print("\n SOURCES :")
    for url in result["sources"]:
        print(f" - {url}")
    print("\n" + "="*50)

    
    result2=run_pipeline(
        topic="climate change latest news",
        platform="instagram_reels",
        tone="dramatic"
    )


    print("\n INSTAGRAM REELS SCRIPT :")
    print("="*50)
    print(result2["script"])