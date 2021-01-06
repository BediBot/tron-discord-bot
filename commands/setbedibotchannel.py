import discord

from commands import _embedMessage, _mongoFunctions, _dueDateMessage, _checkrole, _util


async def set_bedi_bot_channel(ctx: discord.Message, client: discord.Client):
    # Checks if user is admin or bot owner
    if not (_checkrole.author_has_role(ctx, _mongoFunctions.get_settings(ctx.guild.id)['admin_role']) or _util.author_is_bot_owner(ctx)):
        replyEmbed = _embedMessage.create("SetBediBotChannel Reply", "Invalid Permissions", "red")
        await ctx.channel.send(embed = replyEmbed)
        return

    await ctx.channel.purge(limit = None)

    if _mongoFunctions.get_settings(ctx.guild.id)['due_dates_enabled']:
        dueDateEmbeds = {}
        dueDateMessages = {}

        for stream in _mongoFunctions.get_settings(ctx.guild.id)['streams']:
            dueDateEmbeds[stream] = _embedMessage.create("Stream {0} Due Dates Message".format(stream), "Temporary Message", "green")
            dueDateMessages[stream] = await ctx.channel.send(embed = dueDateEmbeds[stream])
            await dueDateMessages[stream].pin()
            _mongoFunctions.set_due_date_message_id(ctx.guild.id, stream, dueDateMessages[stream].id)

        await _dueDateMessage.edit_due_date_message(client)

    _mongoFunctions.set_bedi_bot_channel_id(ctx.guild.id, ctx.channel.id)

    # Purge all unpinned messages
    await ctx.channel.purge(limit = None, check = lambda msg: not msg.pinned)
