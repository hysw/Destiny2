type LICENSE > generated\wishlist.LICENSE
type ^
  src\title.txt src\section-line.txt ^
  src\trivial-wip.txt src\section-line.txt ^
  src\trivial\Neomuna.txt src\section-line.txt ^
  src\trivial\RAID-RON.txt src\section-line.txt ^
  src\trivial\S20.txt src\section-line.txt ^
  src\trivial-trash.txt src\section-line.txt ^
  > generated\wishlist.txt
  
type generated\wishlist.txt wishlist.txt

mkdir generated
type sync\voltron\LICENSE > generated\with_choosy_voltron.LICENSE
type ^
  src\title-merged.txt src\section-line.txt ^
  generated\wishlist.txt src\section-line.txt ^
  sync\voltron\choosy_voltron.txt src\section-line.txt ^
  > generated\with_choosy_voltron.txt
