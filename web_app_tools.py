from crewai_tools import ScrapeWebsiteTool
from langchain_community.tools import DuckDuckGoSearchResults
from beeai_framework.tools import tool
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


def extract_links(text):
    """
    Extracts all links present in the given text.

    Args:
        text (str): The text to extract links from.

    Returns:
        list: A list of extracted links.
    """
    pattern = r"https?://\S+"
    links = re.findall(pattern, text)
    return links


@tool
def scrap_web_page(links: str) -> list[str]:
    """
           Takes a list of websites then scrap and combine their respective content.

           Args:
               links (list): The list of website urls to scrap and extract the contents.

           Returns:
               A list of websites contents related to the query
           """
    logger.info(f"......................................................scrap_web_page********START with input: {links}")
    websites_content = []
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', links)
    for link in links:
        try:
            s_tool = ScrapeWebsiteTool(website_url=link)
            content = s_tool.run()
            logger.info(f"#################################scrap web page: {link} with output: {content}")
            websites_content.append(content)
        except Exception as ex:
            logger.info("Error while parsing a link", ex)
        logger.info(f"......................................................scrap_web_page*************END with output: {websites_content}")
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
    search_results = search.run(query)
    links = extract_links(search_results)
    logger.info(f"......................................................search_web*************END with output: {links}")
    return links
