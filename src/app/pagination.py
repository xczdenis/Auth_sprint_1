import math

from flask import request
from pydantic import BaseModel

from config import settings


class PaginatedPage(BaseModel):
    total_count: int
    total_pages: int
    next_page: int | None
    prev_page: int | None
    results: list

    def serialize_results(self):
        self.results = [item.to_dict() for item in self.results]


def paginate_list(
    page_size: int, page_number: int, results: list, total_count: int | None = None
) -> PaginatedPage:
    total_count = total_count or len(results)
    total_pages = 0
    if total_count > 0:
        total_pages = math.ceil(total_count / page_size)

    next_page = page_number + 1 if page_number < total_pages else None
    prev_page = None
    if page_number and page_number > 1:
        prev_page = page_number - 1
        if prev_page > total_pages:
            prev_page = total_pages

    start = (page_number - 1) * page_size
    end = start + page_size
    portion = results[start:end]

    return PaginatedPage(
        total_count=total_count,
        total_pages=total_pages,
        next_page=next_page,
        prev_page=prev_page,
        results=portion,
    )


def get_pagination_params(default_page_size: int | None = None) -> tuple[int, int]:
    default_pagesize = default_page_size or settings.PAGINATOR.page_size
    page_size = request.args.get(settings.PAGINATOR.page_size_query_path) or default_pagesize
    page_number = request.args.get(settings.PAGINATOR.page_number_query_path) or 1
    return int(page_number), int(page_size)
