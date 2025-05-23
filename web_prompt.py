
def get_the_team_goal(details_report: str, agents_capabilities: str, number_agents: int):
    return f"""
        Given the following goal: search the web and write an outstanding report on AI.
        
        MAKE SURE THE FOLLOWING WRITING INSTRUCTIONS ARE FOLLOWED:    
            {details_report}
             
            Cite key sources, studies, and research papers

         Considering you have {number_agents} agents with the following capabilities:
         
            {agents_capabilities}
         


        Please provide two prompts that can be used by those {number_agents} agents to achieve the aforementioned goal.
        Leverage other agents' outputs as inputs for your tasks. When crafting prompts, 
        specify the agents and outputs to incorporate, ensuring seamless collaboration and informed results.
        You will return a response in JSON format. Here is an example of response:
        {{
                "prompts":{ {"search_prompt": "Here goes the search prompt ",
                             "description": "This prompt should be used to search the web by the SearchAgent"
                             },
    {"write_report_prompt": "Here goes the write report prompt",
     "description": "This prompt should be used to write the report by the WriteReportAgent"
     } }
                
        }}  
    """