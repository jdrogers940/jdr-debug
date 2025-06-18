from langgraph_sdk import Auth

auth = Auth()

@auth.authenticate
async def authorize(headers: dict, path: str) -> Auth.types.MinimalUserDict:
    return {
        "identity": "employee id",
        "current": "josh",
        "is_authenticated": True,
    }
