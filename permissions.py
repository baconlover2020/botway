from discord.ext import commands

def is_ceo():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            return "CEO" in roles or "Equipe Superior" in roles
        return commands.check(predicate)

def is_adm():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if "CEO" in roles or "Equipe Superior" in roles: return True
            return "Administrador" in roles
        return commands.check(predicate)

def is_staff():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if "CEO" in roles or "Equipe Superior" in roles: return True
            return "Staff" in roles
        return commands.check(predicate)

def is_embaixador():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if "CEO" in roles or "Equipe Superior" in roles: return True
            return "Embaixadores" in roles
        return commands.check(predicate)

def is_aea():
        async def predicate(ctx):
            roles = [role.name for role in ctx.message.author.roles]
            if "CEO" in roles or "Equipe Superior" in roles: return True
            return "Equipe AeA" in roles
        return commands.check(predicate)


def in_correct_channel(channel_ids:list):
        async def predicate(ctx):
            for channel_id in channel_ids:
                if channel_id == ctx.message.channel.id: return True
            return False
        return commands.check(predicate)


canais_emblema = []
canais_furni = []
canais_icon = []
canais_buscar_mobi = []


def aceitar_emblema(reacterRoles):
    roles = [role.name for role in reacterRoles]
    if "CEO" in roles: return True
    if "Equipe Superior" in roles: return True
    if "Administrador" in roles: return True
    return False