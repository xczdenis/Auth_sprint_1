from typing import Optional

PAGINATED_RESPONSE_STRUCTURE = {
    "count": int,
    "total_pages": int,
    "next": Optional[int],
    "prev": Optional[int],
    "results": list,
}
