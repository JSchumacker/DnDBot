import discord
from discord.ext import commands
import os
import random
import string
import requests
import json

description = '''Dungeons & Discord Bot'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')

@bot.event
async def on_command_error(error, ctx):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.message.channel.send('Use !help for info.')

@bot.command(pass_context=True)
async def roll(ctx, roll : str):
  """Rolls dice using #d# format, example: !roll 3d6"""
  
  resultTotal = 0
  resultString = ''
  try:
      try: 
          #Splits input #d# into separate int values under numDice and diceVal
          numDice = roll.split('d')[0]
          diceVal = roll.split('d')[1]
      except Exception as e:
          #If input does not follow #d# format, print error
          print(e)
          await ctx.send("Format has to be in #d# %s." % ctx.message.author.name)
          return

      if int(numDice) > 500:
          #If numDice value entered is over 500, print error
          await ctx.send("Cannot handle that many dice %s." % ctx.message.author.name)
          return
      
      #Print to user "Rolling 'number of dice' d'dice max value' for 'User'"
      await ctx.send("Rolling %s d%s for %s" % (numDice, diceVal, ctx.message.author.name))
      rolls, limit = map(int, roll.split('d'))

      #Loops the number of rolls requested by user for the dice maximum asked for
      for r in range(rolls):
          number = random.randint(1, limit)
          resultTotal = resultTotal + number
          
          if resultString == '':
              resultString += str(number)
          else:
              resultString += ', ' + str(number)
      
      #If rolling 1 die of any value, print result
      if numDice == '1':
          #Print "@User 'dice emoji'"
          #Result: Die number rolled
          await ctx.send(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString)
      #If rolling more than 1 die, print result and total
      else:
          #Print "@User 'dice emoji'"
          #Result: Dice numbers rolled
          #Total: Total of dice rolled
          await ctx.send(ctx.message.author.mention + "  :game_die:\n**Result:** " + resultString + "\n**Total:** " + str(resultTotal))

  except Exception as e:
      print(e)
      return

@bot.command(pass_context=True)
async def item(ctx, *, itemID : str):
  """Calls item info. e.g !item Abacus"""

  if(itemID): #Checks if itemID is a valid input
    #Replaces any white space in itemID with '-' for API call
    itemID = itemID.replace(' ', '-').lower()

    #Calls the requested item using response function and itemID input
    response = requests.get("https://www.dnd5eapi.co/api/equipment/" + itemID)

    #Takes response and converts to json text
    output = json.loads(response.text)

    #Dictionary calls within the json output variable, sets call to a variable for printing purposes
    name = output.get('name')
    weight = output.get('weight')

    equipment_category = output.get('equipment_category')
    equipment_name = equipment_category.get('name')

    cost_category = output.get('cost')
    cost_price = cost_category.get('quantity')
    cost_unit = cost_category.get('unit')

    description_category = output.get('desc')

    #Print statement for name of item, equipment type, weight, cost and unit, and description of item
    await ctx.send(f'{name}: {equipment_name}, Weight: {weight}, Cost: {cost_price} {cost_unit}, Description: {description_category}')

  else:
    await ctx.send("No Item found with ID: " + itemID) #Default if item not found in API

@bot.command(pass_context=True)
async def mitem(ctx, *, mItemID : str):
  """Calls magic item info. e.g !mitem Flame Tongue"""

  if(mItemID): #Checks if mItemID is a valid input
    #Replaces any white space in itemID with '-' for API call
    mItemID = mItemID.replace(' ', '-').lower()

    #Calls the requested item using response function and itemID input
    response = requests.get("https://www.dnd5eapi.co/api/magic-items/" + mItemID)

    #Takes response and converts to json text
    output = json.loads(response.text)

    #Dictionary calls within the json output variable, sets call to a variable for printing purposes
    name = output.get('name')

    equipment_category = output.get('equipment_category')
    equipment_name = equipment_category.get('name')

    description_category = output.get('desc')

    #Print statement for name of item, equipment category, and description of magic item
    await ctx.send(f'{name}: Equipment Category: {equipment_name}, Description: {description_category}')

  else:
    await ctx.send("No Item found with ID: " + mItemID) #Default if magic item not found in API
    
@bot.command(pass_context=True)
async def align(ctx, *, alignment : str):
  """Calls alignment info. e.g !align Chaotic Good"""

  if(alignment): #Checks if alignment is a valid input
    #Replaces any white space in itemID with '-' for API call
    itemID = alignment.replace(' ', '-').lower()

    #Calls the requested item using response function and alignment input
    response = requests.get("https://www.dnd5eapi.co/api/alignments/" + itemID)

    #Takes response and converts to json text
    output = json.loads(response.text)

    #Dictionary calls within the json output variable, sets call to a variable for printing purposes
    name = output.get('name')
    abbrev = output.get('abbreviation')
    description_category = output.get('desc')

    #Print statement for name of alignment, the alignment's abbreviation, and description
    await ctx.send(f'{name}: Abbreviation: {abbrev}, Description: {description_category}')

  else:
    await ctx.send("No alignment found named: " + alignment) #Default if alignment not found in API

@bot.command(pass_context=True)
async def classes(ctx, inClass : str):
  """Calls class info. e.g !classes Barbarian"""

  if(inClass): #Checks if inClass is a valid input
    #Replaces any white space in itemID with '-' for API call
    inClass = inClass.replace(' ', '-').lower()

    #Calls the requested item using response function and alignment input
    response = requests.get("https://www.dnd5eapi.co/api/classes/" + inClass)

    #Takes response and converts to json text
    output = json.loads(response.text)

    #Dictionary/list calls within the json output variable, sets call to a variable for printing purposes
    cName = output.get('name')
    hitDie = output.get('hit_die')

    subClass = output.get('subclasses')
    subClassName = subClass[0].get('name')

    #Try except used in case class called does not have spell casting modifier(s)
    try:
      spellCasting = output.get('spellcasting')
      spellCastingInfo = spellCasting.get('info')
      spellCastingAb = spellCastingInfo[3].get('name')
      spellCastingDesc = spellCastingInfo[3].get('desc')

      spellCastingAbility = spellCasting.get('spellcasting_ability')
      spellCastingName = spellCastingAbility.get('name')
      await ctx.send(f'{cName}: Subclass: {subClassName}, Hit Dice: d{hitDie}, Spellcasting Ability: {spellCastingName}, {spellCastingAb}: {spellCastingDesc}')
    except: #If class doesn't have spelcasting modifier(s), use this print statement
      await ctx.send(f'{cName}: Subclass: {subClassName}, Hit Dice: d{hitDie}')
  else:
    await ctx.send("No class found named: " + inClass) #Default if class not found in API


bot.run(os.getenv('TOKEN'))