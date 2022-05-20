from ._anvil_designer import PlayerListTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PlayerList(PlayerListTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
  def tbPlayerNum_pressed_enter(self, **event_args):
    # Find row in datatable that corresponds to row of new number entered
    player = app_tables.players.get_by_id(self.item.get_id())
    # Update datatable with this number
    player['Number'] = self.tbPlayerNum.text