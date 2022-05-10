import pygame

import time

import sys

board = [['  ' for i in range(10)] for i in range(10)]


## Creates a chess piece class that shows what team a piece is on, what type of piece it is and whether or not it can be killed by another selected piece.

class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image


## Creates instances of amazonian pieces
## The first parameter defines what team its on and the second, what type of piece it is

bq = Piece('b', 'q', 'b_queen.png')
wq = Piece('w', 'q', 'w_queen.png')
arrow = Piece('X', 'x', 'X.png')

# the origin is in top left, first index is column, second index is line
starting_order = {(0, 0): None, (1, 0): None,
                  (2, 0): None, (3, 0): pygame.image.load(bq.image),
                  (4, 0): None, (5, 0): None,
                  (6, 0): pygame.image.load(bq.image), (7, 0): None,
                  (8, 0): None, (9, 0): None,

                  (0, 1): None, (1, 1): None,
                  (2, 1): None, (3, 1): None,
                  (4, 1): None, (5, 1): None,
                  (6, 1): None, (7, 1): None,
                  (8, 1): None, (9, 1): None,

                  (0, 2): None, (1, 2): None,
                  (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None,
                  (6, 2): None, (7, 2): None,
                  (8, 2): None, (9, 2): None,

                  (0, 3): pygame.image.load(bq.image), (1, 3): None,
                  (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None,
                  (6, 3): None, (7, 3): None,
                  (8, 3): None, (9, 3): pygame.image.load(bq.image),

                  (0, 4): None, (1, 4): None,
                  (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None,
                  (6, 4): None, (7, 4): None,
                  (8, 4): None, (9, 4): None,

                  (0, 5): None, (1, 5): None,
                  (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None,
                  (6, 5): None, (7, 5): None,
                  (8, 5): None, (9, 5): None,

                  (0, 6): pygame.image.load(wq.image), (1, 6): None,
                  (2, 6): None, (3, 6): None,
                  (4, 6): None, (5, 6): None,
                  (6, 6): None, (7, 6): None,
                  (8, 6): None, (9, 6): pygame.image.load(wq.image),

                  (0, 7): None, (1, 7): None,
                  (2, 7): None, (3, 7): None,
                  (4, 7): None, (5, 7): None,
                  (6, 7): None, (7, 7): None,
                  (8, 7): None, (9, 7): None,

                  (0, 8): None, (1, 8): None,
                  (2, 8): None, (3, 8): None,
                  (4, 8): None, (5, 8): None,
                  (6, 8): None, (7, 8): None,
                  (8, 8): None, (9, 8): None,

                  (0, 9): None, (1, 9): None,
                  (2, 9): None, (3, 9): pygame.image.load(wq.image),
                  (4, 9): None, (5, 9): None,
                  (6, 9): pygame.image.load(wq.image), (7, 9): None,
                  (8, 9): None, (9, 9): None,

                  }


def create_board(board):
    # here the first index is line, second is column, origin top-left
    # team, type, image, killable=False
    board[0][3] = Piece('b', 'q', 'b_queen.png')
    board[0][6] = Piece('b', 'q', 'b_queen.png')
    board[3][0] = Piece('b', 'q', 'b_queen.png')
    board[3][9] = Piece('b', 'q', 'b_queen.png')

    board[6][0] = Piece('w', 'q', 'w_queen.png')
    board[6][9] = Piece('w', 'q', 'w_queen.png')
    board[9][3] = Piece('w', 'q', 'w_queen.png')
    board[9][6] = Piece('w', 'q', 'w_queen.png')

    return board


## returns the input if the input is within the boundaries of the board
def on_board(position):
    if -1 < position[0] < 10 and -1 < position[1] < 10:
        return True


## returns a string that places the rows and columns of the board in a readable manner
def convert_to_readable(board):
    output = ''

    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output


## resets "x's" and killable pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = '  '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
    return convert_to_readable(board)


## Takes in board as argument then returns 2d array containing positions of valid moves
def highlight(board):
    highlighted = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'x ':
                highlighted.append((i, j))
            else:
                pass
    return highlighted


def check_team(moves, index, first_move=False):
    if first_move:
        return True
    row, col = index
    if moves % 2 == 0:
        if board[row][col].team == 'w':
            return True
    elif board[row][col].team == 'b':
        return True
    else:
        return False


## This takes in a piece object and its index then runs then checks where that piece can move using separately defined functions for each type of piece.
def select_moves_2(piece, index, moves):
    if check_team(moves, index):

        if piece.type == 'q':
            return highlight(queen_moves(index))


## This creates 4 lists for up, down, left and right and checks all those spaces for pieces of the opposite team. The list comprehension is pretty long so if you don't get it just msg me.
def rook_moves(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 10 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 10 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    break
    return board


## Same as the rook but this time it creates 4 lists for the diagonal directions and so the list comprehension is a little bit trickier.
def bishop_moves(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 10)],
                 [[index[0] + i, index[1] - i] for i in range(1, 10)],
                 [[index[0] - i, index[1] + i] for i in range(1, 10)],
                 [[index[0] - i, index[1] - i] for i in range(1, 10)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    break
    return board


## applies the rook moves to the board then the bishop moves because a queen is basically a rook and bishop in the same position.
def queen_moves(index):
    board = rook_moves(index)
    board = bishop_moves(index)
    return board


## Checks a 5x5 grid around the piece and uses pythagoras to see if if a move is valid. Valid moves will be a distance of sqrt(5) from centre
def knight_moves(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    return board


WIDTH = 700

WIN = pygame.display.set_mode((WIDTH, WIDTH))

""" This is creating the window that we are playing on, it takes a tuple argument which is the dimensions of the window so in this case 800 x 800px
"""

pygame.display.set_caption("Amazon")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 10, WIDTH / 10))

    def setup(self, WIN):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] is None:
                pass
            else:
                WIN.blit(starting_order[(self.row, self.col)], (self.x, self.y))

        """
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the chess pieces instead
        """


def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i + j) % 2 == 1:
                grid[i][j].colour = GREY
    return grid


"""
This is creating the nodes thats are on the board(so the chess tiles)
I've put them into a 2d array which is identical to the dimesions of the chessboard
"""


def draw_grid(win, rows, width):
    gap = width // 10
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

    """
    The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
    from each other and that is what this function does"""


def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def Find_Node(pos, WIDTH):
    interval = WIDTH / 10
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE
        """
        Displays all the potential moves
        """


def Do_Move(OriginalPos, FinalPosition, WIN):
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None


def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i + j) % 2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid


"""this takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the node it is moving to
you can get those co-ordinates using my old function for swap"""


def main(WIN, WIDTH):
    create_board(board)
    moves = 1
    selected = False
    moved = False
    piece_to_move = []
    grid = make_grid(10, WIDTH)
    while True:
        pygame.time.delay(50)  ##stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """This quits the program if the player closes the window"""

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                if not selected:
                    try:
                        possible = select_moves_2((board[x][y]), (x, y), moves)
                        print(possible)
                        for positions in possible:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x, y
                        print(piece_to_move)
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')
                    # print(piece_to_move)

                else:

                    if board[x][y] == 'x ':
                        if not moved:
                            row, col = piece_to_move
                            print("Row={}, col={}".format(row, col))
                            print("x={}. y={}".format(x, y))
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_highlight(grid)

                            Do_Move((col, row), (y, x), WIN)
                            # now highlight the new position
                            possible = select_moves_2((board[x][y]), (x, y), moves)
                            for positions in possible:
                                row, col = positions
                                grid[row][col].colour = BLUE
                            # piece_to_move = x, y

                            moved = True
                        else:
                            piece_to_move = x, y
                            row, col = piece_to_move
                            board[row][col] = Piece('X', 'x', 'X.png')
                            starting_order[(col, row)] = pygame.image.load(arrow.image)
                            print("Punem X")
                            deselect()
                            remove_highlight(grid)
                            moves += 1
                            selected = False
                            moved = False
                            #print(convert_to_readable(board))
                    else:
                        deselect()
                        remove_highlight(grid)
                        selected = False
                        moved = False
                        print("Invalid move")
                        selected = False

            update_display(WIN, grid, 10, WIDTH)


if __name__ == "__main__":
    main(WIN, WIDTH)
