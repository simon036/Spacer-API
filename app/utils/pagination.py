def paginate(query, schema, page, per_page):
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": schema.dump(paginated.items),
        "total": paginated.total,
        "pages": paginated.pages,
        "current_page": paginated.page
    }