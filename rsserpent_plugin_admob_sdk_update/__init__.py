from rsserpent_rev.models import Persona, Plugin

from . import route


plugin = Plugin(
    name="rsserpent-plugin-admob-sdk-update",
    author=Persona(
        name="EkkoG",
        link="https://github.com/RSSerpent-Rev",
        email="beijiu572@gmail.com",
    ),
    prefix="/admob/sdk-update",
    repository="https://github.com/RSSerpent-Rev/rsserpent-plugin-admob-sdk-update",
    routers={route.path: route.provider},
)
