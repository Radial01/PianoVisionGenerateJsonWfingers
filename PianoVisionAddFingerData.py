# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 01:44:21 2023
@author: jiler
"""

import json
import xml.etree.ElementTree as ET

class XmlNote:
    def __init__(self, pitch, octave, alter, finger):
        self.pitch = pitch
        self.octave = octave
        self.alter = alter
        self.finger = finger

def getNextPitch(XmlNote):
    _xmlNote = XmlNote
    if(_xmlNote.pitch == "A"):
        _xmlNote.pitch = "G"
    elif(_xmlNote.pitch == "B"):
        _xmlNote.pitch = "A"
    elif(_xmlNote.pitch == "C"):
        _xmlNote.pitch = "B"
    elif(_xmlNote.pitch == "D"):
        _xmlNote.pitch = "C"
    elif(_xmlNote.pitch == "E"):
        _xmlNote.pitch = "D"
    elif(_xmlNote.pitch == "F"):
        _xmlNote.pitch = "E"
    elif(_xmlNote.pitch == "G"):
        _xmlNote.pitch = "F"
        _xmlNote.octave = 1
    _xmlNote.alter = 1
    return _xmlNote

xmlNotesRight = []
xmlNotesRightMod = []

xmlNotesLeft = []
xmlNotesLeftMod = []

# Opening JSON file
with open('input.json', 'r') as f:
    data = json.load(f)

# Opening and processing XML file
tree = ET.parse('input.xml')
root = tree.getroot()

# Process right hand notes
for notes in root[4].iter('note'):
    if (len(notes.findall('pitch')) > 0):
        if(len(notes.findall('pitch')[0].findall('step')) > 0):
            step = notes.findall('pitch')[0].findall('step')[0].text
            octave = notes.findall('pitch')[0].findall('octave')[0].text
            alter = 0
            if len(notes.findall('pitch')[0].findall('alter')) > 0:
                alter = notes.findall('pitch')[0].findall('alter')[0].text
            finger = 0
            notations = notes.findall('notations')
            if(len(notations) > 0):
                if(len(notations[0].findall('technical')) > 0):    
                    if len(notes.findall('notations')[0].findall('technical')[0].findall('fingering')) > 0:
                        finger = notes.findall('notations')[0].findall('technical')[0].findall('fingering')[0].text
            xmlNotesRight.append(XmlNote(step, octave, alter, finger))

# Process left hand notes
for notes in root[5].iter('note'):
    if (len(notes.findall('pitch')) > 0):
        if(len(notes.findall('pitch')[0].findall('step')) > 0):
            step = notes.findall('pitch')[0].findall('step')[0].text
            octave = notes.findall('pitch')[0].findall('octave')[0].text
            alter = 0
            if len(notes.findall('pitch')[0].findall('alter')) > 0:
                alter = notes.findall('pitch')[0].findall('alter')[0].text
            finger = 0
            notations = notes.findall('notations')
            if(len(notations) > 0):
                if(len(notations[0].findall('technical')) > 0):    
                    if len(notes.findall('notations')[0].findall('technical')[0].findall('fingering')) > 0:
                        finger = notes.findall('notations')[0].findall('technical')[0].findall('fingering')[0].text
            xmlNotesLeft.append(XmlNote(step, octave, alter, finger))

# Modify xmlNotesRightMod and xmlNotesLeftMod based on alterations
xmlNotesRightMod = xmlNotesRight
for i in xmlNotesRightMod:
    if(i.alter == "-1"):
        i = getNextPitch(i)

xmlNotesLeftMod = xmlNotesLeft
for i in xmlNotesLeftMod:
    if(i.alter == "-1"):
        i = getNextPitch(i)

# Update JSON data with XML data
for i in range(len(data['tracksV2']['right'])):
    for j in range(len(data['tracksV2']['right'][i]['notes'])):
        step = data['tracksV2']['right'][i]['notes'][j]['notePitch']
        octave = data['tracksV2']['right'][i]['notes'][j]['octave']
        xmlNote3 = XmlNote(step, octave, 0, 0)
        if "#" in step:
            xmlNote3.pitch = step[0]
            xmlNote3.alter = 1
        toremove = 0
        for k in xmlNotesRightMod:
            if(xmlNote3.pitch == k.pitch and str(xmlNote3.octave) == str(k.octave) and str(xmlNote3.alter) == str(k.alter)):
                data['tracksV2']['right'][i]['notes'][j]['finger'] = k.finger
                toremove = xmlNotesRightMod.index(k)
                break
        xmlNotesRightMod.remove(xmlNotesRightMod[toremove])

for i in range(len(data['tracksV2']['left'])):
    for j in range(len(data['tracksV2']['left'][i]['notes'])):
        step = data['tracksV2']['left'][i]['notes'][j]['notePitch']
        octave = data['tracksV2']['left'][i]['notes'][j]['octave']
        xmlNote3 = XmlNote(step, octave, 0, 0)
        if "#" in step:
            xmlNote3.pitch = step[0]
            xmlNote3.alter = 1
        toremove = 0
        for k in xmlNotesLeftMod:
            if(xmlNote3.pitch == k.pitch and str(xmlNote3.octave) == str(k.octave) and str(xmlNote3.alter) == str(k.alter)):
                data['tracksV2']['left'][i]['notes'][j]['finger'] = int(k.finger)
                toremove = xmlNotesLeftMod.index(k)
                break
        xmlNotesLeftMod.remove(xmlNotesLeftMod[toremove])

# Incorporate logic from the first script
# Update notes under 'right' key
if 'tracksV2' in data and 'right' in data['tracksV2']:
    id_counter = 0
    for entry in data['tracksV2']['right']:
        for note in entry['notes']:
            note['id'] = f'r{id_counter}'
            note['finger'] = note.get('finger', None)  # Preserve existing 'finger' if already set
            note['smp'] = None
            id_counter += 1


# Update notes under 'left' key
if 'tracksV2' in data and 'left' in data['tracksV2']:
    id_counter = 0
    for entry in data['tracksV2']['left']:
        for note in entry['notes']:
            note['id'] = f'r{id_counter}'
            note['finger'] = note.get('finger', None)  # Preserve existing 'finger' if already set
            note['smp'] = None
            id_counter += 1

# Serializing json
json_object = json.dumps(data, indent=4)

# Writing to output.json
with open("output.json", "w") as outfile:
    outfile.write(json_object)

# Closing file
f.close()
