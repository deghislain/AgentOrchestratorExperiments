from crewai_tools import ScrapeWebsiteTool
from langchain_community.tools import DuckDuckGoSearchResults
from beeai_framework.tools import tool
from typing import Dict

import logging

logger = logging.getLogger('web_app_tools')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


@tool
def scrap_web_page(links: str) -> list[str]:
    """
           Takes a list of websites then scrap and combine their respective content.

           Args:
               links (list): The list of website urls to scrap and extract the contents.

           Returns:
               A list of websites contents related to the query
           """
    logger.info("......................................................scrap_web_page********START")
    websites_content = []
    for link in links:
        try:
            s_tool = ScrapeWebsiteTool(website_url=link)
            websites_content.append(s_tool.run())
        except Exception as ex:
            logger.info("Error while parsing a link", ex)
            logger.info("......................................................scrap_web_page*************END")
    return websites_content


@tool
def search_web(topic: str) -> list[str]:
    """
        Search the web for the given topic and returns a list of websites.

        Args:
            topic (str): The search topic to execute.

        Returns:
            A list of websites containing information related to the topic
        """
    logger.info("......................................................search_web********START")
    search = DuckDuckGoSearchResults()
    search_results = search.run(topic)
    links = search_results.split(', links: ')
    logger.info("......................................................search_web*************END")
    return links



