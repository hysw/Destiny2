import pathlib
import urllib.request
import filter_subset


repo = pathlib.Path(__file__).resolve().parent.parent.parent

def load_wishlist(filename):
  with open(filename, encoding="utf-8") as listfile:
    lines = [line.strip("\n") for line in listfile]
  return lines

def store_wishlist(filename, lines, title_lines = None):
  with open(filename, encoding="utf-8", mode="w") as listfile:
    if title_lines is not None:
      listfile.write(title_lines)
      if not title_lines.endswith("\n"):
        listfile.write("\n")
    for line in lines:
      listfile.write(line)
      listfile.write("\n")

mappings = {
  "jat/just-another-team-mnk.txt": "github://dsf000z/JAT-wishlists-bundler/main/bundles/DIM/just-another-team-mnk.txt",
  "voltron/choosy_voltron.txt": "github://48klocs/dim-wish-list-sources/master/choosy_voltron.txt",
  "voltron/voltron.txt": "github://48klocs/dim-wish-list-sources/master/voltron.txt",
  "voltron/LICENSE": "github://48klocs/dim-wish-list-sources/master/LICENSE"
}


def sync():
  for k, v in mappings.items():
    v = v.replace("github://", "https://raw.githubusercontent.com/")
    output = repo.joinpath("sync", *k.split("/"))
    urllib.request.urlretrieve(v, output)

def update_voltron_subset():
  title_lines = """title: Trivial's subset of voltron
description:https://raw.githubusercontent.com/hysw/Destiny2/main/wishlist/voltron_subset.txt\n\n"""
  src = load_wishlist(repo.joinpath("sync", "voltron", "voltron.txt"))
  out = filter_subset.filter_lines(src)
  store_wishlist(repo.joinpath("wishlist", "voltron_subset.txt"), out, title_lines=title_lines)

def main():
  sync()
  update_voltron_subset()

if __name__ == "__main__":
  main()
