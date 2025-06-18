# Multi-Agent Customer Support Automation 

#warning control
import warnings 
warnings.filterwarnings('ignore')

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

from crewai import Agent , Task , Crew

support_agent=Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful support representative in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and "
        " are now working on providing "
		"support to {customer}, a super important customer "
        " for your company."
		"You need to make sure that you provide the best support!"
		"Make sure to provide full complete answers. "
        ),
    allow_delegation=False,
    llm=llm,
    verbose=True
    )

support_quality_assurance_agent=Agent(
    role="Support Quality assurance Specialist",
    goal="Get recognition for providing the "
        "best support quality assurance in your team",
    backstory=(
        "You work at crewAI (https://crewai.com) and "
        "are now working with your team "
		"on a request from {customer} ensuring that "
        "the support representative is "
		"providing the best support possible.\n"
		"You need to make sure that the support representative "
        "is providing full"
		"complete answers."
    ),
    #Support Quality Assurance Agent can delegate work back to the Support Agent, allowing for these agents to work together.
    llm=llm,
    verbose=True
)

# Acquiring Tools
from crewai_tools import (
    #SerperDevTool, # Does a google search
    WebsiteSearchTool, # A RAG tool for searching website content,
    ScrapeWebsiteTool # Scrape a given url
)

# search_tool = SerperDevTool()
docs_scrape_tool=ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/"
)

# Creating Tasks

inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
	    "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
		"Make sure to use everything you know "
        "to provide the best support possible."
		"You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
	    "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
		"leaving no questions unanswered, and maintain a helpful and friendly "
		"tone throughout."
    ),
	tools=[docs_scrape_tool],
    agent=support_agent
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
		"thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
		"Don't be too formal, we are a chill and cool company "
	    "but maintain a professional and friendly tone throughout."
    ),
    #this task does not have docs scrape tool meaning QA agent wont be able to look at the docs, this ensures
    # the agent will purely acess what the response the Support agent wrote
    agent=support_quality_assurance_agent,
)
print("Putting the crew together...")
# Putting the crew together
crew = Crew(
    agents=[support_agent,support_quality_assurance_agent],
    tasks=[inquiry_resolution,quality_assurance_review],
    verbose=True,
    #memory=True # Enables short term , long term and entity memory
    # memory function requires OPENAI API key
)

inputs = {
    "customer": "Student Founders",
    "person": "Basil Joshua Reji",
    "inquiry": "I need help with setting up a Crew "
               "and kicking it off, specifically "
               "how can I add memory to my crew? "
               "Can you provide guidance? "
}
print(" Starting Kickoff...")
result = crew.kickoff(inputs=inputs)




