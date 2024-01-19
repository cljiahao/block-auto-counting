import json
from .directories import directory

class readSettings(directory):
    def __init__(self):
        super().__init__()
        with open('JSON/settings.json') as f:
            setData = json.load(f)
            self.setData = setData
            self.address = setData['Address']
            self.credentials = setData['Credentials']
            self.config = setData['Config']
            self.tolerance = setData['Tolerance']
            self.chipSize = setData['Chip Size']
            self.accuracy = setData['Accuracy']

        with open('JSON/misc.json') as g:
            miscData = json.load(g)
            self.miscData = miscData
            self.color = miscData['Color']
            self.font = miscData['Font']
            self.highlight = miscData['Highlight']

        with open('JSON/staticnames.json') as h:
            namesData = json.load(h)
            self.defCode = namesData['Defect Code']
            self.defBlack = namesData['Defect Black']
            self.defSticker = namesData['Defect Sticker']
