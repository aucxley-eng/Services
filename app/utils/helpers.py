def paginate(query, page, per_page):
    """
    Helper function to paginate a SQLAlchemy query.
    Returns a dictionary with data and pagination info.
    """
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": pagination.items,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }