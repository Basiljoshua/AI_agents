# Automatic Event Planning
#warning control
import warnings 
warnings.filterwarnings('ignore')

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

#import os
#os.environ["SERPER_API_KEY"] = os.getenv('SERPER_API_KEY') # Serper tool can directly read from os.getenv 
                                                           # so this line is not necessary and redundant

from crewai import LLM
def get_gemini_llm():
    return LLM(
        model="gemini/gemini-1.5-flash",
        temperature=0.7,
        #api_key=os.getenv("AIzaSyCqmDZLJMrMvXSYR2h3R4ahffVMbvYfhhA") - This will use vertex chat AI
    )

llm = get_gemini_llm()

from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

# Initialize the tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agent 1: Venue Coordinator
venue_coordinator = Agent(
    role="Venue Coordinator",
    goal="Identify and book an appropriate venue "
    "based on event requirements",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a keen sense of space and "
        "understanding of event logistics, "
        "you excel at finding and securing "
        "the perfect venue that fits the event's theme, "
        "size, and budget constraints."
    ),
    llm=llm
)

 # Agent 2: Logistics Manager
logistics_manager = Agent(
    role='Logistics Manager',
    goal=(
        "Manage all logistics for the event "
        "including catering and equipment"
    ),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Organized and detail-oriented, "
        "you ensure that every logistical aspect of the event "
        "from catering to equipment setup "
        "is flawlessly executed to create a seamless experience."
    ),
    llm=llm
)

# Agent 3: Marketing and Communications Agent
marketing_communications_agent = Agent(
    role="Marketing and Communications Agent",
    goal="Effectively market the event and "
         "communicate with participants",
    tools=[search_tool, scrape_tool], # Search tool returns a website, Scrape tool retrivers website info
    verbose=True,
    backstory=(
        "Creative and communicative, "
        "you craft compelling messages and "
        "engage with potential attendees "
        "to maximize event exposure and participation."
    ),
    llm=llm
)

# Create a class VenueDetails using Pydantic BaseModel to store venuedetails.
from pydantic import BaseModel
class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    contact: str

# Agents will populate this object with information 
# about different venues by creating different instances of it.
# Fuzzy output from agents are transferred to stronger typed output 

# Creating venue task 
venue_task = Task(
    description="Find a venue in {event_city} "
                "that meets criteria for {event_topic}.",
    expected_output="All the details of a specifically chosen"
                    "venue you found to accommodate the event.",
    human_input=False, # Ask for feedback from users before ending task
    output_json=VenueDetails, # Agents will convert their fuzzy outputs 
                              # to stronger typed format
                              # If not, it will plainly typed in one line
    output_file="venue_details.json",  
      # Outputs the venue details as a JSON file
    agent=venue_coordinator
)

# Creating logistics task
logistics_task = Task(
    description="Coordinate catering and "
                 "equipment for an event "
                 "with {expected_participants} participants "
                 "on {tentative_date}.",
    expected_output="a markdown report on confirmation of all logistics arrangements "
                    "including catering and equipment setup.",
    human_input=False, # Ask for any human input
    output_file="logistics_report.md", #
    async_execution=True, # This task will be executed parallely with other tasks coming after it
    agent=logistics_manager
)

# Creating marketting task
marketing_task = Task(
    description="Promote the {event_topic} "
                "aiming to engage at least"
                "{expected_participants} potential attendees.",
    expected_output="Report on marketing activities "
                    "and attendee engagement formatted as markdown.",
    output_file="marketing_report.md",  # Report on activities done to promote the event
    agent=marketing_communications_agent
)

# Define the crew with agents and tasks
event_management_crew = Crew(
    agents=[venue_coordinator, 
            logistics_manager, 
            marketing_communications_agent],
    
    tasks=[venue_task, 
           logistics_task, 
           marketing_task],
    
    verbose=True
)

event_details = {
    'event_topic': "Birthday Party",
    'event_description': "A gathering of family and friends "
                         " to celebrate my nephew's birthday. "
                         "Parking facility is mandatory.",
    'event_city': "Kochi",
    'tentative_date': "2025-07-25",
    'expected_participants': 50,
    'budget': 2000,
    'venue_type': "Open Hall"
}

result = event_management_crew.kickoff(inputs=event_details)

# from crewai import Agent , Task , Crew

# # Create an agent
# agent = Agent(
#     role="AI Assistant",
#     goal="Help users with their questions",
#     backstory="You are a helpful AI assistant powered by Gemini.",
#     llm=llm,
#     verbose=True
# )

# # Create a task
# task = Task(
#     description="Explain what CrewAI is and its main benefits",
#     expected_output="A clear explanation of CrewAI and its key advantages",
#     agent=agent
# )

# # Create and run the crew
# crew = Crew(
#     agents=[agent],
#     tasks=[task],
#     verbose=True
# )

# result = crew.kickoff()
# print(result)