import evdev
from pathlib import Path

for n in Path('dev/input').iterdir():
    print(n.absolute())