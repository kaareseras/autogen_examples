import autogen
from dotenv import load_dotenv
import os

load_dotenv()

config_list_gpt4 = [
    {
        'model': 'gpt-4o-2',
        'api_key': os.getenv('API_KEY'),
        'base_url': os.getenv('API_BASE'),
        'api_type': 'azure',
        'api_version': '2024-08-01-preview',
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
sdr = autogen.AssistantAgent(
    name="SDR",
    system_message="SDR. State your name first. Check the plan and provide feedback from a sales perspective. Focus on identifying potential leads and researching market opportunities. Suggest how to approach the market and prioritize leads. SDR needs to approve the plan.",
    llm_config=gpt4_config
)
 
caller = autogen.AssistantAgent(
    name="Caller",
    system_message="Caller. State your name first. Check the plan and provide feedback from a sales perspective. Focus on identifying potential leads and researching market opportunities. Suggest how to optimize the call to the customer to engage effectively.",
    llm_config=gpt4_config,
)
 
seller = autogen.AssistantAgent(
    name="Seller",
    system_message="Seller. Check the plan and provide feedback from a overall sales perspective on how to increace the cahnce of success.",
    llm_config=gpt4_config,
 
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Be Creative within reason.
      Revise the plan based on feedback from admin, SDR, caller,seller and critic, until admin approval.
      Explain the plan first. be clear about the problem, solution, and how to get concrette leads.
      In the end provide a summary of the plan.
    ''',
    llm_config=gpt4_config,
)
 
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, sdr, caller, seller, planner, critic], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message=""" Contoso is a large pump manufacturer looking to innovate in the market with new digital enabled pumps and services to improve customers' sustainability. Make 3 concrete leads for the sellers to reach out to, and provide needed info to improve the successful sale of the new products?
    """,
)