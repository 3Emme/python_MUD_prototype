#{TYPE:{LEVEL:{NUMBER:"EQUIP"}}}

#name[] /ATK /DEF /weight /HP /slot /type /DMG /tactics{}

# LEVEL 1 WEAPONS
w1 = {"name":["Long Wooden Staff","Carved Wooden Staff"],"ATK":3,"DEF":5,"weight":3,"HP":3,"slot":"both hands","type":"weapon","DMG":1,"tactics":{"aggressive":None,"defensive":"block","evasive":None}}

w2 = {"name":["Short Knife","Rusted Knife"],"ATK":5,"DEF":3,"weight":3,"HP":3,"slot":"one hand","type":"weapon","DMG":2,"tactics":{"aggressive":None,"defensive":None,"evasive":"backstab"}}

w3 = {"name":["Metallic Hammer","Spiked Hammer"],"ATK":2,"DEF":1,"weight":3,"HP":3,"slot":"both hands","type":"weapon","DMG":3,"tactics":{"aggressive":"power smash","defensive":None,"evasive":None}}

w4 = {"name":["Blunt Short Sword","Rusted Short Sword"],"ATK":4,"DEF":3,"weight":3,"HP":3,"slot":"one hand","type":"weapon","DMG":3,"tactics":{"aggressive":"blade thrust","defensive":"parry","evasive":None}}

# LEVEL 1 ARMOR
a1 = {"name":["Leather Helmet","Padded Hood"],"ATK":0,"DEF":3,"weight":2,"HP":10,"slot":"head","type":"armor","DMG":0}

a2 = {"name":["Leather Tunic","Padded Gerkin"],"ATK":0,"DEF":3,"weight":2,"HP":10,"slot":"body","type":"armor","DMG":0}

a3 = {"name":["Leather Pants","Padded Leggings"],"ATK":0,"DEF":3,"weight":2,"HP":10,"slot":"legs","type":"armor","DMG":0}

a4 = {"name":["Leather Boots","Padded Shoes"],"ATK":0,"DEF":3,"weight":2,"HP":10,"slot":"feet","type":"armor","DMG":0}

random_equip = {"weapon":{1:{1:w1,2:w2,3:w3,4:w4},2:{}},"armor":{1:{1:a1,2:a2,3:a3,4:a4},2:{}}}
