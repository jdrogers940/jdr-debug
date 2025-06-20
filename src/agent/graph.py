"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langchain_core.tools import tool


class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    my_configurable_param: str


@dataclass
class State:
    """Input state for the agent.

    Defines the initial structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    """

    changeme: str = "example"


stored_config = None

def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        langgraph_user = stored_config.get("configurable").get("langgraph_auth_user", {})
        if not langgraph_user:
            raise Exception("User not available")
        if not langgraph_user["is_authenticated"]:
            raise Exception("User is not authenticated")
        return func(*args, **kwargs)
    return wrapper

@tool
@authorize
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def call_model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Process input and returns output.

    Can use runtime configuration to alter behavior.
    """
    global stored_config
    stored_config = config
    langgraph_user = config.get("configurable").get("langgraph_auth_user", {})
    
    # Print all values and structure of langgraph_user
    print("=== langgraph_user variable details ===")
    print(f"Type: {type(langgraph_user)}")
    print(f"Value: {langgraph_user}")
    print(f"Boolean evaluation: {bool(langgraph_user)}")
    print(f"Dir: {dir(langgraph_user)}")
    
    # If it's a dictionary-like object, print all keys and values
    if hasattr(langgraph_user, '__dict__'):
        print(f"Attributes: {langgraph_user.__dict__}")
    
    # If it's a dictionary, print all items
    if isinstance(langgraph_user, dict):
        print("Dictionary items:")
        for key, value in langgraph_user.items():
            print(f"  {key}: {value}")
    
    if not langgraph_user:
        raise Exception("User not available")
    if not langgraph_user["is_authenticated"]:
        raise Exception("User is not authenticated")
    user = langgraph_user["current"]

    try:
        result = await multiply.invoke({"a": 2, "b": 3})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

    # TODO: Coerce to a dotdict in production
    print('identity', langgraph_user["identity"])
    print('is authenticated', langgraph_user["is_authenticated"])
    print('current', langgraph_user["current"])

    return {
        "changeme": "output from call_model. "
        f'Calling user - {user}'
    }


# Define the graph
graph = (
    StateGraph(State, config_schema=Configuration)
    .add_node(call_model)
    .add_edge("__start__", "call_model")
    .compile(name="New Graph")
)
