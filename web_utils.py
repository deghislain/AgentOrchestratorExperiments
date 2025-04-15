

def retrieve_agent_capabilities(data_dict):
    """
    Retrieves all agents capabilities.

    Args:
        data_dict (dict): The agents capabilities.

    Returns:
        str: A formatted string containing agents capabilities.
    """
    return "\n".join(f"{i+1}. Agent name: {key}. \n Agent Capabilities: {value.capabilities[0]}" for i, (key, value) in enumerate(data_dict.items()))
