import sys

def check_note(note_line):
  if "pandapaxxy" in note_line.lower():
    return False
  return True

def filter_lines(lines):
  current_note = ""
  keep_lines = True
  output = []
  for line in lines:
      if not line.startswith("dimwishlist:"):
        keep_lines = True
        current_note = ""
      if line.startswith("//notes:"):
        current_note = line
        keep_lines = check_note(current_note)
      if keep_lines:
        if check_note(line):
          output.append(line)
  return output
title_lines = """title: Trivial's subset of voltron
description:https://raw.githubusercontent.com/hysw/Destiny2/main/wishlist/voltron_subset.txt

"""
lines = []
with open(sys.argv[1], encoding="utf-8") as listfile:
  lines = [line.strip("\n") for line in listfile]
lines = filter_lines(lines)
with open(sys.argv[2], encoding="utf-8", mode="w") as listfile:
  listfile.write(title_lines)
  for line in lines:
    listfile.write(line)
    listfile.write("\n")