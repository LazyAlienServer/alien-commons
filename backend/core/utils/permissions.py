def is_moderator(user):
    return user.is_moderator


def is_the_author(user, obj):
    return user.id == obj.author_id
