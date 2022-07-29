from django.contrib import messages


def is_slug_a_number(request, slug):
    """
    Takes in a WSGIRequest and a slug and returns a boolean result of trying to
    cast the slug to an int. Uses the messages framework to report result to
    user.

    Primary key (PK) is used as the slug. If a string was entered as the slug
    and not checked prior to the PK being referenced in the view, an internal
    server error would occur.

    Args:
        request (WSGIRequest): Request object required to construct message
        slug (str): Slug used in url

    Returns:
        bool: Result of type casting slug to int
    """
    print(type(request), type(slug))
    try:
        int(slug)
    except ValueError:
        messages.error(
            request,
            (
                "URL not valid (see below), did you enter this manually?"
                "<br><br>"
                f"'{request.META['HTTP_HOST']}{request.path_info}'"
                "<br><br>"
                "Please try using links provided by the site navigation."
            ),
        )
        return False
    return True
