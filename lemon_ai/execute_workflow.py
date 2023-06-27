import uuid
from loguru import logger
from langchain.llms.base import BaseLLM
from langchain.agents import initialize_agent, AgentType
from lemon_ai.get_integrations import get_apis_from_env
from lemon_ai.cito_api_wrapper import CitoAPIWrapper
from lemon_ai.cito_toolkit import CitoToolkit

def execute_workflow(llm: BaseLLM, prompt_string: str):

    logfile_path = "output.log"
    logger.remove(handler_id=None)
    logger.add(logfile_path, format="{time} - {extra[session_id]} - {extra[operation_name]}")

    api_keys_dict, access_tokens_dict = get_apis_from_env()
    session_id = uuid.uuid4()

    cito_wrapper = CitoAPIWrapper()
    toolkit = CitoToolkit.from_cito_api_wrapper(cito_wrapper, api_keys_dict, access_tokens_dict, logger, str(session_id))
    tools = toolkit.get_tools()

    prompt = f"Your task is '{prompt_string}'. Focus on the ordering of the tasks given. Do not use a workflow unless it is mentioned. Give your action input as a valid JSON object where the keys are the params and the values are the value for each input parameter. If a param is optional and you have not been given a value, do not include that field in the input. Your final answer should give a brief conversational overview of what you did."

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
    )

    agent.run(prompt)
