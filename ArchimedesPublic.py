###################################################################################################
###################################################################################################
# Developer: Henry Winkleman
# File: playground.py
# Description: Creates a Discord bot with a few commands.
###################################################################################################
###################################################################################################
import discord #For Discord interactions
import time #For counters
import random #For RNG
import asyncio #For asynchronus I/O interaction through Discord
from discord.ext import commands #Allows for bot commands.

#Bot initialization.
bot = commands.Bot(command_prefix="$")
name = "Archimedes"
hunger = 5 #Range is 0-10
lastFeeding = time.time()

#Events
@bot.event
async def on_ready():
    print("{0.user} has landed, connection made at {1}.".format(bot, time.time()))

#Commands
@bot.command(name="ping")
async def some_crazy_function_name(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def bomb(ctx):
  timer = 10
  while timer:
    await ctx.send("{0} second(s) remaining.".format(timer))
    time.sleep(1) 
    timer -= 1
  else:
    await ctx.send("Bomb has detonated.")

###################################################################################################
# Developer: Henry Winkleman
# Command name: sass
# Description: Repeats the string but with "No, " in front of it.
# Parameters: *args - All words that accompany the call.
###################################################################################################
@bot.command()
async def sass(ctx, *args):
  await ctx.send("No, {}".format(" ".join(args)))


###################################################################################################
# Developer: Henry Winkleman
# Command name: angrybot
# Description: Repeats every word in *args in lowercase, with the last in uppercase.
# Parameters: *args - All words that accompany the call.
###################################################################################################
@bot.command()
async def angrybot(ctx, *args):
  size = len(args)  #Determines array size.
  idx=0
  while size:
    if size == 1: #For the last word, become uppercase.
      await ctx.send("{0}".format(args[idx].upper()))
    else: #Every other word is lowecase.
      await ctx.send("{0}".format(args[idx].lower()))
    idx += 1
    size -= 1


###################################################################################################
# Developer: Henry Winkleman
# Command name: fibBomb
# Description: Creates a timed game that requires 4 keys based on the Fibonacci sequence.
# Parameters: difficulty - User entered difficulty for the timer.
###################################################################################################
@bot.command()
async def fibBomb(ctx, difficulty):

  ###########################################################################
  ################################DEFINITIONS################################
  ###########################################################################
  #Returns time for chosen difficulty.
  def addTime(difficulty):
    difficulty = difficulty.lower() #Allows for all variations of capitalization.
    if difficulty == "easiest":
      return 30.0
    elif difficulty == "easy":
      return 20.0
    elif difficulty == "medium":
      return 15.0
    elif difficulty == "hard":
      return 10.0
    elif difficulty == "hardest":
      return 7.5
    else:
      return 5.0
    
  #Checks the user input against the lock.
  def diffuse(attempt):
    key = [int(x) for x in attempt.content.split()] #Separates the message content into list of ints.
    #Checks key against lock.
    if key[0] == FibLock[2] and key[1] == FibLock[3] and key[2] == FibLock[4] and key[3] == FibLock[5]:
      return True
    else: #Failure raised exception that detonates bomb.
      raise Exception
  ###########################################################################
  ##############################END DEFINITIONS##############################
  ###########################################################################

  #Creates Fibonacci sequence lock.
  FibLock = [random.randint(1, 5), random.randint(1, 5)] #Two random integers to start sequence,
  for x in range(2, 6): #Then 4 more are appended following the sequence's definition.
    nextSeq = FibLock[x-1] + FibLock[x-2]
    FibLock.append(nextSeq)
  

  #Game start.
  await ctx.send("Tick tock. Keys are {0} and {1}.".format(FibLock[0], FibLock[1]))
  timer = addTime(difficulty) #Determines timer length.
  await ctx.send("You have {0} seconds.".format(timer))
  startCounter = time.time()  #Records start time.
  try:
    await bot.wait_for('message', check=diffuse, timeout=timer) #Waits for user message within time limit.
  except asyncio.TimeoutError:  #If time limit is passed, detonate.
    await ctx.send("BOOM. you dead.")
  except: #If user input was wrong, detonate.
    await ctx.send ("BOOM. you dead.")
  else:
    endCounter = time.time() - startCounter #Calculate time to input the correct key.
    await ctx.send("Bomb diffused in {0} second(s), you live.".format(round(endCounter,2)))


###################################################################################################
# Developer: Henry Winkleman
# Command name: feed
# Description: Archimedes may eat what the user gives them.
###################################################################################################
@bot.command()
async def feed(ctx):
  
  ###########################################################################
  ################################DEFINITIONS################################
  ###########################################################################
  async def give(hungerSimplified):
    #Allows for global variables to be edited.
    global hunger
    global lastFeeding 

    await ctx.send("What do you want to feed {0}?".format(name))
    food = await bot.wait_for('message')  #User chooses food.
    food = food.content.lower()           #Food is formatted for text.
    #Output is dependent on the hunger level.
    if (hungerSimplified == "starving"):
      await ctx.send("{0} devours the {1}.".format(name, food))
    elif (hungerSimplified == "hungry"):
      await ctx.send("{0} feverishly pecks at the {1}.".format(name, food))
    elif (hungerSimplified == "neutral"):
      await ctx.send("{0} eats the {1}.".format(name, food))
    elif (hungerSimplified == "wellfed"):
      await ctx.send("{0} hesitantly pecks at the {1}.".format(name, food))
    else: #Implies "full"
      await ctx.send("{0} can't eat any more.".format(name))
    
    #If not full, increases hunger and updates most recent feeding time.
    if hungerSimplified != "full":
      hunger += 1
      lastFeeding = time.time()
  ###########################################################################
  ##############################END DEFINITIONS##############################
  ###########################################################################
      
  #Allows for global variables to be edited.
  global hunger

  #Determines hunger based on last feeding.
  timeSinceFed = int(time.time() - lastFeeding)
  hunger -= round(timeSinceFed/900) #Decreases hunger by one for every 15 minutes since feeding.

  #Simplifies the hunger.
  if hunger < 0:
    hunger = 0
    hungerSimplified = "starving"
  elif 0 < hunger and hunger <= 3:
    hungerSimplified = "hungry"
  elif 3 < hunger and hunger <= 6:
    hungerSimplified = "neutral"
  elif 6 < hunger and hunger <= 9:
    hungerSimplified = "wellfed"
  else: #Assumes hunger is 10.
    hungerSimplified = "full"
  await give(hungerSimplified)


#Visualize a nine box board (A-C, 1-3)
  #2-D array
#Be able to have three-value variable
  #Int value, 0 for empty 1-2 for player
#Compute what is the next best space
  #Determine strategic value for every unused space
#Protocol for going first/second
  #Random, choice is still functional after first move
###################################################################################################
# Developer: Henry Winkleman
# Command name: tictactoe
# Description: Plays a game of tictactoe.
###################################################################################################
@bot.command()
async def tictactoe(ctx):
  await ctx.send("Starting tic tac toe game.")

  ###########################################################################
  ################################DEFINITIONS################################
  ###########################################################################
  def playerChoice(choice):
    format = list(choice.content.upper())
    if format[0] == 'A':
      targetC = 0
    elif format[0] == 'B':
      targetC = 1
    elif format[0] == 'C':
      targetC = 2
    else:
      pass
    if format[1] == '3':
      targetR = 0
    elif format[1] == '2':
      targetR = 1
    elif format[1] == '1':
      targetR = 2
    else:
      pass
    board[targetR][targetC] = 'X'
    return True


  async def outputBoard(board):
    await ctx.send("Board:A    B     C\n\
        #########\n\
    3  # {0} # {1} # {2} #\n\
        #########\n\
    2  # {3} # {4} # {5} #\n\
        #########\n\
    1  # {6} # {7} # {8} #\n\
        #########\n".format(board[0][0], board[0][1], board[0][2], 
    board[1][0], board[1][1], board[1][2], 
    board[2][0], board[2][1], board[2][2]))

  def validation(board):
    winCondition = [0 for _ in range(8)] #0-2 vertical starting from left, 3-5 horizontal top-down, 6 left diag, 7 right diag
    for i in range(len(board)): #change to static 3
      for j in range(len(board[i])):
        if board[i][j] == 'X':
          if i == 0:
            if j == 0:
              winCondition[6] += 1
            elif j == 2:
              winCondition[7] += 1
            winCondition[3] += 1
          elif i == 1:
            if j == 1:
              winCondition[6] += 1
              winCondition[7] += 1
            winCondition[4] += 1
          elif i == 2:
            if j == 0:
              winCondition[7] += 1
            elif j == 2:
              winCondition[6] += 1
            winCondition[5] += 1
          if j == 0:
            winCondition[0] += 1
          elif j == 1:
            winCondition[1] += 1
          elif j == 2:
            winCondition[2] += 1
    for idx in range(8):
      if winCondition[idx] == 3:
        return 1
    return 0
  ###########################################################################
  ##############################END DEFINITIONS##############################
  ###########################################################################

      

  #Intitializations
  board = [["   "]*3 for _ in range(3)] #3x3 2-D array.
  gameComplete = 0 #0 for unfinished, 1 for win, 2 for loss, 3 for tie.

  while gameComplete == 0:
    await outputBoard(board)
    await ctx.send("Where will you place your check?")
    await bot.wait_for("message", check=playerChoice)
    gameComplete = validation(board)
  #Final output
  await outputBoard(board)

#bot mind possibilities
#Focus on strategic value of each space and how many possible win conditions there are
#use validation() results to block the player



bot.run("NO-ID", bot=True)