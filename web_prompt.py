
def get_the_team_goal():
    return """
        Given the following goal: search the web and write an outstanding report on AI.

        Ensure the report has the following structure and information:

            Definition of Artificial Intelligence (AI)
            Brief history and development of AI
            Importance and relevance of AI in modern times

            Cite key sources, studies, and research papers

         Considering you have 2 agents with the following capabilities:
         1.agent name=SearchAgent,
           agent capability=Conduct a targeted web search for a specified topic and return a curated list of relevant 
           websites, prioritizing credible sources such as academic journals, research papers, government websites, 
           and reputable news outlets.

         2. agent name="ReportWriterAgent"
           agent capability=Given a list of curated websites and a specified topic, extract relevant content, 
           analyze and synthesize the information,and write a well-structured report. 


        Please provide two prompts that can be used by those two agents to achieve the aforementioned goal.
        You will return a response in JSON format. Here is an example of response:
        {{
            "prompts":{
                            { 
                                "search_prompt": "Here goes the search prompt",
                            },
                            { 
                                "write_report_prompt": "Here goes the write report prompt",
                            }

        }}  
    """