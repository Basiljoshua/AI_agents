Requirement :
 Learn todays-news fast and understand its impact

 Issues :
    1. more than one bullet point speaks of the same matter, the bullet points must speak a
        bout different news
    2. Obscene news or Irrevalant news are also ranked, news pertaining to Rape, Murdur, Burglary
        is unnecessary


Improvements :
    1. Create another agent to remove all obscene news points. 
        it should delegate articles back to prioritizer to re-rank the articles
    2. More than one news website (The Hindu and CNN) can be scraped and passed as input DONE
    3. Prompt better to remove repetitive news bulletions DONE
    4. Consider reducing the size from 10 to 5 

    
Realizations : 
    1. Even if no tools were provided , the llm model does a query based on prompt and 
       return news from prominent news channels. We have to prompt explicitely to use specific websites
       and resources of news retrival 

