from discord.ext import commands
import config

def is_ceo():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            return config.ceo in roles or config.equipeSuperior in roles
        return commands.check(predicate)

def is_adm():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if config.ceo in roles or config.equipeSuperior in roles: return True
            return config.adm in roles
        return commands.check(predicate)

def is_staff():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if config.ceo in roles or config.equipeSuperior in roles: return True
            return config.staff in roles
        return commands.check(predicate)

def is_embaixador():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if config.ceo in roles or config.equipeSuperior in roles: return True
            if config.staff in roles or config.adm in roles: return True
            return config.embaixador in roles
        return commands.check(predicate)

def is_aea():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if config.ceo in roles or config.equipeSuperior in roles: return True
            return config.aea in roles
        return commands.check(predicate)


def in_correct_channel(channel_ids:list):
        async def predicate(ctx):
            for channel_id in channel_ids:
                if channel_id == ctx.message.channel.id: return True
            return False
        return commands.check(predicate)





def aceitar_emblema(reacterRoles):
    roles = [role.name for role in reacterRoles]
    if config.ceo in roles: return True
    if "Equipe Superior" in roles: return True
    if "Administrador" in roles: return True
    return False