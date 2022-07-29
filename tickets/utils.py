def is_user_elevated_role(user):
    """
    Return boolean value based on user objects role attribute

    Args:
        user (SimpleLazyObject): Lazy loaded 'request.user' Object

    Returns:
        bool: Result of conditional statement
    """
    if (user.role == "administrator") or (user.role == "technician"):
        return True
    else:
        return False
