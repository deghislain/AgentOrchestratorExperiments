
def get_the_team_goal(details_report: str, agents_capabilities: str, number_agents: int):
    return f"""
        Given the following goal: search the web and write an outstanding report on AI.

            
            {details_report}
             
            Cite key sources, studies, and research papers

         Considering you have {number_agents} agents with the following capabilities:
         
            {agents_capabilities}
         


        Please provide two prompts that can be used by those {number_agents} agents to achieve the aforementioned goal.
        You will return a response in JSON format. Here is an example of response:
        {{
                "prompts":{ 
                    {"search_prompt": "Here goes the search prompt"},
                    {"write_report_prompt": "Here goes the write report prompt"} 
                }
                
        }}  
    """