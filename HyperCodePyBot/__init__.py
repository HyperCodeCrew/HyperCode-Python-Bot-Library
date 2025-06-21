# __init__.py
import discord
from discord.ext import commands
from discord import app_commands

from packaging import version

from typing import *

# Import utility modules
if __name__ != "__main__":
    from .utils.token_utils import *
    from .utils.embed_utils import *
    from .utils.webhook_utils import *
else:
    from utils.token_utils import *
    from utils.embed_utils import *
    from utils.webhook_utils import *

token = None  # Placeholder for the token, to be set later

# Ensure discord.py version is compatible
if version.parse(discord.__version__) < version.parse("2.0.0"):
    raise RuntimeError("HyperCodePyBot requires discord.py version 2.0.0 or higher.")

class HyperCodePyBot(commands.Bot):
    def __init__(self, command_prefix='!'):
        if command_prefix == "/": warn("Command prefix cannot be '/' as it is reserved for slash commands. Use a different prefix or no prefix at all. it is buggy it not show autocompletion in chat and not recommended.")
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.bot = self  # For compatibility with older code

        if not self.tree:
            # discord.py 2.0+ requires a CommandTree for slash commands
            self.tree = app_commands.CommandTree(self)
        self._token = None

    # === Lifecycle Events ===
    async def setup_hook(self) -> None:
        """Initial setup after the bot is ready."""
        await self.tree.sync()
        print("Commands synced with Discord!")
        if hasattr(self, 'hook') and self.hook.on_setup_hook:
            await self.hook.on_setup_hook()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        if hasattr(self, 'hook') and self.hook.on_ready:
            await self.hook.on_ready()

    async def on_command_error(self, ctx, error):
        await ctx.send(embed=embed_utils.create_embed("Error: Command failed", str(error), color=0xff0000))
        if hasattr(self, 'hook') and self.hook.on_command_error:
            await self.hook.on_command_error(ctx, error)
    
    async def on_interaction(self, interaction: discord.Interaction):
        """Handle interactions, such as slash commands."""
        if interaction.type == discord.InteractionType.application_command:
            await self.tree.process_interaction(interaction)
        if hasattr(self, 'hook') and self.hook.on_interaction:
            await self.hook.on_interaction(interaction)
    
    async def on_message(self, message: discord.Message):
        """Handle messages sent in channels."""
        if message.author == self.user:
            return
        await self.process_commands(message)
        if hasattr(self, 'hook') and self.hook.on_message:
            await self.hook.on_message(message)

    async def on_disconnect(self):
        """Handle bot disconnection."""
        print("Bot has disconnected.")
        if hasattr(self, 'hook') and self.hook.on_disconnect:
            await self.hook.on_disconnect()
    
    async def on_connect(self):
        """Handle bot connection."""
        print("Bot has connected.")
        if hasattr(self, 'hook') and self.hook.on_connect:
            await self.hook.on_connect()

    def run(self, new_token: Optional[str] = None):
        """Run the bot with the provided token."""
        global token
        
        # Priority: passed token > instance token > global token
        running_token = new_token or self._token or token
        
        if running_token is None:
            raise ValueError("Token is not set. Please load a token before running the bot.")
            
        # Update all token references
        self._token = running_token
        token = running_token
        
        super().run(running_token)

    def reboot_bot(self, callback: Optional[Callable[[], Any]] = None):
        """Reboot the bot."""
        print("Rebooting bot...")
        try:
            self.loop.run_until_complete(self.close())
            self.loop.run_until_complete(self.start(self._token))
            callback(True, "Reboot successful") if callback else None
        except Exception as e:
            print(f"Error rebooting bot: {e}")
            callback(False, str(e)) if callback else None

    def add_custom_command(self, name, function):
        """Add a custom prefix command to the bot."""
        self.add_command(commands.Command(function, name=name, help=function.__doc__))

    # === Token Methods (delegated to utils) ===
    @staticmethod
    def load_token_from_string(token_string):
        global token
        token = token_utils.load_token_from_string(token_string)
        return token

    @staticmethod
    def load_token_from_file(file_path):
        global token
        token = token_utils.load_token_from_file(file_path)
        return token

    @staticmethod
    def load_token_from_environment(env_var):
        global token
        token = token_utils.load_token_from_environment(env_var)
        return token

    @staticmethod
    def load_token_from_config(config_file, token_key):
        global token
        token = token_utils.load_token_from_config(config_file, token_key)
        return token

    @staticmethod
    def load_token_from_secret(secret_name):
        global token
        token = token_utils.load_token_from_secret(secret_name)
        return token
    
    class Member:
        @staticmethod
        def get_member(guild: discord.Guild, member_id: int):
            """Get a member by ID in a guild."""
            return guild.get_member(member_id)

        @staticmethod
        def get_members(guild: discord.Guild):
            """Get all members in a guild."""
            return guild.members

        @staticmethod
        def get_member_roles(member: discord.Member):
            """Get roles of a member."""
            return member.roles

        @staticmethod
        def add_role(member: discord.Member, role: discord.Role):
            """Add a role to a member."""
            return member.add_roles(role)

        @staticmethod
        def remove_role(member: discord.Member, role: discord.Role):
            """Remove a role from a member."""
            return member.remove_roles(role)

    class Channel:
        @staticmethod
        def get_channel(guild: discord.Guild, channel_id: int):
            """Get a channel by ID in a guild."""
            return guild.get_channel(channel_id)
        
        @staticmethod
        def get_channels(guild: discord.Guild):
            """Get all channels in a guild."""
            return guild.channels
        
        @staticmethod
        def create_text_channel(guild: discord.Guild, name: str, category: Optional[discord.CategoryChannel] = None):
            """Create a text channel in a guild."""
            return guild.create_text_channel(name, category=category)
        
        @staticmethod
        def create_voice_channel(guild: discord.Guild, name: str, category: Optional[discord.CategoryChannel] = None):
            """Create a voice channel in a guild."""
            return guild.create_voice_channel(name, category=category)
        
        @staticmethod
        def delete_channel(channel: discord.abc.GuildChannel):
            """Delete a channel."""
            return channel.delete()
        
        @staticmethod
        def edit_channel(channel: discord.abc.GuildChannel, **kwargs):
            """Edit a channel's properties."""
            return channel.edit(**kwargs)
        
        def move_channel(channel: discord.abc.GuildChannel, position: int):
            """Move a channel to a specific position."""
            return channel.edit(position=position)
        
    class Role:
        @staticmethod
        def get_role(guild: discord.Guild, role_id: int):
            """Get a role by ID in a guild."""
            return guild.get_role(role_id)

        @staticmethod
        def get_roles(guild: discord.Guild):
            """Get all roles in a guild."""
            return guild.roles

        @staticmethod
        def create_role(guild: discord.Guild, name: str, **kwargs):
            """Create a role in a guild."""
            return guild.create_role(name=name, **kwargs)

        @staticmethod
        def delete_role(role: discord.Role):
            """Delete a role."""
            return role.delete()

        @staticmethod
        def edit_role(role: discord.Role, **kwargs):
            """Edit a role's properties."""
            return role.edit(**kwargs)
        
    class Guild:
        @staticmethod
        def get_guild(guild_id: int):
            """Get a guild by ID."""
            return discord.utils.get(discord.Client.guilds, id=guild_id)

        @staticmethod
        def get_guilds(client: discord.Client):
            """Get all guilds the bot is in."""
            return client.guilds

        @staticmethod
        def create_guild(name: str):
            """Create a new guild."""
            return discord.Guild.create(name=name)

    class VoiceChannel:
        @staticmethod
        def join_vc(channel: discord.VoiceChannel):
            """Join a voice channel."""
            return channel.connect()
        def leave_vc(channel: discord.VoiceChannel):
            """Leave a voice channel."""
            return channel.disconnect()
        def play_audio(channel: discord.VoiceChannel, source: str):
            """Play audio in a voice channel."""
            if not channel.guild.voice_client:
                return channel.connect()
            return channel.guild.voice_client.play(discord.FFmpegPCMAudio(source))
        def stop_audio(channel: discord.VoiceChannel):
            """Stop audio playback in a voice channel."""
            if channel.guild.voice_client and channel.guild.voice_client.is_playing():
                return channel.guild.voice_client.stop()
            return None
        def pause_audio(channel: discord.VoiceChannel):
            """Pause audio playback in a voice channel."""
            if channel.guild.voice_client and channel.guild.voice_client.is_playing():
                return channel.guild.voice_client.pause()
            return None
        def resume_audio(channel: discord.VoiceChannel):
            """Resume audio playback in a voice channel."""
            if channel.guild.voice_client and channel.guild.voice_client.is_paused():
                return channel.guild.voice_client.resume()
            return None
        def get_vc_status(channel: discord.VoiceChannel):
            """Get the status of the voice channel."""
            if channel.guild.voice_client:
                return {
                    "is_connected": channel.guild.voice_client.is_connected(),
                    "is_playing": channel.guild.voice_client.is_playing(),
                    "is_paused": channel.guild.voice_client.is_paused(),
                    "channel": channel.guild.voice_client.channel.name if channel.guild.voice_client.channel else None
                }
            return {"is_connected": False, "is_playing": False, "is_paused": False, "channel": None}
        def get_vc_channel(channel: discord.VoiceChannel):
            """Get the voice channel the bot is connected to."""
            if channel.guild.voice_client:
                return channel.guild.voice_client.channel
            return None
        def get_vc_members(channel: discord.VoiceChannel):
            """Get the members in the voice channel."""
            if channel.guild.voice_client:
                return [member.name for member in channel.guild.voice_client.channel.members]
            return []
        def kick_member(channel: discord.VoiceChannel, member: discord.Member):
            """Kick a member from the voice channel."""
            if channel.guild.voice_client and member in channel.guild.voice_client.channel.members:
                return member.move_to(None)
            return None
        def move_member(channel: discord.VoiceChannel, member: discord.Member, target_channel: discord.VoiceChannel):
            """Move a member to another voice channel."""
            if channel.guild.voice_client and member in channel.guild.voice_client.channel.members:
                return member.move_to(target_channel)
            return None

