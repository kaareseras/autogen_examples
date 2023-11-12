import autogen
from dotenv import load_dotenv
import os

load_dotenv()

config_list_gpt4 = [
    {
        'model': 'gpt-4-32k',
        'api_key': os.getenv('API_KEY'),
        'api_base': os.getenv('API_BASE'),
        'api_type': 'azure',
        'api_version': '2023-07-01-preview',
    }
]

gpt4_config = {
    "seed": 39,  # change the seed for different trials
    "temperature": 0.5,
    "config_list": config_list_gpt4,
    "timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
   name="Admin",
   system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
   code_execution_config=False,
)
cto = autogen.AssistantAgent(
    name="CTO",
    system_message="CTO. State your name first. Check the plan and provide feedback from a technical persepctive. Suggest how to build the solution. CTO needs to approve the plan.",
    llm_config=gpt4_config
)
 
cfo = autogen.AssistantAgent(
    name="CFO",
    system_message="CFO. State your name first. Check the plan and provide feedback from a financial persepctive. Suggest how to build the business case. CFO needs to approve the plan.",
    llm_config=gpt4_config,
)
 
cpo = autogen.AssistantAgent(
    name="CPO",
    system_message="CPO. State your name first. Check the plan and provide feedback from a people persepctive. Suggest what capabilities are required to deliver the plan.",
    llm_config=gpt4_config,
 
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Be Creative within reason.
      Revise the plan based on feedback from admin, CFO, CPO and critic, until admin approval.
      Explain the plan first. be clear about the problem, solution, and how to measure success.
      In the end provide a summary of the plan.
    ''',
    llm_config=gpt4_config,
)
 
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, cto, cfo, cpo, planner, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message=""" Contoso is a midsize startup in the tech industry. Contoso is looking for the next product to develop and launch in the series of GPT enabled devices. What should this next device be, and what is the paln for development and launch?
    """,
)