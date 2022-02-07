from discord_webhook import DiscordWebhook, DiscordEmbed


def monitor_attendance(lesson):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/940240657413468230/eLhWgAvnVu0mOdwmp79XFumlChQT8HrrADQtU8InnXR9WveXtvulKdtyYm-MUCnrI8GJ')

    embed = DiscordEmbed(title='✅ Lesson attended', color='339441')
    embed.set_timestamp()
    embed.add_embed_field(name="Lesson", value=lesson, inline=False)


    webhook.add_embed(embed)

    webhook.execute()

