EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

### add code here ###
class Tile():
    """
    A tile represents an available space in the game board.

    """
    def __init__(self, name, selectable=True):
        """
        Construct a tile object given their name and selectable tile.

        Parameters:
            name(str): The name of the tile.
            selectable(bool): The tile can be unlocked/selectable (available to have pipes placed on them)
                              or locked/unselectable (cannot have pipes placed on them).

        """
        self._name=name
        self._selectable=selectable
        
    def get_name(self):
        """
        (str) Return the name of the tile.
        
        """
        return self._name
    
    def get_id(self):
        
        """
        (str) Return the id of the tile class.
        
        """
        return EMPTY_TILE
    
    def set_select(self, select: bool):
        """
        (bool) Sets the status of the select switch to True or False.
        
        """
        self._selectable=select

    def can_select(self):
        """
        (bool) Returns True if the tile is selectable,
               or False if the tile is not selectable.
        
        """
        return self._selectable

    def __str__(self):
        """
        (str) Returns the string representation of the Tile.
        
        """
        return f"Tile('{self._name}', {self._selectable})"

    def __repr__(self):
        """
        (str) Returns the string representation of the Tile.
        
        """
        return f"Tile('{self._name}', {self._selectable})"

class Pipe(Tile):
    """
    A pipe represents a pipe in the game

    """
    def __init__(self,name, orientation=0, selectable=True):
        """
        Construct a pipe object given their name, orientation and selectable tile.

        Parameters:
            name(str): The name of the pipe.
            orientation(int): The orientation of pipe.
            selectable(bool): The tile can be unlocked/selectable (available to have pipes placed on them)
                              or locked/unselectable (cannot have pipes placed on them).


        """
        super().__init__(name,selectable=True)
        self._orientation=orientation

    def get_id(self):
        
        """
        (str) Return the id of the pipe class.
        
        """
        return 'pipe'

    def get_orientation(self):
        """
        (int) Returns the orientation of the pipe
              (orientation must be in the range [0, 3]).
        
        """
        return self._orientation

    def rotate(self, direction: int):
        """
        Rotates the pipe one turn.
        
        """
        if direction%4!=0:
            self._orientation=(self._orientation+direction%4)%4
        else:
            self._orientation
        

    def get_connected(self, side: str):
        """
        list<str> Returns a list of all sides that are connected to
                   the given side.

        """
        
        if self._name=='straight':
            straight1={'N':['S'],'S':['N']}
            straight2={'E':['W'],'W':['E']}

            if self._orientation==0 or self._orientation==2 :
                return straight1.get(side,[])
            else:
                return straight2.get(side,[])
            

        elif self._name=='cross':
            cross={'N':['S','E','W'],'S':['N','E','W'],'E':['N','S','W'],'W':['N','E','S']}

            if self._orientation==0 or self._orientation==1 or self._orientation==2 or self._orientation==3:
                return cross.get(side,[])
          
        elif self._name=='corner':
            corner1={'N':['E']}
            corner2={'E':['S']}
            corner3={'S':['W']}
            corner4={'W':['S']}

            if self._orientation==0:
                return corner1.get(side,[])
            elif self._orientation==1:
                return corner2.get(side,[])
            elif self._orientation==2:
                return corner3.get(side,[])
            else:
                return corner4.get(side,[])

        elif self._name=='junction-t':
            junction_t1={'W':['S','E'],'S':['W','E'],'E':['W','S']}
            junction_t2={'N':['S','W'],'S':['N','W'],'W':['S','N']}
            junction_t3={'E':['N','W'],'N':['E','W'],'W':['N','E']}
            junction_t4={'S':['N','E'],'N':['S','E'],'E':['S','N']}

            if self._orientation==0:
                return junction_t1.get(side,[])
            elif self._orientation==1:
                return junction_t2.get(side,[])
            elif self._orientation==2:
                return junction_t3.get(side,[])
            else:
                return junction_t4.get(side,[])

        elif self._name=='diagonals':
            diagonals1={'N':['E'],'W':['S']}
            diagonals2={'N':['W'],'E':['S']}

            if self._orientation==0 or self._orientation==2:
                return diagonals1.get(side,[])
            else:
                return diagonals2.get(side,[])

        else:
            over_under1={'E':['W'],'W':['E'],'N':['S'],'S':['N']}
            over_under2={'N':['S'],'S':['N'],'E':['W'],'W':['E']}

            if self._orientation==0 or self._orientation==2 :
                return over_under1.get(side,[])
            else:
                return over_under2.get(side,[])
            
    def __str__(self):
        """
        (str) Returns the string representation of the Pipe.
        
        """
        return f"Pipe('{self._name}', {self._orientation})"

    def __repr__(self):
        """
        (str) Returns the string representation of the Pipe.
        
        """
        return f"Pipe('{self._name}', {self._orientation})"


