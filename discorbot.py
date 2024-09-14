import discord
import datetime
from zoneinfo import ZoneInfo
from discord import app_commands
from discord.ext.commands import Bot
from fantasybot import getAllForWeek, createTeamTableFromDiscord, getMatchupFromWeekAndButton, createScheduleFromWeekAndTwoButtons,createStandings
from secrets import getLeagueID, getDiscordGuildID, getDiscordSecret
leagueIDA = getLeagueID()[0]
leagueIDB = getLeagueID()[1]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = Bot(command_prefix='/', intents=intents)

class MySubView(discord.ui.View):
    def __init__(self, w:int, bg:int):
            super().__init__(timeout=None)
            self.week = w
            self.buttonGame = bg
    @discord.ui.button(label="📅", style=discord.ButtonStyle.primary, emoji="1️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button1_callback(self, interaction,button):
        await interaction.response.defer()
        team, week = createScheduleFromWeekAndTwoButtons(leagueIDA,leagueIDB,self.week,self.buttonGame,1)
        #await interaction.response.send_message(file=discord.File(r'./images/schedule'+str(team)+'-week'+str(week)+'.png'),ephemeral =True)
        await interaction.followup.send(file=discord.File(r'./images/schedule'+str(team)+'-week'+str(week)+'.png'),ephemeral =True)
    
    @discord.ui.button(label="📅", style=discord.ButtonStyle.primary, emoji="2️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button2_callback(self, interaction,button):
        await interaction.response.defer()
        team, week = createScheduleFromWeekAndTwoButtons(leagueIDA,leagueIDB,self.week,self.buttonGame,2)
        await interaction.followup.send(file=discord.File(r'./images/schedule'+str(team)+'-week'+str(week)+'.png'),ephemeral =True) 
    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def button3_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week , self.buttonGame)
        view=MySubView(self.week,self.buttonGame)
        await interaction.followup.edit_message(interaction.message.id,content = 'Last updated: ' + datetime.datetime.now(ZoneInfo("America/Chicago")).ctime(), attachments=[discord.File(r'./images/button'+str(self.buttonGame)+'-week'+str(self.week)+'Matchups.png')], view=view)
    
class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    
    def __init__(self, w:int):
            super().__init__(timeout=None)
            self.week = w
            
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="1️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button1_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week , 1)
        view=MySubView(self.week,1)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(1)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
        
    
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="2️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button2_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 2)
        view=MySubView(self.week,2)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(2)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="3️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button3_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 3)
        view=MySubView(self.week,3)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(3)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="4️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button4_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 4)
        view=MySubView(self.week,4)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(4)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="5️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button5_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 5)
        view=MySubView(self.week,5)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(5)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="6️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button6_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 6)
        view=MySubView(self.week,6)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(6)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="7️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button7_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 7)
        view=MySubView(self.week,7)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(7)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="8️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button8_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 8)
        view=MySubView(self.week,8)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(8)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="9️⃣") # Create a button with the label "😎 Click me!" with color Blurple
    async def button9_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 9)
        view=MySubView(self.week,9)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(9)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="🔟") # Create a button with the label "😎 Click me!" with color Blurple
    async def button10_callback(self, interaction,button):
        await interaction.response.defer()
        getMatchupFromWeekAndButton(leagueIDA,leagueIDB,self.week, 10)
        view=MySubView(self.week,10)
        await interaction.followup.send(file=discord.File(r'./images/button'+str(10)+'-week'+str(self.week)+'Matchups.png'), view=view,ephemeral =True)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji="🏆") # Create a button with the label "😎 Click me!" with color Blurple
    async def button11_callback(self, interaction,button):
        await interaction.response.defer()
        createStandings(leagueIDA,leagueIDB,self.week)
        await interaction.followup.send(file=discord.File(r'./images/standings-week'+str(self.week)+'.png'),ephemeral =True)
    @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji="🔄")
    async def button12_callback(self, interaction,button):
        await interaction.response.defer()
        getAllForWeek(leagueIDA,leagueIDB,self.week)
        view=MyView(self.week)
        
        #await interaction.response.edit_message(content='',delete_after=1)
        #await interaction.followup.send("FANTASY BOT\r\nIf the bot has been idle for awhile, the button interaction may fail initailly. Click the button again in 10 seconds.",file=discord.File(r'./images/week'+str(self.week)+'Matchups.png'), view = view ,silent=True)
        await interaction.followup.edit_message(interaction.message.id,content='FANTASY BOT\r\nLast updated: ' + datetime.datetime.now(ZoneInfo("America/Chicago")).ctime(), attachments=[discord.File(r'./images/week'+str(self.week)+'Matchups.png')], view = view)
        
    

@tree.command(
    name="week",
    description="Create display for weeks fantasy",
    guild=discord.Object(id=getDiscordGuildID()))
async def week(interaction, week:int):
    getAllForWeek(leagueIDA,leagueIDB,week)
    view=MyView(week)
    await interaction.response.send_message('FANTASY BOT\r\nLast updated: ' + datetime.datetime.now(ZoneInfo("America/Chicago")).ctime(),file=discord.File(r'./images/week'+str(week)+'Matchups.png'), view = view ,silent=True)

    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=getDiscordGuildID()))
    print("Ready!")

client.run(getDiscordSecret())
