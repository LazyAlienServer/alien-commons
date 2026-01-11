def is_moderator(user):
    return getattr(user, "is_moderator", False)


def is_the_author(user, obj):
    return user.id == obj.author_id
