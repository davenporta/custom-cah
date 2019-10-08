import os
import sys

FRONTS = {'white': 'white front.png',
          'black': 'black front.png'}
MARGIN = 111  # px, safe-bleed + actual margin (300dpi)
TEXT_WIDTH = 600  # px, 300dpi (card width - 2 * MARGIN)
FONT = 'Helvetica-Neue-Bold'
SIZE = 72

def CardAgainstHumanity(text, background_color, back, out):
  """Writes text onto back, result is in out. color is the background color."""
  text_color = 'white' if background_color == 'black' else 'black'
  text = text.replace('"', '\\"')
  command = ('convert -font %s -pointsize %d -size %dx '
             '-background %s -transparent %s -fill %s "caption:%s" temp.png' % (
                 FONT, SIZE, TEXT_WIDTH, background_color, background_color, text_color, text.strip()))
  os.system(command)
  command = 'composite -geometry +%d+%d "%s" "%s" "%s"' % (
                MARGIN, MARGIN, 'temp.png', back, out)
  os.system(command)


def main():
  usage = 'Usage: %s <black|white> input.txt' % sys.argv[0]
  if len(sys.argv) != 3:
    sys.stderr.write(usage)
    return
  if sys.argv[1] not in ('white', 'black'):
    sys.stderr.write(usage)
    return
  background = sys.argv[1] + ' front.png'

  try:
    outdir = os.path.splitext(os.path.basename(sys.argv[2]))[0]
    outdir = os.path.splitext(outdir)[0]
    os.mkdir(outdir)
  except OSError: pass
  
  print
  with open(sys.argv[2]) as f:
    for card_num, line in enumerate(f):
      outfile = '%s%03d.png' % (sys.argv[1], card_num)
      outfile = os.path.join(outdir, outfile)
      text = line.strip()
      print('\rCreating %s...' % outfile)
      sys.stdout.flush()
      CardAgainstHumanity(text, sys.argv[1], background, outfile)
    print('\rCreated %d cards!%s' % (card_num+1, ' '*30))
      


  
if __name__ == '__main__':
  main()
