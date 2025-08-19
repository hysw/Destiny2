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