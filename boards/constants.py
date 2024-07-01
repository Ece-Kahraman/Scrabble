import numpy


BOARD_SCORES = numpy.empty((15, 15), dtype='U3')
BOARD_SCORES[0][0] = BOARD_SCORES[0][7] = BOARD_SCORES[0][14] = '3W'
BOARD_SCORES[7][0] = BOARD_SCORES[7][14] = '3W'
BOARD_SCORES[14][0] = BOARD_SCORES[14][7] = BOARD_SCORES[14][14] = '3W'
BOARD_SCORES[1][1] = BOARD_SCORES[2][2] = BOARD_SCORES[3][3] = BOARD_SCORES[4][4] = '2W'
BOARD_SCORES[1][13] = BOARD_SCORES[2][12] = BOARD_SCORES[3][11] = BOARD_SCORES[4][10] = '2W'
BOARD_SCORES[13][1] = BOARD_SCORES[12][2] = BOARD_SCORES[11][3] = BOARD_SCORES[10][4] = '2W'
BOARD_SCORES[10][10] = BOARD_SCORES[11][11] = BOARD_SCORES[12][12] = BOARD_SCORES[13][13] = '2W'
BOARD_SCORES[7][7] = '2W'
BOARD_SCORES[1][5] = BOARD_SCORES[1][9] = '3L'
BOARD_SCORES[5][1] = BOARD_SCORES[5][5] = BOARD_SCORES[5][9] = BOARD_SCORES[5][13] = '3L'
BOARD_SCORES[9][1] = BOARD_SCORES[9][5] = BOARD_SCORES[9][9] = BOARD_SCORES[9][13] = '3L'
BOARD_SCORES[13][5] = BOARD_SCORES[13][9] = '3L'
BOARD_SCORES[0][3] = BOARD_SCORES[0][11] = BOARD_SCORES[2][6] = BOARD_SCORES[2][8] = BOARD_SCORES[3][7] = '2L'
BOARD_SCORES[3][0] = BOARD_SCORES[11][0] = BOARD_SCORES[6][2] = BOARD_SCORES[8][2] = BOARD_SCORES[7][3] = '2L'
BOARD_SCORES[14][3] = BOARD_SCORES[14][11] = BOARD_SCORES[12][6] = BOARD_SCORES[12][8] = BOARD_SCORES[11][7] = '2L'
BOARD_SCORES[3][14] = BOARD_SCORES[11][14] = BOARD_SCORES[6][12] = BOARD_SCORES[8][12] = BOARD_SCORES[7][11] = '2L'
BOARD_SCORES[6][6] = BOARD_SCORES[6][8] = BOARD_SCORES[8][6] = BOARD_SCORES[8][8] = '2L'

DICTIONARY = set()
with open('C:/Users/kahra/Documents/dictionary.txt', 'r') as f:
    for line in f:
        DICTIONARY.add(line[:-2])

BAG = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
       'B', 'B',
       'C', 'C',
       'D', 'D', 'D', 'D',
       'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
       'F', 'F',
       'G', 'G', 'G',
       'H', 'H',
       'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
       'J',
       'K',
       'L', 'L', 'L', 'L',
       'M', 'M',
       'N', 'N', 'N', 'N', 'N', 'N',
       'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
       'P', 'P',
       'Q',
       'R', 'R', 'R', 'R', 'R', 'R',
       'S', 'S', 'S', 'S',
       'T', 'T', 'T', 'T', 'T', 'T',
       'U', 'U', 'U', 'U',
       'V', 'V',
       'W', 'W',
       'X',
       'Y', 'Y',
       'Z']

