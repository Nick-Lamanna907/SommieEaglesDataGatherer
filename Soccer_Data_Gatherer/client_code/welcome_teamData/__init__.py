from ._anvil_designer import welcome_teamDataTemplate
from anvil import *
from .PlayerList import PlayerList
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

###### Adds player to the datatable ######
def addPlayer(date, team, name, passS, passF):
  app_tables.player_data.add_row(
    date=date,
    team=team,
    name=name,
    passS=passS,
    passF=passF
  )

class welcome_teamData(welcome_teamDataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Start-up code
    # Set up date picker
    dp = self.dpRound
    dp.format = '%d/%m/%Y'
    dp.date = datetime.date.today()
    dp.max_date = '31 12 23'
    dp.min_date = '1 1 22'
    
    # Fill player list
    self.rpPlayerList.items = app_tables.players.search()

  def btnSubmit_click(self, **event_args):
    # Get all data from form
    nums = []
    names = []
    for player in self.rpPlayerList.items:
      if player['Playing'] == True:
        nums.append(player['Number'])
        names.append(player['Name'])
    date = str(self.dpRound.date)
    team = str(self.ddTeam.selected_value)
    
    # Search for duplicates in data table
    dateClash = len(app_tables.player_data.search(date=date))
    teamClash = len(app_tables.player_data.search(team=team))
    
    # Add each player to the datatable using addPlayer(...)
    for player in self.rpPlayerList.items:
      if player['Playing'] == True:
        if dateClash != 0: # date is in table already
          if teamClash != 0: # team is in table already
            nameClash = len(app_tables.player_data.search(name=player['Name']))
            if nameClash != 0: # name is in table already
                print(date + ' ' + team + ' ' + player['Name'] + " - already in table")
            else: # number is not in table for chosen team and date
                addPlayer(date, team, player['Name'], [], [])
          else: # team is not already in table for chosen date
              addPlayer(date, team, player['Name'], [], [])
        else: # date is not in table
            addPlayer(date, team, player['Name'], [], [])
        
    # Open the next form
    open_form('main_playerData', team=team, date=date, names=names, nums=nums)
        
      




