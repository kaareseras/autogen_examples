import autogen
import os
import requests
from bs4 import BeautifulSoup
import requests
import json

from dotenv import load_dotenv

load_dotenv()


# === Setup Keys ===

# [START create_agent_with_bing_grounding_tool]

# === Bing Web Search Function ===

def cognism(Industri: str, region: str) -> str:
    """Search the web using Cognism API."""
    COGNISM_API_KEY = os.environ["COGNISM_API_KEY"]


    url = "https://app.cognism.com/api/search/account/search?indexSize=5&lastReturnedKey="

    payload = json.dumps({
    # "names": [
    #     "Cognism"
    # ],
    "revenue": {
        "from": 500000000,
        "to": 1000000000
    },
    # "domains": [
    #     "www.cognism.com"
    # ],
    "industries": [
        Industri
    ],
    # "types": [
    #     "Public Company"
    # ],
    # "technologies": [
    #     "MongoDB"
    # ],
    "regions": [
        region
    ],
    # "cities": [
    #     "London"
    # ],
    # "size": {
    #     "from": 0,
    #     "to": 500
    # },
    "accountSearchOptions": {
        "match_exact_company_name": False,
        "match_exact_domain": False,
        "filter_domain": "exists",
        "location_Type": "ALL",
        "events_operator": "OR",
        "sort_fields": []
    }
    })
    headers = {
    'Authorization': 'Bearer ' + COGNISM_API_KEY,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text



# === Function Schemas for OpenAI ===

cognism_func = {
    "name": "cognism_search",
    "description": "Searches for companies.",
    "parameters": {
        "type": "object",
        "properties": {
            "Industri": {"type": "string", "description": "The industry to search for"},
            "region": {"type": "string", "description": "The region to search in"},
        },
        "required": ["Industri", "region"],
    },
}

# === LLM Config ===

config_list_gpt4 = [
    {
        'model': 'gpt-4o-2',
        'api_key': os.getenv('API_KEY'),
        'base_url': os.getenv('API_BASE'),
        'api_type': 'azure',
        'api_version': '2024-08-01-preview',
    }
]

llm_config = {
    "seed": 39,  # change the seed for different trials
    "temperature": 0.5,
    "config_list": config_list_gpt4,
    "timeout": 120,
}


# === Agents ===

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config=False,
)

search_agent = autogen.AssistantAgent(
    name="SearchAgent",
    llm_config=llm_config,
    function_map={"cognism_search": cognism_func},
    system_message="Search cognsim for companies.",
    human_input_mode="NEVER",
)


summarizer_agent = autogen.AssistantAgent(
    name="SummarizerAgent",
    llm_config=llm_config,
    system_message="Summarize the fetched content.",
    human_input_mode="NEVER",
)

# === Orchestration ===

group_chat = autogen.GroupChat(
    agents=[user_proxy, search_agent, summarizer_agent],
    messages=[],
    max_round=8
)

manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

# === Launch ===

# if __name__ == "__main__":
#     user_proxy.initiate_chat(
#         manager,
#         message="Find the most relevvant companies in the Food and Breweries.",
#     )


if __name__ == "__main__":
    print(cognism("Food", "Denmark"))
