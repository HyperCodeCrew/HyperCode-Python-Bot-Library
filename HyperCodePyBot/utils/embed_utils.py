import discord
from datetime import datetime

class embed_utils:
    def create_embed(title, description=None, color=0x000000):
        return discord.Embed(title=title, description=description, color=color)
    
    def set_embed_title(embed, title):
        embed.title = title
        return embed
    def set_embed_description(embed, description):
        embed.description = description
        return embed
    def set_embed_color(embed, color):
        embed.color = color
        return embed
    def set_embed_url(embed, url):
        embed.url = url
        return embed
    def set_embed_timestamp(embed, timestamp=None):
        embed.timestamp = timestamp or datetime.utcnow()
        return embed
    def set_embed_fields(embed, fields):
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        return embed
    def add_embed_field(embed, name, value, inline=True):
        embed.add_field(name=name, value=value, inline=inline)
        return embed
    
    def set_embed_footer(embed, text, icon_url=None):
        embed.set_footer(text=text, icon_url=icon_url)
        return embed
    
    def set_embed_footer_text(embed, text):
        icon_url = embed.footer.icon_url if embed.footer else None
        embed.set_footer(text=text, icon_url=icon_url)
        return embed
    
    def set_embed_footer_icon(embed, icon_url):
        text = embed.footer.text if embed.footer else None
        embed.set_footer(text=text, icon_url=icon_url)
        return embed
    
    def set_embed_thumbnail(embed, url):
        embed.set_thumbnail(url=url)
        return embed
    
    def set_embed_image(embed, url):
        embed.set_image(url=url)
        return embed
    
    def set_embed_author(embed, name, url=None, icon_url=None):
        embed.set_author(name=name, url=url, icon_url=icon_url)
        return embed
    
    def set_embed_author_name(embed, name):
        author = embed.author
        embed.set_author(
            name=name,
            url=getattr(author, 'url', None),
            icon_url=getattr(author, 'icon_url', None)
        )
        return embed
    
    def set_embed_author_url(embed, url):
        author = embed.author
        embed.set_author(
            name=getattr(author, 'name', None),
            url=url,
            icon_url=getattr(author, 'icon_url', None)
        )
        return embed
    
    def set_embed_author_icon(embed, icon_url):
        author = embed.author
        embed.set_author(
            name=getattr(author, 'name', None),
            url=getattr(author, 'url', None),
            icon_url=icon_url
        )
        return embed
    