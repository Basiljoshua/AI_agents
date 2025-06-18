Issue : 
    The event planning requires a stronger model
    Gemini 1.5 flash would be insufficient to retrive the big mass of data 
    from google search and proceed with a selected website

Proposed Solution :
    You can use 3 llms with each llm specifically for one agent
    Using a single llm for all 3 agents 
        1. Input token count = 32.65K 
        2. Requests Count = 12

a. Passing api key in crewai llm function assumes VertexChat AI. Rather do not pass api key 
    explicitely but as environment vaiable and then load it.
b. every agent can use different llm, it can be passed in the Agent function