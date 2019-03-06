import arcpy
import os
import sys

scripts_folder = os.path.join(os.path.dirname(__file__), 'Scripts')
sys.path.append(scripts_folder)

# Use importlib to force reload to pick up my changes
# ---------------------------------------------------
import importlib

import swisshs
import historicd

importlib.reload(swisshs)
importlib.reload(historicd)
# ---------------------------------------------------

from swisshs import SwissHillshade
from historicd import HistoricDots


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Viz tools"
        self.alias = "viztools"

        # List of tool classes associated with this toolbox
        self.tools = [SwissHillshade, HistoricDots]
