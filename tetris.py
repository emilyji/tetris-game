from graphics import *
import random

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 1

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def check_if_can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
        '''
        if board.check_if_can_move(self.x+dx, self.y+dy):
            return True
        else:
            return False

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape(object):
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape  (i.e. 1 for clockwise, -1 for counterclockwise)
                    shift_rotation_dir - type: bool - whether or not the shape shifts rotation direction
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        # A boolean to indicate if a shape shifts rotation direction or not
        self.shift_rotation_dir = False

        for pos in coords:
            self.blocks.append(Block(pos, color))

    def draw_shape(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)
             

    def get_blocks(self):
        '''returns the list of blocks
        '''
        
        return self.blocks
    
    def check_if_can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if all of them can, and False otherwise
        '''
        for block in self.blocks:
            if block.check_if_can_move(board, dx, dy) == False:
                return False
        return True
        
    
    def check_can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated, return True
            if it can, False otherwise
        '''
        
        d = self.rotation_dir
        center = self.center_block 
        for block in self.blocks:
            x= center.x - d*center.y + d*block.y
            y= center.y + d*center.x - d*block.x
            dx = x-block.x
            dy = y-block.y
            if block.check_if_can_move(board, dx, dy) == False:
                return False
        
        return True

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape in the direction
            specified by the value returned by
            rotation_dir
        '''
        if self.check_can_rotate(board) == True:
            
            d = self.rotation_dir
            center = self.center_block
            for block in self.get_blocks():
                x= center.x - d*center.y + d*block.y
                y= center.y + d*center.x - d*block.x
                dx = x-block.x
                dy = y-block.y
                block.move(dx, dy)
                    
        if self.shift_rotation_dir:
            self.rotation_dir = self.rotation_dir*-1

############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 2, center.y)]
        Shape.__init__(self, coords, 'misty rose')
        self.center_block = self.blocks[1]
        self.rotation_dir = -1
        self.shift_rotation_dir = True
    
class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'lavender')
        self.center_block = self.blocks[1]

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'papaya whip')
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'thistle')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        return

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'RosyBrown1')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True

class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'peach puff')
        self.center_block = self.blocks[1]

class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'lemon chiffon')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True


############################################################
# BOARD CLASS
############################################################

class Board(object):
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('white')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}
     
    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
            Hint: you want to use an existing method of the shape
            to check if the shape can be drawn at its current location
        '''
        if shape.check_if_can_move(self, 0,0) == True:
            shape.draw_shape(self.canvas)
            return True
        else:
            return False
       
    def check_if_can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            checks if it is ok to move to square x,y
            you need to check:
            1. if the position is outside of the board boundaries
            2. if there is already a block at that postion
            returns True if it is ok, otherwise returns False

        '''

        if 0<= x < 10 and 0 <= y < 20 and (x,y) not in self.grid:
            return True
        else:
            return False
        
    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
        '''
        
        blocks = shape.get_blocks()
        for block in blocks:
            self.grid[(block.x, block.y)] = block

    def delete_row(self, y):
        ''' Parameters: y - type:int

            delete all the blocks in row y from the grid
            and erase them from the canvas
        '''
        for x in range(self.width):
           if (x,y) in self.grid.keys():
               block = self.grid[x,y]
               block.undraw()
               del self.grid[x,y]
               
               
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            check if all the squares in row y are occupied.
            return True if they are, False otherwise
        '''

        for x in range(self.width):
            if (x,y) not in self.grid.keys():
                return False
        return True

           
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            move all the blocks in each row starting at y_start and up
            down 1 square
            Note: make sure you update the grid as well.
        '''
        for y in range(y_start, 0, -1):
            for x in range(self.width):
                if (x,y) in self.grid:
                    block = self.grid[x,y]
                    block.move(0, 1)
                    del self.grid[x,y]
                    self.grid[block.x, block.y] = block 
                                  
    
    def remove_complete_rows(self):
        ''' removes all the complete rows
            and moves all rows above them down
        '''
        for y in range(self.height + 1):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.move_down_rows(y)

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        gameoverbox = Rectangle(Point(45,225), Point(255, 325))
        gameoverbox.setFill('pale violet red')
        gameoverbox.draw(self.canvas)
        game_over_msg = Text(Point(150, 275), "GAME OVER")
        game_over_msg.setStyle('italic')
        game_over_msg.setFace('times roman')
        game_over_msg.setTextColor('white')
        game_over_msg.draw(self.canvas)      


############################################################
# WTP TETRIS CLASS
############################################################

class WTPTetris(object):
    ''' WTPTetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()
        self.board.draw_shape(self.current_shape)

        # 1. draw the current_shape on the board (take a look at the
        # methods available in the Board class)
        # 2. animate the shape
        
        self.animate_shape()
        
        
       
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay instance variable (attribute)
        '''
        
        self.do_move("Down")
        win.after(self.delay, self.animate_shape)
            

    def create_new_shape(self):
        ''' Return value: type: Shape
            
            create a random new shape that is centered
            at the top center of the board
            return the shape
        '''
        
        shape = random.choice(self.SHAPES)
        done_shape = shape(Point(self.BOARD_WIDTH/2, 0))
        return done_shape
        
        

    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False
        '''
        dx, dy = self.DIRECTION[direction]
        if self.current_shape.check_if_can_move(self.board, dx,dy):
            self.current_shape.move(dx,dy)
            return True
        if direction == 'Down':
            self.board.add_shape(self.current_shape)
            self.board.remove_complete_rows()
            self.current_shape = self.create_new_shape()
            self.board.draw_shape(self.current_shape)
            if not self.current_shape.check_if_can_move(self.board, 0,0):
                self.board.game_over()
        else:
            return False
            
            
                   

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        if self.current_shape.check_can_rotate(self.board)== True:
            self.current_shape.rotate(self.board)
        else:
            return False
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currently just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.
        '''
        
        
        key = event.keysym
        print key

            
        
        if key in self.DIRECTION:
            self.do_move(key)
        elif key == 'space':
            while self.do_move('Down'):
                pass
        elif key == 'Up':
            self.do_rotate()
        
            
       
################################################################
# Start the game
################################################################

win = Window("WTP Tetris")
game = WTPTetris(win)
win.mainloop()