class SpecialPipe(Pipe):
    """
    The representation of the start and end pipes in the game

    """

    def get_id(self):
        
        """
        (str) Return the id of the specialpipe class.
        
        """
        return 'special_pipe'       

    def __str__(self):
        """
        (str) Returns the string representation of the Special Pipes.
        
        """
        return f"SpecialPipe({self._orientation})"

    def __repr__(self):
        """
        (str) Returns the string representation of the Special Pipes.
        
        """
        return f"SpecialPipe({self._orientation})"        

        
class StartPipe(SpecialPipe):
    """
    A StartPipe represents the start pipe in the game.

    """
    def __init__(self,orientation=0):
        """
        Construct a start pipe object given their orientation.

        Parameters:
            orientation(int): The orientation of start pipe.

        """
        super().__init__("start", orientation)
    
    def get_connected(self, side=None):
        """
        list<str> Returns the direction that the start pipe is facing.

        """
        start_side=[]
        if self._orientation==1:
            start_side.append('E')
            return start_side
        elif self._orientation==2:
            start_side.append('S')
            return start_side
        elif self._orientation==3:
            start_side.append('W')
            return start_side
        else:
            start_side.append('N')
            return start_side

    def __str__(self):
        """
        (str) Returns the string representation of the Start Pipe.
        
        """
        return f"StartPipe({self._orientation})"

    def __repr__(self):
        """
        (str) Returns the string representation of the Start Pipe.
        
        """
        return f"StartPipe({self._orientation})"        


class EndPipe(SpecialPipe):
    """
    An EndPipe represents the end pipe in the game.

    """
    def __init__(self,orientation=0):
        """
        Construct an end pipe object given their orientation.

        Parameters:
            orientation(int): The orientation of end pipe.

        """
        super().__init__("end", orientation)
    
    def get_connected(self, side=None):
        """
        list<str> Returns the direction that the end pipe is facing.

        """
        end_side=[]
        if self._orientation==1:
            end_side.append('W')
            return end_side
        elif self._orientation==2:
            end_side.append('N')
            return end_side
        elif self._orientation==3:
            end_side.append('E')
            return end_side
        else:
            end_side.append('S')
            return end_side

    def __str__(self):
        """
        (str) Returns the string representation of the End Pipe.
        
        """
        return f"EndPipe({self._orientation})"

    def __repr__(self):
        """
        (str) Returns the string representation of the End Pipe.
        
        """
        return f"EndPipe({self._orientation})" 

    
