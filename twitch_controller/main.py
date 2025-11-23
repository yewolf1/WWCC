import asyncio
import os
import sys

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.helper import first
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent
from twitchAPI.type import AuthScope
if __package__ is None or __package__ == "":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    from config import ensure_config, load_tokens, save_tokens
    from actions import run_action
else:
    from .config import ensure_config, load_tokens, save_tokens
    from .actions import run_action

async def run():
    config = ensure_config()
    client_id = config.get("client_id") or ""
    client_secret = config.get("client_secret") or ""
    if not client_id or not client_secret:
            print("client_id / client_secret manquants. Renseigne TWITCH_CLIENT_ID et TWITCH_CLIENT_SECRET dans le fichier .env")
            return
        
    scope_names = config.get("scopes") or ["CHANNEL_READ_REDEMPTIONS"]
    scopes = []
    for name in scope_names:
        value = getattr(AuthScope, name, None)
        if value is not None:
            scopes.append(value)
    if not scopes:
        print("Aucun scope valide dans twitch_config.json")
        return
    twitch = await Twitch(client_id, client_secret)
    tokens = load_tokens()
    if tokens:
        await twitch.set_user_authentication(
            tokens["access_token"],
            scopes,
            tokens.get("refresh_token"),
        )
        user_id = tokens["user_id"]
    else:
        auth = UserAuthenticator(twitch, scopes)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, scopes, refresh_token)
        user = await first(twitch.get_users())
        user_id = user.id
        tokens = {
            "access_token": token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "login": user.login,
            "display_name": user.display_name,
        }
        save_tokens(tokens)
    eventsub = EventSubWebsocket(twitch)

    async def on_redeem(event: ChannelPointsCustomRewardRedemptionAddEvent):
        try:
            title = event.event.reward.title
            user_input = event.event.user_input
            user_name = event.event.user_name      # pseudo affiché
        except AttributeError:
            data = event.to_dict()
            ev = data.get("event", {})
            reward = ev.get("reward", {})
            title = reward.get("title", "")
            user_input = ev.get("user_input", "")
            user_name = ev.get("user_name") or ev.get("user_login") or ""
        print("Reward:", title, "/", user_input, "/", user_name)
        run_action(title, user_input, user_name, config)

    eventsub.start()
    await eventsub.listen_channel_points_custom_reward_redemption_add(user_id, on_redeem)
    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await eventsub.stop()
        await twitch.close()


if __name__ == "__main__":
    asyncio.run(run())
