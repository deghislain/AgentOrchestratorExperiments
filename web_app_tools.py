from crewai_tools import ScrapeWebsiteTool
from langchain_community.tools import DuckDuckGoSearchResults
from beeai_framework.tools import tool
from urllib.parse import urlparse
import re

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
    logger.info(
        f"......................................................scrap_web_page********START with input: {links}")
    websites_content = []
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',links)

    logger.info(f"**********************************urls: {urls}")
    for link in urls:
        try:
            s_tool = ScrapeWebsiteTool(website_url=link)
            content = s_tool.run()
            logger.info(f"#################################scrap web page: {link} with output: {content}")
            websites_content.append(content)
        except Exception as ex:
            logger.info(f"Error while extracting the content of this website {link}", ex)
        logger.info(
            f"......................................................scrap_web_page*************END with output: {websites_content}")
    return websites_content


@tool
def search_web(query: str) -> list[str]:
    """
        Search the web for the given query and returns a list of websites.

        Args:
            query (str): The search query to execute.

        Returns:
            A list of websites related to the topic
        """
    logger.info(f"......................................................search_web********START with input: {query}")
    search = DuckDuckGoSearchResults()
    search_results =search.run(query)
    logger.info(
        f"......................................................search_web*************END with output: {search_results}")
    return search_results
