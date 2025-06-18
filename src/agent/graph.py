"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph


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


async def call_model(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Process input and returns output.

    Can use runtime configuration to alter behavior.
    """
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
    if not langgraph_user.is_authenticated:
        raise Exception("User is not authenticated")
    user = langgraph_user.current

    print('identity', langgraph_user.identity)
    print('is authenticated', langgraph_user.is_authenticated)
    print('current', langgraph_user.current)

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
