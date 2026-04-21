import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"
sys.path.append(os.path.dirname(__file__))

from mcp_server import get_latest_info_mcp,get_video_script_mcp,get_topic_summary_mcp

print("Testing MCP DIRETLY")
print("="*50)

#Test 1 researh tool
print("\n Test 1: get_latest_info_mcp")
print("-"*40)
result1=get_latest_info_mcp("SpaceX latest launch 2026")
print(result1[:500])
print("...[truncated]")
#test 2 

print("\n Test 2 : get_topic_summary_mcp")
print("-"*40)
result2=get_topic_summary_mcp("AI agents:latest in 2026")
print(result2)

# Test 3 : Full script tool
print("\n Test 3 : get_video_script_mcp")
result3=get_video_script_mcp(
    topic ="how to get the business ideas",
    platform="youtube_shorts",
    tone="casual")
print(result3)

print("\n" + "="*50)
print("ALL TOOLLS TESTEST SUCCESSFULLY 1")
