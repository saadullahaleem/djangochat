

def save_user_alias(*args, **kwargs):
    alias = kwargs['response'].get("displayName").split(" ")[0]
    user = kwargs.get("user")
    user.alias = alias
    user.save()