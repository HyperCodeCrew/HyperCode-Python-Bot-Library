# __init__.py
import discord 
from discord.ext import commands
from discord import app_commands
from typing import Optional, Callable, Any, List
import PyBot.utils.token_utils as token_utils
import PyBot.utils.embed_utils as embed_utils
import PyBot.utils.webhook_utils as webhook_utils

token = None  # Placeholder for the token, to be set later

class PyBot(commands.Bot):
    def __init__(self, command_prefix='!'):
        if command_prefix == "/":
            raise ValueError("Command prefix cannot be '/' as it is reserved for slash commands. Use a different prefix or no prefix at all. it is buggy and not recommended.")
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
        await ctx.send(f"An error occurred: {error}")
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

    def reboot_bot(self):
        """Reboot the bot."""
        print("Rebooting bot...")
        self.loop.create_task(self.close())
        self.loop.run_until_complete(self.start(self._token))

    # === Command Methods ===
    def add_slash_command(self, name: str, description: str, function: Callable[..., Any], options: Optional[list] = None):
        """Create a slash command.
        
        Args:
            name: The name of the command
            description: The description of the command
            function: The function to execute when the command is called
            options: Optional list of app_commands.Option for additional parameters
        """
        @app_commands.command(name=name, description=description)
        async def slash_command(interaction: discord.Interaction):
            await function(interaction)

        if options:
            for option in options:
                slash_command.add_option(option)

        self.tree.add_command(slash_command)
        return slash_command


    def add_slash_group(self, name: str, description: str):
        """Create a slash command group.
        
        Args:
            name: The name of the command group
            description: The description of the group
        """
        return app_commands.Group(name=name, description=description)

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