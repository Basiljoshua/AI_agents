# Multi-Agent Customer Support Automation 

#warning control
import warnings 
warnings.filterwarnings('ignore')

from datetime import date
from dotenv import load_dotenv
load_dotenv()

import os
from crewai import LLM
def get_gemini_llm():
    return LLM(
        model="gemini/gemini-1.5-flash",
        temperature=0.7,
    )

llm = get_gemini_llm()
# def use_gemini_openai_compatible():
#     llm = LLM(
#         model="gemini/gemini-2.0-flash",
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#         api_key=os.getenv("GOOGLE_API_KEY"),  # Replace with your actual key
#     )
    
#     return llm


# llm = use_gemini_openai_compatible() 
# Acquiring Tools
from crewai_tools import (
    #SerperDevTool, # Does a google search
    WebsiteSearchTool, # A RAG tool for searching website content,
    ScrapeWebsiteTool # Scrape a given url
)

# search_tool = SerperDevTool()
BBC_search_tool=ScrapeWebsiteTool(
    website="https://www.bbc.com/news"
)
Firstpost_search_tool=ScrapeWebsiteTool(
    website="https://www.firstpost.com/"
)
CNN_search_tool=ScrapeWebsiteTool(
    website="https://edition.cnn.com/"
)


from crewai import Agent , Task , Crew

news_reporter=Agent(
    role="Senior News Reporter",
    goal="Deliver timely, accurate, and impactful" 
        " international news—especially on geopolitics and global affairs by retrieving information from various tools.",
    backstory=(
        "You are a senior journalist having access to https://www.bbc.com, https://edition.cnn.com/ and https://www.firstpost.com/ . "
        "You are known for your commitment to truth and clarity. "
        "Your primary responsibility is to report the most relevant and "
        "up-to-date international and national stories, with a sharp focus "
        "on geopolitical developments and global diplomatic relations and Indian Govenrment policies and economy. "
        "Your audience relies on your ability to cut through the noise and highlight the most important events. "
        "Stay objective, prioritize verified information, and always deliver the news that truly matters to UPSC aspirant."
        ),
    allow_delegation=False,
    llm=llm,
    tools=[BBC_search_tool,CNN_search_tool,Firstpost_search_tool],
    verbose=False
    )

UPSC_news_ranker = Agent(
    role="Senior News Specialist",
    goal=(
        "Identify and rank news articles in chronological order "
        "based on their importance and relevance for UPSC aspirants."
    ),
    backstory=(
        "You are a Senior News Specialist helping UPSC students"
        "tasked with curating and ranking the top 10 news articles each day for UPSC aspirants. "
        "Your audience relies on you to present news in an order that reflects not just timeliness, "
        "but also the significance and relevance of each story for civil service preparation. "
        "You must prioritize news related to geopolitics, international relations, governance, policy, "
        "and other subjects critical to the UPSC syllabus. "
        "The order in which you present news directly shapes how your audience consumes and learns from it, "
        "so accuracy, context, and insight are key."
    ),
    llm=llm,
    verbose=False
)


# Creating Tasks

news_fetch = Task(
    description=(
        "{Student} has reached out to know today’s top news.\n"
        "{Student} is a bright and sharp learner, so your response must reflect that standard. "
        "Use tools at your disposal to deliver the most relevant, accurate, and up-to-date information. "
        "Focus specifically on topics such as geopolitics, international relations, and governance policies received from your tools."
    ),
    expected_output=(
        "Deliver crisp and clear news updates in bullet points from available tools.\n"
        "- Each point should contain a few sentenses to read and understand about the issue.\n"
        "- Remove repetitive news content.\n"
        "- Ensure the facts are accurate.\n"
        "- Maintain an informative, neutral, and insightful tone suitable for a UPSC aspirant.\n" 
        "- Add the source of each bullet point"
    ),
    agent=news_reporter
)


news_prioritize = Task(
    description=(
        "Review the news bullet points written by the Senior News Reporter in response to {Student}'s request. "
        "Your job is to select and rank the **top 10 news items** based on the following priority criteria:\n"
        "1. International News\n"
        "2. Geo-political developments\n"
        "3. News on Indian Government Policies\n"
        "4. News on Indian Economy and New business developments"
        "\nAny bullet points containing obscene, inappropriate must be removed.\n"
        "Ensure the final output is well-structured, clearly written, and contain a conclusion."
    ),
    expected_output=(
        "A concise and well-organized list of the **top 10 news articles**, ranked by the priority criteria.\n"
        "- Each point should contain a few sentenses to read and understand about the issue.\n"
        "- Each bullet point should cover a distinct topic—avoid repetition or multiple points on the same issue.\n"
        "- Content should be easily digestible and ideal for UPSC note-making.\n"
        "- Avoid excessive jargon and add the source of the news at last."
    ),
    # This task does not have access to the docs scrape tool.
    # The agent must rely only on the content provided by the Support agent.
    agent=UPSC_news_ranker,
    output_file="{Date} News.md"
)

print("Putting the crew together...")
# Putting the crew together
crew = Crew(
    agents=[news_reporter,UPSC_news_ranker],
    tasks=[news_fetch,news_prioritize],
    verbose=True,
    #memory=True # Enables short term , long term and entity memory
    # memory function requires OPENAI API key
)


print(" Starting Kickoff...")
datetoday = date.today().strftime("%d-%m-%Y")  # e.g., '23-06-2025'
result = crew.kickoff(inputs={"Student" : "Basil Joshua Reji","Date":datetoday})




