from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class OAuthProviders:
    yandex = "yandex"
    mail = "mail"
    google = "google"

    @classmethod
    def is_valid(cls, provider_name: str) -> bool:
        ok = False
        for attr in cls.__dict__.keys():
            if attr[:2] != "__":
                value = getattr(cls, attr)
                if value == provider_name:
                    ok = True
                    break
        return ok
