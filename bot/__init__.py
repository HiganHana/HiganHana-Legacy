from discord import ApplicationContext

def has_roles(ctx : ApplicationContext, *rolenames):
    """
    Checks if the author of a message has any of the roles specified.
    """
    author = ctx.author
    roles_obj = author.roles
    for role in roles_obj:
        if role.name in rolenames:
            return True
    return False