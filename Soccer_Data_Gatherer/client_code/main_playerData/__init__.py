from ._anvil_designer import main_playerDataTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

# TO USE:
#    - while timer is at 0, sub on starting 11
#    - click start
#    - pause game at half time

matchTime = 0            # match time in seconds
sommieScore = 0          # eagles score
otherScore = 0           # other teams score
matchStart = False       # indicates the start button has been clicked when True
selectedPlayer = ""      # the selected player 
date = ""
team = ""
plyrs = []               # a list of all active players (list of classes)
btns = []                # a list of all the player buttons

class matchPlayer:
    def __init__(self, name, date, team):
      self.name = name
      self.date = date
      self.team = team
      self.passS = []
      self.passF = []
      self.shotS = []
      self.shotF = []
      self.yellowCard = []
      self.redCard = []
      self.subOn = []
      self.subOff = []
      self.assist = []
      self.goal = []

# (done) make a class for each player with each key being a stat
# (done) append the matchTime to the list allocated to each key
# (done) every save click fill the data table with the classes 
# label to indicate the last action (eg/ Lamanna passS)
# (done) add the rest of the stats (keep very simple - save, pass, goal, card, sub on, sub off)
# (done) add in other team goal button, and label to show scoreline
# (done) timeline of major events (subs, cards, goals) - make name come up next to goals and cards 
# undo feature

class main_playerData(main_playerDataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    # Get all variables passed into this form 
    global date, team, btns, plyrs
    team = properties['team']
    date = properties['date']
    names = properties['names']
    nums = properties['nums']
    
    # Create list of all the column panels and add player buttons to each one
    cols = [
      self.cp1, self.cp2, self.cp3, self.cp4, self.cp5, self.cp6, self.cp7, self.cp8
    ]
    player = 0
    for name in names:
      txt = names[player] + "\n" + str(nums[player]) # text for button
      btn = Button(text=txt, background='blue', align='full', foreground='yellow') # button for player
      btn.set_event_handler('click', self.playerBtnClick) # set the button click function
      btns.append(btn) # add the button to the global btns list
      name = matchPlayer(name,date,team) # create a class for the current player
      plyrs.append(name) # add this players class to the plyrs list
      cols[player%8].add_component(btn) # add the button to the appropriate column
      player += 1 # ensures next button is added to the next column
    
  ###### Put all classes into the datatable ######'
  def loadData(self, **event_args):
    global date, team, sommieScore, otherScore
    for plyr in plyrs:
      row = app_tables.player_data.get(date=date, team=team, name=plyr.name)
      row['passS'] = plyr.passS
      row['passF'] = plyr.passF
      row['shotS'] = plyr.shotS
      row['shotF'] = plyr.shotF
      row['yellowCard'] = plyr.yellowCard 
      row['redCard'] = plyr.redCard 
      row['subOn'] = plyr.subOn 
      row['subOff'] = plyr.subOff 
      row['assist'] = plyr.assist 
      row['goal'] = plyr.goal
      if sommieScore > otherScore:
        row['win'] = True
      else:
        row['win'] = False
  
  ###### When the timer increments, change the clock ######
  def timer_tick(self, **event_args):
    if matchStart == True:
      global matchTime
      matchTime += 1
      minutes = str(math.floor(matchTime/60))
      seconds = str(matchTime%60)
      self.lblTime.text = minutes + ":" + seconds

  ###### When the button that controls the timer is clicked, change match start variable ######
  def btnTimerControl_click(self, **event_args):
    global matchStart
    if matchStart == False:
      matchStart = True
      self.btnTimerControl.text = "Pause"
      self.btnTimerControl.background = "red"
    else:
      matchStart = False
      self.btnTimerControl.text = "Start"
      self.btnTimerControl.background = "blue"
      
  ###### When player button is clicked, change colour and update selected player ######
  def playerBtnClick(self, **event_args):
    btn = event_args['sender']
    global selectedPlayer
    if btn.background == 'yellow':
      self.resetBtn()
    else:
      self.resetBtn()
      btn.background = 'yellow'
      btn.foreground = 'blue'
      selectedPlayer = btn.text.split("\n")[0]
  
  ###### Resets selectedPlayer and all buttons ######
  def resetBtn(self):
    global selectedPlayer
    for btn in btns:
      btn.background = 'blue'
      btn.foreground = 'yellow'
    selectedPlayer = ""
    
  ###### Updates scoreline ######
  def updateScore(self):
    global sommieScore, otherScore
    self.lblScore.text = "SESC " + str(sommieScore) + " - " + str(otherScore)
  
  ###### Add timestamp to selectedPlayer.passS ######
  def btnPassS_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.passS.append(matchTime)
        self.resetBtn()
        
  ###### Add timestamp to selectedPlayer.passF ######       
  def btnPassF_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.passF.append(matchTime)
        self.resetBtn()
   
  ###### Add timestamp to selectedPlayer.shotS ######
  def btnShotS_click(self, **event_args):
    global selectedPlayer, matchTime, sommieScore
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.shotS.append(matchTime)
    self.resetBtn()
        
  ###### Add timestamp to selectedPlayer.shotF ######
  def btnShotF_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.shotF.append(matchTime)
        self.resetBtn()

  ###### Add timestamp to selectedPlayer.subOn ######
  def btnSubOn_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.subOn.append(matchTime)
    text = self.lblTimeline.text + "\n" + str(math.floor(matchTime/60)) + "' - ON " + selectedPlayer
    self.lblTimeline.text = text  
    self.resetBtn()
        
  ###### Add timestamp to selectedPlayer.subOff ######
  def btnSubOff_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.subOff.append(matchTime)
    text = self.lblTimeline.text + "\n" + str(math.floor(matchTime/60)) + "' - OFF " + selectedPlayer
    self.lblTimeline.text = text  
    self.resetBtn()

  ###### Add timestamp to selectedPlayer.yellowCard ######
  def btnYel_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.yellowCard.append(matchTime)
    text = self.lblTimeline.text + "\n" + str(math.floor(matchTime/60)) + "' - Y. C. " + selectedPlayer
    self.lblTimeline.text = text  
    self.resetBtn()
        
  
  ###### Add timestamp to selectedPlayer.redCard ######
  def btnRed_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.redCard.append(matchTime)
    text = self.lblTimeline.text + "\n" + str(math.floor(matchTime/60)) + "' - R. C. " + selectedPlayer
    self.lblTimeline.text = text
    self.resetBtn()

  ###### Add timestamp to selectedPlayer.assist ######
  def btnAssist_click(self, **event_args):
    global selectedPlayer, matchTime
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.assist.append(matchTime)
        self.resetBtn()

  ###### Add 1 to oppositions score ######
  def btnOppGoal_click(self, **event_args):
    global otherScore, matchTime
    otherScore += 1
    text = self.lblTimeline.text + "\n" + str(math.floor(matchTime/60)) + "' - Opp Goal"
    self.lblTimeline.text = text
    self.updateScore()

  ##### Reset clock back to 45' #####
  def btnHalfTime_click(self, **event_args):
    global matchTime
    if matchTime > 45*60:
      matchTime = 45*60

  ##### Add one to Sommie Goal #####
  def btnOurGoal_click(self, **event_args):
    global selectedPlayer, matchTime, sommieScore
    for plyr in plyrs:
      if plyr.name == selectedPlayer:
        plyr.goal.append(matchTime)
        self.resetBtn()
    sommieScore += 1
    self.updateScore()
    text = self.lblTimeline.text + "\n" + str(math.floor(matchTime/60)) + "' - Eagles Goal"
    self.lblTimeline.text = text
    







