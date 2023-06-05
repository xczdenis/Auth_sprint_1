from dataclasses import dataclass

from flask import url_for


@dataclass
class URLBuilder:
    api_prefix: str = "api"
    api_version: str = "v1"

    def build_url(self, path_to_route: str = "", **url_params):
        return url_for(
            "{api_prefix}.{api_version}.{path}".format(
                api_prefix=self.api_prefix, api_version=self.api_version, path=path_to_route
            )
        )


url_builder_v1: URLBuilder = URLBuilder(api_version="v1")
