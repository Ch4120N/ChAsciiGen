import shutil
from pyfiglet import FigletFont

def showfonts():
    fonts = FigletFont.getFonts()
    term_width = shutil.get_terminal_size().columns
    numbered_fonts = [f"{i+1}. {font}" for i, font in enumerate(fonts)]
    max_len = max(len(item) for item in numbered_fonts) + 2
    cols = max(1, term_width // max_len)
    rows = [numbered_fonts[i:i+cols] for i in range(0, len(numbered_fonts), cols)]

    for row in rows:
        line = ""
        for item in row:
            line += item.ljust(max_len)
        print(' '*3, line)

if __name__ == "__main__":
    showfonts()
