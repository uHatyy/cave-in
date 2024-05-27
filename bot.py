import discord
import os
import random
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    if not os.path.exists("data/players"):
        os.makedirs("data/players")

@bot.command(name = "setcave")
async def setcave(ctx):
    cavedata = {}
    i = 1
    while i <= 10:
       cavedata[i] = random.randint(1, 100)
       i += 1
    cavedata[random.randint(0, 9)] = 101
    json.dump(cavedata, open('data/cavedata.json', "w"))       
    await ctx.respond("Done!") 

@bot.command(name = "mine", description = "Mine for loot in a cave!")
async def mine(ctx, cave: discord.Option(int)):
    id = str(ctx.author.id)
    PathToID = Path("data/players/" + id + ".json")
    if not PathToID.exists():
        PlayerItems ={
            "gold" : 0,
            "thulecite" : 0,
            "gemR" : 0,
            "gemB" : 0,
            "gemP" : 0,
            "gemO" : 0,
            "gemY" : 0,
            "gemG" : 0
        }
        json.dump(PlayerItems, open(PathToID, "w"))
    else:
        PlayerItems = json.load(open(PathToID, "r"))

    if cave > 0 and cave < 11:
        roll = json.load(open("data/cavedata.json", "r"))[str(cave)]
        if roll < 41:
            reward = "<:gold:1236493246826414111> 1 gold!"
            PlayerItems["gold"] += 1
        elif roll < 66:
            reward = "<:gold:1236493246826414111> 3 gold!"
            PlayerItems["gold"] += 3
        elif roll < 80:
            reward = "<:gold:1236493246826414111> 5 gold!"
            PlayerItems["gold"] += 5
        elif roll < 89:
            reward = "<:gold:1236493246826414111> 10 gold!"
            PlayerItems["gold"] += 10
        elif roll < 95:
            reward = "<:gold:1236493246826414111> 20 gold!"
            PlayerItems["gold"] += 20
        elif roll < 101:
            if random.randint(0, 1):
                PlayerItems["thulecite"] += 4
                reward = "<:thulecite:1236496891533852694> 4 thulecite!"
            else:
                gemRNG = random.randint(1, 6)
                if gemRNG == 1:
                    PlayerItems["thulecite"] += 2
                    PlayerItems["gemR"] += 1
                    reward = "<:thulecite:1236496891533852694> 2 thulecite and <:gemR:1236494017055952958> a red gem!"
                elif gemRNG == 2:
                    PlayerItems["thulecite"] += 2
                    PlayerItems["gemB"] += 1
                    reward = "<:thulecite:1236496891533852694> 2 thulecite and <:gemB:1236493950198485028> a blue gem!"
                elif gemRNG == 3:
                    PlayerItems["thulecite"] += 2
                    PlayerItems["gemP"] += 1
                    reward = "<:thulecite:1236496891533852694> 2 thulecite and <:gemP:1236494105631264858> a purple gem!"
                elif gemRNG == 4:
                    PlayerItems["thulecite"] += 2
                    PlayerItems["gemO"] += 1
                    reward = "<:thulecite:1236496891533852694> 2 thulecite and <:gemO:1236494152309542943> an orange gem!"
                elif gemRNG == 5:
                    PlayerItems["thulecite"] += 2
                    PlayerItems["gemY"] += 1
                    reward = "<:thulecite:1236496891533852694> 2 thulecite and <:gemY:1236494202687328366> a yellow gem!"
                else:
                    PlayerItems["thulecite"] += 2
                    PlayerItems["gemG"] += 1
                    reward = "<:thulecite:1236496891533852694> 2 thulecite and <:gemG:1236494250149937162> a green gem!"
        else:
            OldItems = list(PlayerItems.values())
            RNG = random.randint(1, 100)
            if RNG < 51:
                reps = 1
            elif RNG < 86:
                reps = 2
            else:
                reps = 3
            for i in range(reps):
                if random.randint(0, 1):
                    gemRNG = random.randint(1, 6)
                    if gemRNG == 1:
                        PlayerItems["thulecite"] += 2
                        PlayerItems["gemR"] += 1
                    elif gemRNG == 2:
                        PlayerItems["thulecite"] += 2
                        PlayerItems["gemB"] += 1
                    elif gemRNG == 3:
                        PlayerItems["thulecite"] += 2
                        PlayerItems["gemP"] += 1
                    elif gemRNG == 4:
                        PlayerItems["thulecite"] += 2
                        PlayerItems["gemO"] += 1
                    elif gemRNG == 5:
                        PlayerItems["thulecite"] += 2
                        PlayerItems["gemY"] += 1
                    else:
                        PlayerItems["thulecite"] += 2
                        PlayerItems["gemG"] += 1
                else:
                    PlayerItems["thulecite"] += 4
            RuinsRewards = []
            item = 0
            for i in OldItems:
                RuinsRewards.append(list(PlayerItems.values())[item] - OldItems[item])
                item += 1
            reward = str(RuinsRewards[1]) + "<:thulecite:1236496891533852694> thulecite"
            def GemRewards(index, gem, emoji):
                value = RuinsRewards[index]
                if value != 0:
                    if value == 1:
                        s = ""
                    else:
                        s = "s"
                    return " and " + str(value) + " " + emoji + " " + gem + s
                else:
                    return ""
            reward = reward + GemRewards(2, "red gem", "<:gemR:1236494017055952958>")
            reward = reward + GemRewards(3, "blue gem", "<:gemB:1236493950198485028>")
            reward = reward + GemRewards(4, "purple gem", "<:gemP:1236494105631264858>")
            reward = reward + GemRewards(5, "orange gem", "<:gemO:1236494152309542943>")
            reward = reward + GemRewards(6, "yellow gem", "<:gemY:1236494202687328366>")
            reward = reward + GemRewards(7, "green gem", "<:gemG:1236494250149937162>")
        json.dump(PlayerItems, open(PathToID, "w"))
        await ctx.respond("In cave " + str(cave) + ", you earned " + reward + ".")
    else:
         await ctx.respond("Enter a cave number between 1 and 10")

@bot.command(name = "stats", description = "Get the amount of items someone has")
async def stats(ctx, target: discord.User = None):
    if target == None:
        statsuser = ctx.author.id
    else:
        statsuser = target._user.id
    try:
        playerdata = open("data/players/" + str(statsuser) + ".json", "r+").read()
    except:
        playerdataexists = False
    else:
        playerdataexists = True

    if playerdataexists == True:
        playerdata = json.load(open("data/players/" + str(statsuser) + ".json", "r"))
        statrespond = str(await (bot.fetch_user(statsuser))) + "'s items:"
        def getplayerdata(stat, emoji):
            if playerdata[stat] != 0:
                return statrespond + "\n <:" + stat + ":" + str(emoji) + "> " + str(playerdata[stat]) + " " + stat 
            else:
                return statrespond
        statrespond = getplayerdata("gold", 1236493246826414111)
        statrespond = getplayerdata("thulecite", 1236496891533852694)
        statrespond = getplayerdata("gemR", 1236494017055952958)
        statrespond = getplayerdata("gemB", 1236493950198485028)
        statrespond = getplayerdata("gemP", 1236494105631264858)
        statrespond = getplayerdata("gemO", 1236494152309542943)
        statrespond = getplayerdata("gemY", 1236494202687328366)
        statrespond = getplayerdata("gemG", 1236494250149937162)
        await ctx.respond(statrespond)
    else:
        await ctx.respond("Invalid user or user hasnt participated in the game.")
    
bot.run(os.getenv('TOKEN'))