class WebhookUtils:
    @staticmethod
    def add_webhook(url):
        return webhook_utils.add_webhook(url)

    @staticmethod
    def send_webhook(webhook, content):
        return webhook_utils.send_webhook(webhook, content)

    @staticmethod
    def send_embed(webhook, embed):
        return webhook_utils.send_embed(webhook, embed)

    # === Embed Utility Methods ===
    @staticmethod
    def create_embed(title, description=None, color=0x000000):
        return embed_utils.create_embed(title, description, color)

    @staticmethod
    def set_embed_title(embed, title):
        return embed_utils.set_embed_title(embed, title)

    @staticmethod
    def set_embed_description(embed, description):
        return embed_utils.set_embed_description(embed, description)

    @staticmethod
    def set_embed_color(embed, color):
        return embed_utils.set_embed_color(embed, color)

    @staticmethod
    def set_embed_url(embed, url):
        return embed_utils.set_embed_url(embed, url)

    @staticmethod
    def set_embed_timestamp(embed, timestamp=None):
        return embed_utils.set_embed_timestamp(embed, timestamp)

    @staticmethod
    def set_embed_fields(embed, fields):
        return embed_utils.set_embed_fields(embed, fields)

    @staticmethod
    def add_embed_field(embed, name, value, inline=True):
        return embed_utils.add_embed_field(embed, name, value, inline)

    @staticmethod
    def set_embed_footer(embed, text, icon_url=None):
        return embed_utils.set_embed_footer(embed, text, icon_url)

    @staticmethod
    def set_embed_footer_text(embed, text):
        return embed_utils.set_embed_footer_text(embed, text)

    @staticmethod
    def set_embed_footer_icon(embed, icon_url):
        return embed_utils.set_embed_footer_icon(embed, icon_url)

    @staticmethod
    def set_embed_thumbnail(embed, url):
        return embed_utils.set_embed_thumbnail(embed, url)

    @staticmethod
    def set_embed_image(embed, url):
        return embed_utils.set_embed_image(embed, url)

    @staticmethod
    def set_embed_author(embed, name, url=None, icon_url=None):
        return embed_utils.set_embed_author(embed, name, url, icon_url)

    @staticmethod
    def set_embed_author_name(embed, name):
        return embed_utils.set_embed_author_name(embed, name)

    @staticmethod
    def set_embed_author_url(embed, url):
        return embed_utils.set_embed_author_url(embed, url)

    @staticmethod
    def set_embed_author_icon(embed, icon_url):
        return embed_utils.set_embed_author_icon(embed, icon_url)