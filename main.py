################################################################################
# Chess Using Turtle Graphics.
################################################################################
class Chess:
    """Plays Chess Game. This initializes what needs to be done. However it is
    in the Input class that deals with driving the game.
    
    Attributes:
        board: Object of ChessBoard.
        pen: Pen to Turtle.
        piece: Object of ChessPiece.
        update: Update the screen after disabling tracer for faster draw.
        user_input: Object of Input.
        window: Turtle Screen used for Input class to hook the mouse.
        mouse_x: x of mouse. If None, then haven't done anything yet.
        mouse_y: y of mouse. If None, then haven't done anything yet.
    """
    SQUARE_SIZE = 40  # ULTIMATELY DECIDES ON SIZE OF EVERYTHING

    def __init__(self):
        import turtle
        self.pen = turtle.Turtle()
        self.window = turtle.Screen()
        self.board = ChessBoard(self.pen, Chess.SQUARE_SIZE)
        self.piece = ChessPiece(self.board)
        self.update = turtle.update
        self.user_input = Input(self.board, self.piece, self.window, 
                                self.update)
        turtle.tracer(0,0)
        self.pen.speed(0)
        self.pen.ht()
        self.pen.pensize(.5)

    def _select_piece(self, row, col):
        self.board.select_piece(row, col)
        self.update()
    
    def _move_piece(self, frow, fcol, trow, tcol):
        self.board.move_piece(frow, fcol, trow, tcol)
        self.update()
        
    def run(self):
        import time
        self.board.draw_board()
        self.piece.start_at_beginning()
        self.update()

        # Listen for mousse clicks.
        self.window.listen()


