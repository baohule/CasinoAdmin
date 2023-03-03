class URLs:
    """
    Generic method to create routers in FastAPI so they are added to the swagger doc.
    To use, add the route name as a string to the include list and your route will be built.
    """

    include = [
        "admin",
        "allocation",
        "auth",
        "comment",
        "feed",
        "files",
        "follow",
        "interest",
        "investment",
        "like",
        "portfolio",
        "post",
        "profile",
        "question",
        "reaction",
        "review",
        "search",
        "strategy",
        "tip",
        "topic",
        "trending",
        "update",
        "user",
    ]
