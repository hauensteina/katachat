
EMPTY = '.'
WHITE = 'O'
BLACK = 'X'
COORDS = 'ABCDEFGHIJKLMNOPQRST'

class GoBoard:
    """
    A Go board implementation without Ko rule, Coordinates start at 0.
    """
    def __init__(self, size=9):
        self.size = size
        self.board = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.moves = []

    def is_valid_move(self, x, y, color):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if self.board[y][x] != EMPTY:
            return False
        return True

    def place_stone(self, x, y, color):
        if self.is_valid_move(x, y, color):
            self.board[y][x] = color
            self.remove_captured_stones(self.board, x, y)
            self.moves.append( ['b' if color == BLACK else 'w', f'{chr(x+65)}{y+1}'] )

    def play_move(self, move, color):
        """ 
            Play a move in the format 'A1' or 'B2'
            Color is in ('O','X') 
         """
        x = ord(move[0].lower()) - ord('a')
        y = int(move[1:]) - 1
        self.place_stone(x, y, color)

    def get_string(self, x, y):
        """ Get all coordinates in the string containing the stone at (x, y) """
        if not (0 <= x < self.size and 0 <= y < self.size): return set()
        color = self.board[y][x]
        if color == EMPTY: return set()
        sstring = set()
        candidates = set()
        candidates.add((x, y))
        while candidates:
            cx, cy = candidates.pop()
            sstring.add((cx, cy))
            neighbors = ( (cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1) )
            for nx, ny in neighbors:
                if not (0 <= nx < self.size and 0 <= ny < self.size): continue
                if (nx, ny) not in sstring and self.board[ny][nx] == color:
                    candidates.add((nx, ny))
        return sstring  
    
    def remove_captured_stones(self, board, x, y):
        """" Remove any stones captured by the stone placed at (x, y) """
        if not (0 <= x < self.size and 0 <= y < self.size): return
        color = board[y][x] 
        if color == EMPTY: return 
        other_color = BLACK if color == WHITE else WHITE
        neighbors = ( (x-1, y), (x+1, y), (x, y-1), (x, y+1) )
        for nx, ny in neighbors:
            if not (0 <= nx < self.size and 0 <= ny < self.size): continue
            if not self.board[ny][nx] == other_color: continue
            sstring = self.get_string(nx, ny)
            if self.is_captured(sstring):
                self.remove_string(sstring)

    def is_captured(self, sstring):
        """ Return True if no stone in the string has a liberty """
        for x, y in sstring:
            neighbors = ( (x-1, y), (x+1, y), (x, y-1), (x, y+1) )
            for nx, ny in neighbors:
                if not (0 <= nx < self.size and 0 <= ny < self.size): continue
                if self.board[ny][nx] == EMPTY: return False
        return True
    
    def remove_string(self, sstring):
        for x, y in sstring:
            self.board[y][x] = EMPTY

    def __str__(self):
        res = '\n  ' + ' '.join([ f'{COORDS[x]}' for x in range(self.size) ]) + '\n'
        for row in  range(self.size):
            res += f'{self.size-row} ' + ' '.join(self.board[self.size - row - 1]) + '\n'
        res += '\n\n'
        return res

def main():
    board = GoBoard()
    board.place_stone(3, 3, BLACK) 
    board.place_stone(4, 3, WHITE)
    board.place_stone(3, 4, WHITE)
    board.place_stone(2, 3, WHITE)
    board.place_stone(3, 2, WHITE)

    print(board)  

    board = GoBoard()
    board.place_stone(3, 3, BLACK) 
    board.place_stone(3, 4, BLACK)

    board.place_stone(3, 2, WHITE)
    board.place_stone(3, 5, WHITE)
    board.place_stone(2, 3, WHITE)
    board.place_stone(2, 4, WHITE)
    board.place_stone(4, 3, WHITE)
    board.place_stone(4, 4, WHITE)

    print(board)  


if __name__ == "__main__":
    main()
