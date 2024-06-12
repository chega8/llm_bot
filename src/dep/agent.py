from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()


def get_tavily():
    return TavilySearchResults()
