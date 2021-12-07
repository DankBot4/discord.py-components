from typing import List

from discord import Client, File, Message 
from discord.http import Route

from .component import Button
from .utils import _form_files

__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self, bot: Client):
        self.bot = bot

    def edit_response(
        self, interaction_token: str, data: dict, files: List[File] = None
    ):
        route = Route(
            "PATCH",
            f"/webhooks/{self.bot.user.id}/{interaction_token}/messages/@original",
        )

        if files is not None:
            return self.bot.http.request(
                route, data=_form_files(data, files), files=files
            )
        else:
            return self.bot.http.request(
                route,
                json=data,
            )

    def initial_response(
        self,
        interaction_id: int,
        interaction_token: str,
        data: dict,
        files: List[File] = None,
    ):
        route = Route(
            "POST",
            f"/interactions/{interaction_id}/{interaction_token}/callback",
        )

        if files is not None:
            return self.bot.http.request(
                route, data=_form_files(data, files), files=files
            )
        else:
            return self.bot.http.request(
                route,
                json=data,
            )
    def click_button(self, msg: Message, button: Button):
        route = Route("POST", 'interactions/')
        data = {"component_type": 2, "custom_id": str(button.id)}
        values = {"application_id": "270904126974590976", "channel_id": str(msg.channel.id), "type": "3", "data": data,
             "guild_id": str(msg.guild.id), "message_flags": 1, "message_id": str(msg.id)}

        return self.bot.http.request(route, json=values)