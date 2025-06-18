Issue Faced
"raise exception_type(
    model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
                                                            ^^^^^^^^^^^^^^^^^
    raise e
    
.BadRequestError:"

I have tried giving a simple API request with the google api key and it has worked fine.
I tried using multiple models and uptil gemini-2.5-flash-preview , it gave a response 
so its not a problem of api key or the llm used. 

Maybe the problem is CrewAI may not yet have full 
compatibility with Gemini's prompt formatting expectations 
(e.g., missing system prompts, input formatting, or function/tool call structure).

Check if crewai expects a different LLM class config for Gemini (since most examples use OpenAI or Anthropic).
OpenAI was checked, but no free models of openai are available as of today. (tried both gpt-3.5-turbo and gpt-4.0-mini)
both give errors on exhausted quotas and hence require biling

DATED : 15th June
This error indicates that CrewAI is trying to use Google Vertex AI which requires GCP credentials instead of the Google Gemini API.
The error occurs because Vertex AI requires different authentication 
(Google Cloud credentials) while Gemini API uses a simple API key.

SOLUTION: Use OpenAI-Compatible Gemini Endpoint
from crewai import LLM
def use_gemini_openai_compatible():
    llm = LLM(
        model="openai/gemini-2.0-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key="AIzaSyDrShjpMrOg6kP7bZQN6ywl7lk3hcSZEPI",  # Replace with your actual key
    )
    
    return llm

now we have used the gemini openai compatible form, and this works
I am grateful for not giving up. It only has to work once. 
Lessons : Reading Documentation is very important
          Go to the AI assistant of the framework(if any), they are better equipped to give solutinos

AGENTS2.0
URL Construction Issue: The OpenAI-compatible endpoint for 
Gemini might have URL construction problems in the current CrewAI/LiteLLM version
SOLUTION : Start with a minimal configuration to isolate the issue