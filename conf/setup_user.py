def setup_demo_user(user):
    """
    The django2ynh DEMO use the Django admin. So we need a "staff" user ;)
    """
    user.is_staff = True
    user.save()
    return user
