from pydantic import Field
from typing import List
import json


class AgentOutput:
    agent_name: str = Field(description="Agent name")
    agent_output: List[str] = Field(description="Agent returns output")


def retrieve_agent_capabilities(data_dict):
    """
    Retrieves all agents capabilities.

    Args:
        data_dict (dict): The agents capabilities.

    Returns:
        str: A formatted string containing agents capabilities.
    """
    return "\n".join(
        f"{i + 1}. Agent name: {key}. \n Agent Capabilities: {value.capabilities[0]}" for i, (key, value) in
        enumerate(data_dict.items()))


def parse_output(output: str) -> json:
    print("start")
    prefix = ""
    for index in range(len(output)):
        #print(prefix)
        if output[index] != '{':
            prefix += output[index]
        else:
            break

    output = output[len(prefix):].strip()
    try:
        # Parse the JSON string
        data = json.loads(output)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

