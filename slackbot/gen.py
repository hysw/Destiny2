msgs = {
    "raid": """
Root of Nightmares (!ron) 
King's Fall (!kf)
Vow of the Disciple (!vow)
Vault of Glass (!vog)
Deep Stone Crypt (!dsc)
Garden of Salvation (!gos)
~Crown of Sorrow~
~Scourge of the Past~
Last Wish (!lw)
~Spire of Stars~
~Eater of Worlds~
~Leviathan~
""",
    "ron": """
Root of Nightmares (!ron)
!ron-maps:
  E1: https://i.imgur.com/tMEMWQ8.jpeg
  E2: https://i.imgur.com/GLV7lb8.jpeg
  E3: https://i.imgur.com/xgqQT42.jpeg
  E4: https://i.imgur.com/U0ppm4M.jpeg
Other maps:
!ron-e2
!ron-e3
"""
}

print()
for cmd, msg in msgs.items():
    print("!%s:" % cmd, msg.strip().replace("\n", "\\n"))
    print()
