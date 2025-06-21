from discord_webhook import DiscordWebhook

class webhook_utils:
    def add_webhook(url):
        return DiscordWebhook(url=url)
    
    def send_webhook(webhook, content):
        webhook.content = content
        response = webhook.execute()
        return response.status_code == 204
    
    def send_embed(webhook, embed):
        webhook.embeds = [embed]
        response = webhook.execute()
        return response.status_code == 204