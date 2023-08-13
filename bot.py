# -------------- Invite Role Rewards ----------------------#
# This requires the Manage Roles and Manage Server permission. 
# This requires the 'members' privileged intent to function.
# The bots role must be above the role you want to award in the list at Server Settings -> Roles. 
# ---------------------------------------------------------

import discord

BOT_TOKEN = "PUT_YOUR_TOKEN_HERE"
REWARD_ROLE_NAME = "NAME OF ROLE TO AWARD" # Name of role awarded to user upon fulfilling invite criteria - case sensitive
REWARD_ROLE_CRITERIA = -1 # Number of invites user has to make to get the role.

class MyClient(discord.Client):


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


    async def get_total_invites(self , user, guild):
        total_invites = 0
        for invite in await guild.invites():
            if invite.inviter == user:
                total_invites += invite.uses
        return total_invites
    
    def has_reward_role(self, user, guild):
        member = guild.get_member(user.id)
        member_roles = list(map(lambda m: m.name,member.roles))
        if(REWARD_ROLE_NAME in member_roles):
            return True
        else:
            return False
        

    async def on_member_join(self, member):
        guild = member.guild
        invites = await guild.invites()
        inviters_checked = {} 
        for invite in invites:
            if(inviters_checked.get(invite.inviter,False) == True): # Avoid double checking a user if he has multiple invite links. 
                continue 
            elif(self.has_reward_role(invite.inviter, guild)):
                inviters_checked[invite.inviter] = True 
            else:
                inviters_checked[invite.inviter] = True 
                number_of_invites = await self.get_total_invites(invite.inviter, guild)
                if(number_of_invites >= REWARD_ROLE_CRITERIA):
                    role = discord.utils.get(guild.roles, name=REWARD_ROLE_NAME)
                    await guild.get_member(invite.inviter.id).add_roles(role)
            
intents = discord.Intents.default()
intents.members = True


client = MyClient(intents=intents)
client.run(BOT_TOKEN)