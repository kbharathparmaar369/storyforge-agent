import os
import sys
import json
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
from dotenv import load_dotenv
sys.path.append(os.path.dirname(__file__))

from fastmcp import FastMCP
from app import get_realtime_info,format_search_results,generate_video_script,run_pipeline
load_dotenv()



mcp=FastMCP(
   name="StoryForge Agent",
   instruction="""You are StoryForge, an AI-powered YouTube and Instagram content creation agent.
    You can research any topic in real-time and generate optimized short-form video scripts.
    Use get_latest_info_mcp to research a topic first, then get_video_script_mcp to generate the script."""
)

# TOOL 1: Research Tool
@mcp.tool()
def get_latest_info_mcp(query: str)-> str:
    """
     Searches the web for the latest real-time information on any topic.
    Use this tool first before generating a script to get current facts and data.

    Args:
        query: The topic or question to search for (e.g. "black holes explained")

    Returns:
        A formatted string with search summary, articles and source URL
    """
    try:
        print(f"[MCP] Tool called : get_latest_info_mcp")
        print(f"[MCP] Query : {query}")

        #run search
        search_data=get_realtime_info(query)
        formatted=format_search_results(search_data)
        sources=[
            {
            "title": r["title"],
            "url": r["url"]
            }
            for r in search_data.get("results",[])
        ]

        output=f"{formatted}\n\nSOURCES_JSON:\n{json.dumps(sources,indent=2)}"

        print(f"[MCP] Returning {search_data['total_results']} results")
        return output

    except Exception as e:
        error_msg=f"search failed :{str(e)}"
        print(f"[MCP] Error :{error_msg}")
        return error_msg

# Tool 2 script generation
@mcp.tool()
def get_video_script_mcp(
    topic: str,
    platform: str="youtube_shorts",
    tone :str="educational"
) -> str:
    """
    Generates a complete short-form video script for YouTube Shorts or Instagram Reels.
    This tool handles everything — it researches the topic AND generates the script.

    Args:
        topic: The video topic (e.g. "climate change explained simply")
        platform: Either "youtube_shorts" (60s) or "instagram_reels" (30s)
        tone: Either "educational", "funny", "dramatic", or "casual"

    Returns:
        A complete script with title suggestions, hashtags, word count and sources
    """
    try:
        print(f"[MCP] tool called : get_video_script_mcp")
        print(f"[MCP] Topic :{topic} | platform :{platform} | Tone :{tone}")

        #validate the input

        valid_platforms=["youtube_shorts","instagram_reels"]
        valid_tones=["educational","funny","dramatic","casual"]

        if platform not in valid_platforms:
            platform="youtube_shorts"
            print(f"[MCP] Invalid platform, defaulting to youtube_shorts")
        
        if tone not in valid_tones:
            tone="educational"
            print(f"[MCP] Invalid tone, defaulting to educational")

        result=run_pipeline(
            topic=topic,
            platform=platform,
            tone=tone
        )

        output=f"""
                STORYFORGE SCRIPT GENERATED
                ============================
                Topic:{result.get('topic')}
                Platform:{result.get('platform')}
                Tone:{result.get('tone')}
                Word count:{result.get('word_count')}
                Estimated Duration :{result.get('estimated_duration')}

                SCRIPT:
                -------
                {result.get('script')}
                
                SUGGESTED TITLES:
                ----------------
                {result.get('titles')}

                HASHTAGS:
                ---------
                {result.get('hashtags')}

                SOURCES:
                --------

                {chr(10).join(result.get('sources',[]))}

             """

            
        print(f"[MCP] script generated successfully")
        return output.strip()

    except Exception as e:
        error_msg=f"Script generation failed : {str(e)}"
        print(f"[MCP] Error : {error_msg}")
        return error_msg


# Quick summary tool
@mcp.tool()
def get_topic_summary_mcp(topic: str) -> str:
    """
    Gets a quick one-paragraph summary of any topic using real-time web search.
    Use this for a fast overview before deciding on a full script.

    Args:
        topic: Any topic to summarize

    Returns:
        A short paragraph summary with key facts 
    """
    try:
        print(f"\n [MCP] Tool called : get_topic_summary_mcp")
        print(f"[MCP] Topic :{topic}")

        search_data=get_realtime_info(topic)
        summary=search_data.get("answer","No summary available")

        sources=[r["url"] for r in search_data.get("results",[])[:3]]
        sources_text="\n".join(sources)
        

        output=f"""

        Topic Summary : {topic}
        =====================
        {summary}

        TOP SOURCES:
        --------
        {sources_text}
        """

        return output.strip()

    except Exception as e:
        return f"summary Failed :{str(e)}"

# Run server

if __name__=="__main__":
    import sys

    if len(sys.argv)>1 and sys.argv[1]=="--stdio":
        mcp.run(transport="stdio")
    else:
        print("\n StoryForge MCP server starting ... ")
        print("Tools available:")
        print("1. get_latest_info_mcp  - real-time web search")
        print("2. get_video_script_mcp -full script generation")
        print("3. get_topic_summary_mcp - quick topic summary")
        print("\n server running ! Waiting for tool calls ...\n")
        mcp.run(transport="stdio")