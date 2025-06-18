from langgraph_sdk import Auth

auth = Auth()

@auth.authenticate
def get_user_info(authorization: str) -> dict:
    return {
        "identity": "employee id",
        "current": "josh",
        "is_authenticated": True,
    }