class PipeGame:
    """
    A game of Pipes.
    """
    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        
        
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
##        board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
##        Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
##        Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
##        Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
##        Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
##        [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
##        Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
##        Tile('tile', True), Tile('tile', True)]]
##
##        playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
##
        self._board_layout,self._playable_pipes=self.load_file(game_file)
        self._start,self._end=None,None
        self._start=self.get_starting_position()
        self._end=self.get_ending_position()
        #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################

        ### add code here ###

    def load_file(self, filename: str):
        """


        """
        import csv
        
        with open(filename,'r') as file:
            reader=csv.reader(file)
            board=[row for row in reader]
            board_layout=[]
            playable_pipes=dict()
            for i,j in enumerate(['corner','cross','diagonals','junction-t','over-under','straight']):
                x=board[6][i]
                playable_pipes.update({j:int(x)})
            board.pop()
            for row in board:
                rows=[]
                for col in row:
                    if col=='#':
                        rows.append(Tile('tile',True))

                    elif col.isalpha():
                        orientation=0
                        if  col == 'JT':
                            rows.append(Pipe('junction-t', orientation, False))
                        elif col == 'E':
                            rows.append(EndPipe(orientation))
                        elif col == 'L':
                            rows.append(Tile('locked', False))
                            
                    else:
                        x=col[:-1]
                        y=int(col[-1])
                        if x == 'S':
                            rows.append(StartPipe(y))
                        elif x == 'E':
                            rows.append(EndPipe(y))
                                                                
                board_layout.append(rows)
            return board_layout,playable_pipes
                        
        
    def get_board_layout(self):
        """
        (list<list<Tile, ...>>) Returns a list of lists,
                                i.e. a list where each element is
                                a list representation of the row
                                (each row list contains the Tile instances
                                for each column in that row).
        
        """
        return self._board_layout

    def get_playable_pipes(self):
        """
        (dict<str:int>) Returns a dictionary of all the playable pipes
                         (the pipe types) and number of times
                         each pipe can be played.
                         
        """
        return self._playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int):
        """
        Add the quantity of playable pipes of type specified by pipe_name to number (in the selection panel).
                         
        """
        self._playable_pipes[pipe_name]+=number

    def get_pipe(self, position):
        """
        (Pipe|Tile)  Returns the Pipe at the position or the tile if there is no pipe at that position.

        """
        return self._board_layout[position[0]][position[1]]

    def set_pipe(self, pipe: Pipe, position):
        """
        Place the specified pipe at the given position (row, col) in the game board.
        The number of available pipes of the relevant type should also be updated
        
        """
        self._board_layout[position[0]][position[1]]=pipe
        self.change_playable_amount(pipe.get_name(),-1)

    def remove_pipe(self, position):
        """
        Removes the pipe at the given position from the board.
        
        """
        pipename=self._board_layout[position[0]][position[1]].get_name()
        self.change_playable_amount(pipename,+1)
        self._board_layout[position[0]][position[1]]=Tile('tile', True)
        return None

    def valid_position(self,position):
        """
        (bool) Return True if position of pipe is in the board_layout, which means it's a valid position.
               Return False if position of pipe is not in the board_layout, which means it's an invalid position.


        """
        if position[0]<0 or position[0]>=len(self._board_layout) or position[1]<0 or position[1]>=len(self._board_layout[0]):
            return False
        else:
            return True

    def pipe_in_position(self, position):
        """
         Pipe: Returns the pipe in the given position (row, col) of the game board if there is a Pipe in the given position.
               Returns None if the position given is None or if the object in the given position is not a Pipe.
               
        """
        pipe=self._board_layout[position[0]][position[1]]
        if self.valid_position(position):
            if pipe.get_id()=='pipe' or pipe.get_id()=='special_pipe':
                return pipe
        elif position==None:
            return None
        else:
            return None

    def position_in_direction(self, direction, position):
        """
         tuple<str, tuple<int, int>> Returns the direction and position (row, col) in the given direction from the given position,
                                     if the resulting position is within the game grid, i.e. valid.
                                     Returns None if the resulting position would be invalid.

        """
        pn=self._board_layout[position[0]][position[1]]
        if pn==None:
            return None
        elif direction=='E' and self.valid_position((position[0],position[1]+1)):
            return ('W',(position[0],position[1]+1))
        elif direction=='N' and self.valid_position((position[0]-1,position[1])):
            return ('S',(position[0]-1,position[1]))
        elif direction=='S' and self.valid_position((position[0]+1,position[1])):
            return ('N',(position[0]+1,position[1]))
        elif direction=='W' and self.valid_position((position[0],position[1]-1)):
            return ('E',(position[0],position[1]-1))
        else:
            return None
        
    
    def end_pipe_positions(self):
        """
        Find and save the start and end pipe positions from the game board.

        """
        self._start
        self._end
        
    def get_starting_position(self):
        """                                       
        (tuple<int, int>) Returns the (row, col) position of the start pipe.
        
        """
        if self._start!=None:
            return self._start
        for i in range(len(self._board_layout)):
            for j in range(len(self._board_layout[i])):
                if "StartPipe" in str(self._board_layout[i][j]):
                    start_position=(i,j)
                    return start_position

    def get_ending_position(self):
        """                                       
        (tuple<int, int>) Returns the (row, col) position of the end pipe.
        """
        if self._end!=None:
            return self._end
        for i in range(len(self._board_layout)):
            for j in range(len(self._board_layout[i])):
                if "EndPipe" in str(self._board_layout[i][j]):
                    end_position=(i,j)
                    return end_position                                            
                    
    
    def check_win(self):
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):

                if self.position_in_direction(direction, position) is None:
                    new_direction = None 
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                         new_position).get_connected()[0]:
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False
    

def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