################################################################################
class ChessBoard:
    """Handles anything related to the chess board.
    
    Attributes:
        # Turtle Graphics Ability to Draw
        pen: Turtle pen.

        # Colors
        border_color: Oak Brown (128, 101, 23).
        select_color: Blue (0, 0, 255).
        not_select_color: Black (0, 0, 0)
        square_dark: Off Red (188, 23, 15).
        square_light: White (255, 255, 255).

        # Dimensions
        border_size: Size of the border.
        board_size: Size of the chess board (apart from border).
        board_top_y: Top y of chess board (apart from border).
        board_lft_x: Left x of chess board (apart from border).
        next_square: Amount for next square (horizontal or veritcal).
        square_side_size: Size of each individual side of a square on board.

        # Piece to Board DataStructure.
        squares: 2 dimensional list representing each square on board.
                       1st dimensional
                         0
                         1
                         2
                         3
                         4
                         5
                         6
                         7
                           0 1 2 3 4 5 6 7 2nd dimension
    """

    def __init__(self, pen, square_side_size):
        """Inits chess board attributes.
        
        Args:
            pen: Object of turtle pen.
            square_side_size: Integer representing side of square.
            squares: If pass, setup board with particular setup.
                           This could be used for testing or for practice.
            board_top_y: Chess Board top y coord.
            board_lft_x: Chess Board left x coord.
        """
        self.border_color = (128, 101, 23)
        self.square_dark = (188, 100, 75)
        self.square_light = (255, 255, 255)
        self.not_select_color = (0, 0, 0)
        self.select_color = (0, 0, 255)
        self.pen = pen
        self.next_square = square_side_size + 1
        self.board_side = square_side_size*8 + 7
        self.board_top_y = self.next_square*4
        self.board_lft_x = self.next_square*-4
        self.square_side_size = square_side_size
        self.border_size = square_side_size*1.2
        self.squares = [[None for col in range(8)] for row in range(8)]

    def _draw_square(self, left_x, top_y, side, color, fill):
        """Draws a square at a given row, col on board.
        
        Args:
            left_x: Left x of square.
            top_y: Top y of square.
            side: Square side.
            color: Color tuple (r,g,b).
            fill: True if fill.
        """
        self.pen.up()
        self.pen.color(color)
        self.pen.goto(left_x, top_y)
        self.pen.down()
        self.pen.fill(fill)
        for i in range(4):
            self.pen.forward(side)
            self.pen.right(90)
        self.pen.fill(False)

    def _goto_piece_xy(self, row, col, adjustment_x=0):
        """Goto x,y based upon row,col to display piece.
        
        Args:
            row: 1st dimension.
            col: 2nd dimension.
            adjustment_x: Fraction * square_side_size added to x.
        """
        self.pen.up()
        x = (self.board_lft_x + col*(self.next_square) + 
             self.square_side_size*.05) + adjustment_x*self.square_side_size
        y = (self.board_top_y - row*(self.next_square) -
             self.square_side_size*.8)
        self.pen.goto(x, y)

    def _put_chr_at(self, char, row, col, color, adjustment_x=0):
        """Put piece on chess board or notation on border.
        
        Args:
            char: Unicode of char.
            row: 1st dimension location.
            col: 2nd dimension location.
            adjustment_x: Fraction * square_side_size added to x. (text)
        """
        self._goto_piece_xy(row, col, adjustment_x)
        self.pen.color(color)
        self.pen.write(char, font=("Courier", round(self.square_side_size*.7),
                                   "normal"))
                                   
    def xy_to_rowcol(self, x, y):
        """Convert x,y to row,col on chess board.
        
        Args:
            x: x location.
            y: y location.
            
        Returns:
            List [row, col].
        """
        col = int((x - self.board_lft_x) / self.next_square)
        row = int((self.board_top_y - y) / self.next_square)
        return [row, col]

    def overwrite_board_square(self, row, col):
        """Overwrite board with new square.
        
        Args:
            row: Row of board, 0-7 from top to bottom.
            col: Col of board, 0-7 from left to right.
        """
        x = self.board_lft_x + col*self.next_square
        y = self.board_top_y - row*self.next_square
        color = self.square_light if (row+col)%2 == 0 else self.square_dark
        self._draw_square(x, y, self.square_side_size, color, True)
    
    def put_piece(self, piece, row, col):
        """Put piece on chess board.
        
        Args:
            piece: Unicode of chess piece.
            row: 1st dimension location.
            col: 2nd dimension location.
        """
        self.squares[row][col] = piece
        self._put_chr_at(piece, row, col, self.not_select_color, 0)

    def draw_board(self):
        """Draws border and board. No pieces are drawn."""
        # Clears screen of all turtle drawings
        self.pen.clear()

        # Draw border and fill everything.
        self._draw_square(self.board_lft_x - self.border_size,
                          self.board_top_y + self.border_size,
                          self.board_side + 2*self.border_size, 
                          self.border_color, True)

        # Draw white squares of board.
        self._draw_square(self.board_lft_x, self.board_top_y,
                          self.board_side, self.square_light, True)
                          
        # Draw dark squares of board.
        #   Automatically add a square side to x. 
        #   Subtract that square side when row is odd.
        for row in range(8):
            x = self.board_lft_x + self.next_square - row%2*self.next_square
            y = self.board_top_y - row*self.next_square
            for col in range(4):
                self._draw_square(x, y, self.square_side_size, self.square_dark,
                                  True)
                x += 2*self.next_square

        # Draw Notation 1-8 on border.
        for row in range(8):
            self._put_chr_at(chr(ord(str(8-row))), row, -1, (0,0,0), .2)
            
        # Draw Notation a-h on border.
        for col in range(8):
            self._put_chr_at(chr(ord('a')+col), 8, col, (0,0,0), .2)
            
        # Draw White Turn.
        self._put_chr_at("Turn: White", 9, 1, (0,0,0), .2)

    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move from row,col to row,col.
        
        If there is no piece at from location, do nothing.
        Does not validate moves.
        
        Args:
            from_row: from 1st dimension.
            from_col: from 2nd dimension.
            to_row: to 1st dimension.
            to_col: to 2nd dimension.
            
        Returns:
            False there was no piece at location.
        """
        # Get piece from-square
        piece = self.squares[from_row][from_col]
        
        # overwrite from-square and update board to relect nothing.
        self.squares[from_row][from_col] = None
        self.overwrite_board_square(from_row, from_col)

        # Overwrite to-square (including any pieces taken).
        self.overwrite_board_square(to_row, to_col)
        self.put_piece(piece, to_row, to_col)
        self.squares[to_row][to_col] =  piece
        
        return True

    def select_piece(self, row, col):
        """Select piece at row, col and highlight it to a different color.
        
        Args:
            row: Row 1-8 on board of piece.
            col: Col a-h on board of piece.
            
        Returns:
            A string representing the piece selected.
            None is returned if there is no piece at first selection or unselection.
        """
        piece = self.squares[row][col]
        if piece != None:
            self._put_chr_at(piece, row, col, self.select_color)
        return piece

    def unselect_piece(self, row, col):
        """Unselect piece that was previously selected.
        
        Args:
            row: Row wanting to unselect.
            col: Col wanting to unselect.
        """
        piece = self.squares[row][col]
        self.overwrite_board_square(row, col)
        self._put_chr_at(piece, row, col, self.not_select_color)


################################################################################
class ChessPiece:
    """Checks valid moves of pieces."""
    W_KING = u'♔'
    W_QUEEN = u'♕'
    W_ROOK = u'♖'
    W_BISHOP = u'♗'
    W_KNIGHT = u'♘'
    W_PAWN = u'♙'
    B_KING = u'♚'
    B_QUEEN = u'♛'
    B_ROOK = u'♜'
    B_BISHOP = u'♝'
    B_KNIGHT = u'♞'
    B_PAWN = u'♟'
    
    def __init__(self, chess_board):
        """Inits attributes.
        
        Args:
            chess_board: Object of ChessBoard.
        """
        self.board = chess_board

    def start_at_beginning(self):
        """Draw pieces at the beginning of game."""
        b_pieces = [ChessPiece.B_ROOK, 
                    ChessPiece.B_KNIGHT,
                    ChessPiece.B_BISHOP,
                    ChessPiece.B_QUEEN,
                    ChessPiece.B_KING,
                    ChessPiece.B_BISHOP,
                    ChessPiece.B_KNIGHT,
                    ChessPiece.B_ROOK]
        w_pieces = [ChessPiece.W_ROOK, 
                    ChessPiece.W_KNIGHT,
                    ChessPiece.W_BISHOP,
                    ChessPiece.W_QUEEN,
                    ChessPiece.W_KING,
                    ChessPiece.W_BISHOP,
                    ChessPiece.W_KNIGHT,
                    ChessPiece.W_ROOK]

        for i in range(8):
            self.board.put_piece(b_pieces[i], 0, i)
            self.board.put_piece(ChessPiece.B_PAWN, 1, i)
            self.board.put_piece(w_pieces[i], 7, i)
            self.board.put_piece(ChessPiece.W_PAWN, 6, i)

    def piece_color(self, piece):
        """Tells the color of the piece.
        
        Args:
            piece: The unicode of the piece.
            
        Returns:
            "white" is returned for white and "black" for black pieces.
            None is returned for blank piece.
        """
        if piece == None:
            return None
        if ord(ChessPiece.W_KING) <= ord(piece) <= ord(ChessPiece.W_PAWN):
            return "white"
        return "black"
        
    def _is_taking_own_piece(self, from_row, from_col, to_row, to_col):
        """Trying to take own piece?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if trying to take own piece.
        """
        # Get piece being moved
        piece = self.board.squares[from_row][from_col]
        piece_color = self.piece_color(piece)
        
        # is piece trying to take it's own piece?
        to_piece = self.board.squares[to_row][to_col]
        if to_piece != None:
            if self.piece_color(to_piece) == piece_color:
                return True
        return False

    def _any_piece_in_way(self, from_row, from_col, dr, dc, dm):
        """Is any pieces are in the way for bishop or rook like moves?
        
        NOTE: If only moving one, than assume piece is not same piece
        so assume can move there.
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            dr: amount to change row
            dc: amount to change col
            dm: amount to move

        Return:
            True if valid move.
        """
        for i in range(1, dm):
            if self.board.squares[from_row+i*dr][from_col+i*dc] != None:
                return False
        return True
        
    def _is_rook_move_valid(self, from_row, from_col, to_row, to_col):
        """Is move valid for a rook?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if valid move.
        """
        # if not on same column or row
        if ((from_row != to_row and from_col != to_col) or 
            (from_row == to_row and from_col == to_col)):
            return False
        
        # check if any pieces are in the way of destination
        if from_row != to_row:
            dc = 0
            dr = 1 if to_row - from_row > 0 else -1
        if from_col != to_col:
            dr = 0
            dc = 1 if to_col - from_col > 0 else -1
        dm = abs(to_row - from_row)
        return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

    def _is_knight_move_valid(self, from_row, from_col, to_row, to_col):
        """Is move valid for a knight?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if valid move.
        """
        # check for valid move
        if ((abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2) or
            (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1)):
            return True
        return False
        
    def _is_bishop_move_valid(self, from_row, from_col, to_row, to_col):
        """Is move valid for a bishop?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if valid move.
        """
        # if not on same colored diagonal exit.
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        
        # check if any pieces are in the way of destination
        dr = 1 if to_row - from_row > 0 else -1
        dc = 1 if to_col - from_col > 0 else -1
        dm = abs(to_row - from_row)
        return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

    def _is_queen_move_valid(self, from_row, from_col, to_row, to_col):
        """Is move valid for a queen?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if valid move.
        """
        # if not on same colored diagonal
        if abs(from_row - to_row) != abs(from_col - to_col):
            # if on same row? (like rook)
            if from_row != to_row:
                dc = 0
                dr = 1 if to_row - from_row > 0 else -1
            # elif on same col?
            elif from_col != to_col:
                dr = 0
                dc = 1 if to_col - from_col > 0 else -1
            else:
                # if not on same col or row
                return False
        else:
            # on same colored diagonal (moves like bishop)
            dr = 1 if to_row - from_row > 0 else -1
            dc = 1 if to_col - from_col > 0 else -1

        # check if any pieces are in the way of destination
        dm = abs(to_row - from_row)
        return self._any_piece_in_way(from_row, from_col, dr, dc, dm)
    
    def _is_king_move_valid(self, from_row, from_col, to_row, to_col):
        """Is move valid for a king?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if valid move.
        """
        if abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1:
            return True
        return False
        
    def _is_pawn_move_valid(self, from_row, from_col, to_row, to_col):
        """Is move valid for a pawn?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.

        Return:
            True if valid move.
        """
        # Setup variables used
        piece = self.board.squares[from_row][from_col]
        to_piece = self.board.squares[to_row][to_col]
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        dc = 0
        
        # Set flag for first move of pawn
        first_move = True if from_row == 6 or from_row == 1 else False

        # If direction is not correct for white, exit
        if to_row - from_row > 0:
            dr = 1
            if self.piece_color(piece) == "white":
                return False
            
        # If direction is not correct for black, exit
        if to_row - from_row < 0:
            dr = -1
            if self.piece_color(piece) == "black":
                return False
        
        # If moving straight
        if from_col == to_col:
            # if not legal straight move, exit
            if not (row_diff == 1 or (first_move and row_diff == 2)):
                return False
            
            # make sure to move has no pieces on straight path
            dm = row_diff + 1
            return self._any_piece_in_way(from_row, from_col, dr, dc, dm)

            # otherwise legal move
            # return True
            
        # else move must be taking piece move
        # if legal taking piece move and (opponent-already check for own piece) piece at to-square
        if col_diff == 1 and row_diff == 1 and to_piece != None:
            return True
            
        return False

    def is_move_valid(self, from_row, from_col, to_row, to_col):
        """Is the piece attempting to move from - to valid?
        
        Args:
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.
            
        Return:
            True if valid move.
        """
        # check is taking own piece?
        if self._is_taking_own_piece(from_row, from_col, to_row, to_col):
            return False

        piece = self.board.squares[from_row][from_col]
        if piece == ChessPiece.W_ROOK or piece == ChessPiece.B_ROOK:
            return self._is_rook_move_valid(from_row, from_col, 
                                              to_row, to_col)
        if piece == ChessPiece.W_KNIGHT or piece == ChessPiece.B_KNIGHT:
            return self._is_knight_move_valid(from_row, from_col,
                                              to_row, to_col)
        if piece == ChessPiece.W_BISHOP or piece == ChessPiece.B_BISHOP:
            return self._is_bishop_move_valid(from_row, from_col, 
                                              to_row, to_col)
        if piece == ChessPiece.W_QUEEN or piece == ChessPiece.B_QUEEN:
            return self._is_queen_move_valid(from_row, from_col, 
                                             to_row, to_col)
        if piece == ChessPiece.W_KING or piece == ChessPiece.B_KING:
            return self._is_king_move_valid(from_row, from_col, 
                                            to_row, to_col)
        if piece == ChessPiece.W_PAWN or piece == ChessPiece.B_PAWN:
            return self._is_pawn_move_valid(from_row, from_col, 
                                            to_row, to_col)
                                            
    def is_check_or_mate(self, color_move):
        print("is_check_or_mate()")
        """Is check of mate?
        
        Args:
            possible_squares: possible board squares[row][col]
            color_move: color being moved.
            from_row: row of source square.
            from_col: col of source square.
            to_row: row of destination square.
            to_col: col of destination square.
            
        Return:
            0 - not check or mate
            1 - check
            2 - check mate
        """
        # Get all pieces of color_move and get opposing king
        pieces = [] # a tuple (row,col) of where piece is located
        krow = None # row of opposing king
        kcol = None # col of opposing king
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col]
                if self.piece_color(piece) == color_move:
                   pieces.append((row,col))
                elif piece == ChessPiece.W_KING or piece == ChessPiece.B_KING:
                    krow = row
                    kcol = col

        # Check if place in Check
        num_piece_check = 0
        return_result = 0
        
        for piece_rowcol in pieces:
            frow, fcol = piece_rowcol
            if self.is_move_valid(frow, fcol, krow, kcol):
                num_piece_check += 1
            if num_piece_check == 2:
                break
        if num_piece_check > 0:
            return_result += 1
        return return_result


################################################################################
class Input:
    """Get input from user for move.
    
    Attributes:
        board: refers to ChessBoard object.
        pieces: refers to ChessPieces object.
        update: Update draw. Needed because tracer(0,0) is used.
        is_piece_selected: true if piece was selected.
        selected_row: row of selected piece.
        selected_col: col of selected piece.
        turn_color: color of player taking current turn.
        check_color: color of player in check.
    """
    def __init__(self, chess_board, pieces, window, update):
        """Inits and setup keyboard input handlers.
        
        Args:
            chess_board: Object of ChessBoard
            pieces: Object of CheckPiece
            window: Turtle screen.
            update: Refers to update().
        """
        self.board = chess_board
        self.pieces = pieces
        self.update = update
        self.is_piece_selected = False
        self.selected_row = -1
        self.selected_col = -1
        self.turn_color = "white"
        self.check_color = None
        
        window.onclick(self.onclick)
    
    def onclick(self, x, y):
        # Check to see if within board for x. Do nothing if not.
        board_x = x - self.board.board_lft_x
        if (board_x < 0 or
            board_x >= 8*self.board.next_square):
            return
        
        # Checks to see if within board for y. Do nothing if not.
        board_y = self.board.board_top_y - y
        if (board_y < 0 or
            board_y >= 8*self.board.next_square):
            return
    
        # Get the row, col from x, y.
        row, col = self.board.xy_to_rowcol(x, y)

        # if first time selecting piece
        if self.is_piece_selected == False:
            selected_piece = self.board.select_piece(row, col)
            # if selected piece is not a piece then exit
            if selected_piece == None:
                return
            
            # if piece is not correct turn color then exit
            piece_color = self.pieces.piece_color(selected_piece)
            if self.turn_color is not piece_color:
                self.board.unselect_piece(row, col)
                return
            
            # update selected piece
            print("update selected piece") # debug
            self.update() # update selected color in self.board.select_piece(row,col)
            self.is_piece_selected = True
            self.selected_row = row
            self.selected_col = col
            return

        # (then must have piece already selected)
        # if new row,col is the same as selected one, then unselect
        if row == self.selected_row and col == self.selected_col:
            self.board.unselect_piece(row, col)
            self.update()
            self.is_piece_selected = False
            self.selected_row = -1
            self.selected_col = -1
            return
        
        # (must have piece already selected and new location)
        # check if valid move
        if self.pieces.is_move_valid(self.selected_row, 
                                     self.selected_col, row, col) == False:
            return
        
        # if in check, check if move would get out of check
        pass
        
        # save original board just in case can't move there
        #  (because copy can't be imported in this version of python)
        org_selected_row = self.selected_row
        org_selected_col = self.selected_col
        org_selected_piece = self.board.squares[self.selected_row][self.selected_col]
        org_row = row
        org_col = col
        org_to_piece = self.board.squares[row][col]
    
        # move piece
        self.board.move_piece(self.selected_row, self.selected_col, row, col)
        print self.board.squares
        self.update()
        self.is_piece_selected = False
        self.selected_row = -1
        self.selected_col = -1

        # if in check, check if move would get out of check
        '''
        result = self.pieces.is_check_or_mate("black" if self.turn_color == "white" else "white")
        '''
        # if move would result in check or mate
        '''
        result = self.pieces.is_check_or_mate(self.turn_color,
                                              self.selected_row, self.selected_col,
                                              row, col)
        # if not check
        if result == 0:
            self.check_color = None
            
        # if check
        if result == 1:
            self.check_color = "black" if self.turn_color == "white" else "white"
            
        # if checkmate
        if result == 2:
            # end game
            pass
        '''

        # switch player        
        self.turn_color = "black" if self.turn_color == "white" else "white"
        
        # display turn before next selected piece begins
        if self.turn_color == "white":
            self.board._put_chr_at("Turn: Black", 9, 1, (255,255,255), .2)
            self.board._put_chr_at("Turn: White", 9, 1, (0,0,0), .2)
        else:
            self.board._put_chr_at("Turn: White", 9, 1, (255,255,255), .2)
            self.board._put_chr_at("Turn: Black", 9, 1, (0,0,0), .2)
            
        # if turn to move is in check
        if self.turn_color == self.check_color:
            self.board._put_chr_at("Check", 10, 3, (0,0,0), .2)
        else:
            self.board._put_chr_at("Check", 10, 3, (255,255,255), .2)
            
        self.update()

################################################################################
# Run the Game.
#print "\x1b[30m \x1b[0m"
chess = Chess()
chess.run()

