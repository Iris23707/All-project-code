import tkinter as tk
import random
import time
from random import choice
from tkinter import messagebox

TASK_ONE = "task1"
TASK_TWO = "task2"
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
DIRECTIONS = (UP, DOWN, LEFT, RIGHT,
              f"{UP}-{LEFT}", f"{UP}-{RIGHT}",
              f"{DOWN}-{LEFT}", f"{DOWN}-{RIGHT}")
WALL_VERTICAL = "|"
WALL_HORIZONTAL = "-"
POKEMON = "☺"
FLAG = "♥"
UNEXPOSED = "~"
EXPOSED = "0"
INVALID = "That ain't a valid action buddy."
HELP_TEXT = """h - Help.
<Uppercase Letter><number> - Selecting a cell (e.g. 'A1')
f <Uppercase Letter><number> - Placing flag at cell (e.g. 'f A1')
:) - Restart game.
q - Quit.
"""


# the manager class
class BoardModel:
    """
    Storing and managing the internal game state.
    """

    def __init__(self, grid_size, num_pokemon):
        """
        Construct a boardmodel with a given name.

        Parameters:
            grid_size (int): the number of rows (equal to the number of columns) in the board.
            num_pokemon (int):  the number of hidden pokemon.
        """
        self._game_board = UNEXPOSED * (grid_size ** 2)
        self._num_pokemon = num_pokemon
        self._pokemon_location = self.generate_pokemons(grid_size)

    def generate_pokemons(self, grid_size):
        """Pokemons will be generated and given a random index within the game.

        Parameters:
            grid_size (int): The grid size of the game.
            number_pokemon (int): The number of pokemons that the game will have.

        Returns:
            (tuple<int>): A tuple containing  indexes where the pokemons are
            created for the game string.
        """
        cell_count = grid_size ** 2
        pokemon_locations = ()
        for _ in range(self._num_pokemon):
            if len(pokemon_locations) >= cell_count:
                break
            index = random.randint(0, cell_count - 1)

            while index in pokemon_locations:
                index = random.randint(0, cell_count - 1)

            pokemon_locations += (index,)
        return pokemon_locations

    def replace_character_at_index(self, index, character):
        """A specified index in the game string at the specified index is replaced by
        a new character.
        Parameters:
            index (int): The index in the game string where the character is replaced.
            character (str): The new character that will be replacing the old character.

        Returns:
            (str): The updated game string.
        """
        self._game_board = self.get_game()[:index] + character + self.get_game()[index + 1:]
        return self._game_board

    def flag_cell(self, index):
        """Toggle Flag on or off at selected index. If the selected index is already
            revealed, the game would return with no changes.

            Parameters:
                index (int): The index in the game string where a flag is placed.
            Returns
                (str): The updated game string.
        """
        if self.get_game()[index] == FLAG:
            self._game_board = self.replace_character_at_index(index, UNEXPOSED)

        elif self.get_game()[index] == UNEXPOSED:
            self._game_board = self.replace_character_at_index(index, FLAG)

        return self._game_board

    def index_in_direction(self, index, grid_size, direction):
        """The index in the game string is updated by determining the
        adjacent cell given the direction.
        The index of the adjacent cell in the game is then calculated and returned.

        For example:
          | 1 | 2 | 3 |
        A | i | j | k |
        B | l | m | n |
        C | o | p | q |

        The index of m is 4 in the game string.
        if the direction specified is "up" then:
        the updated position corresponds with j which has the index of 1 in the game string.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.
            direction (str): The direction of the adjacent cell.

        Returns:
            (int): The index in the game string corresponding to the new cell position
            in the game.

        """
        # convert index to row, col coordinate
        col = index % grid_size
        row = index // grid_size
        if RIGHT in direction:
            col += 1
        elif LEFT in direction:
            col -= 1
        # Notice the use of if, not elif here
        if UP in direction:
            row -= 1
        elif DOWN in direction:
            row += 1
        if not (0 <= col < grid_size and 0 <= row < grid_size):
            return None
        return row * grid_size + col

    def neighbour_directions(self, index, grid_size):
        """Seek out all direction that has a neighbouring cell.

        Parameters:
            index (int): The index in the game string.
            grid_size (int): The grid size of the game.

        Returns:
            (list<int>): A list of index that has a neighbouring cell.
        """
        neighbours = []
        for direction in DIRECTIONS:
            neighbour = self.index_in_direction(index, grid_size, direction)
            if neighbour is not None:
                neighbours.append(neighbour)

        return neighbours

    def number_at_cell(self, pokemon_locations, grid_size, index):
        """Calculates what number should be displayed at that specific index in the game.

        Parameters:
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell

        Returns:
            (int): Number to be displayed at the given index in the game string.
        """
        if self.get_game()[index] != UNEXPOSED:
            return int(self.get_game()[index])

        number = 0
        for neighbour in self.neighbour_directions(index, grid_size):
            if neighbour in pokemon_locations:
                number += 1

        return number

    def reveal_cells(self, grid_size, pokemon_locations, index):
        """Reveals all neighbouring cells at index and repeats for all
        cells that had a 0.

        Does not reveal flagged cells or cells with Pokemon.

        Parameters:
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            grid_size (int): Size of game.
            index (int): Index of the currently selected cell



        Returns:
            (str): The updated game string
        """
        number = self.number_at_cell(pokemon_locations, grid_size, index)
        self.replace_character_at_index(index, str(number))
        clear = self.big_fun_search(grid_size, pokemon_locations, index)
        for i in clear:
            if self._game_board[i] != FLAG:
                number = self.number_at_cell(pokemon_locations, grid_size, i)
                self.replace_character_at_index(i, str(number))

        return self._game_board

    def big_fun_search(self, grid_size, pokemon_locations, index):
        """Searching adjacent cells to see if there are any Pokemon"s present.

        Using some sick algorithms.

        Find all cells which should be revealed when a cell is selected.

        For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
        neighbours are revealed. If one of the neighbouring cells is also zero then
        all of that cell"s neighbours are also revealed. This repeats until no
        zero value neighbours exist.

        For cells which have a non-zero value (i.e. cells with neighbour pokemons), only
        the cell itself is revealed.

        Parameters:
            grid_size (int): Size of game.
            pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
            index (int): Index of the currently selected cell

        Returns:
            (list<int>): List of cells to turn visible.
        """
        queue = [index]
        discovered = [index]
        visible = []

        if self.get_game()[index] == FLAG:
            return queue

        number = self.number_at_cell(pokemon_locations, grid_size, index)
        if number != 0:
            return queue

        while queue:
            node = queue.pop()
            for neighbour in self.neighbour_directions(node, grid_size):
                if neighbour in discovered:
                    continue

                discovered.append(neighbour)
                if self._game_board[neighbour] != FLAG:
                    number = self.number_at_cell(pokemon_locations, grid_size, neighbour)
                    if number == 0:
                        queue.append(neighbour)
                visible.append(neighbour)
        return visible

    def get_game(self):
        """
        Returns an appropriate representation of the current state of the game board.
        """
        return self._game_board

    def get_pokemon_location(self):
        """
        Returns the indices describing all pokemon locations.
        """
        return self._pokemon_location

    def index_to_position(self, index):
        """
        Returns the (row, col) coordinate corresponding to the supplied index.
        """
        col = index % self._grid_size
        row = index // self._grid_size
        return row, col

    def check_win(self):
        """
        Returns True if the game has been lost, else False.
        """
        return UNEXPOSED not in self.get_game() and self.get_game().count(FLAG) == len(self.get_pokemon_location)

    def check_loss(self):
        """
        Returns True iff the game has been lost, else False.
        """
        return POKEMON in self.get_game()

    def check_pokemon(self, index):
        """
        Returns the (row, col) of pokemon.
        """
        if index in self._pokemon_location:
            self._num_pokemon -= 1
            return index

#the view class
class BoardView(tk.Canvas):
    """
    Representing the GUI for the board.
    """

    def __init__(self, master, grid_size, board_width=600, *args, **kwargs):
        """
        Construct a boardview with a given name.
        Parameters:
            master (tk.Widget): Widget within which to place the selection view.
            grid_size (int): the number of rows (equal to the number of columns) in the board.
            board_width(int): the number of pixels the board should span (both width and height).
        """

        super().__init__(master)
        self._master = master
        self._grid_size = grid_size
        self._board_width = board_width
        self._board = None

        self.config(height=board_width, width=board_width)

    def draw_board(self, board: BoardModel):
        """
        Given an appropriate representation of the current state of the game board,
        draw the view to reflect this game state.

        """
        self._board = board
        self.delete(tk.ALL)

        for i in range(self._grid_size):
            for j in range(self._grid_size):
                char = self._board.get_game()[self.position_to_index((j, i), self._grid_size)]
                x1 = i * 60
                y1 = j * 60
                x2 = x1 + 60
                y2 = y1 + 60

                if char == UNEXPOSED:
                    self.create_rectangle(x1, y1, x2, y2, fill="green")
                elif char == POKEMON:
                    self.create_rectangle(x1, y1, x2, y2, fill="yellow")
                elif char.isdigit():
                    self.create_rectangle(x1, y1, x2, y2, fill="#90EE90")
                    self.create_text(x1 + 60 / 2, y1 + 60 / 2, text=int(char))
                elif char == FLAG:
                    self.create_rectangle(x1, y1, x2, y2, fill="red")

        self.bind_clicks()

    def bind_clicks(self):
        """
        Bind clicks on a label to the left and right click handlers.
        """
        self.bind("<Button-1>", lambda e: self._handle_left_click((e.x, e.y)))
        self.bind("<Button-2>", lambda e: self._handle_right_click((e.x, e.y)))
        self.bind("<Button-3>", lambda e: self._handle_right_click((e.x, e.y)))

    def _handle_left_click(self, pixel):
        """
        Clicking to expose cell.
        """
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position, self._grid_size)
        if self._board.check_pokemon(index):

            for index in self._board.get_pokemon_location():
                self._board.replace_character_at_index(index, POKEMON)
            self.draw_board(self._board)

            if self._board.check_loss():
                messagebox.showinfo("Game over","You lose! Would you like to play again?")
                raise SystemExit


        else:
            self._board.reveal_cells(self._grid_size, self._board.get_pokemon_location(), index)
            self.draw_board(self._board)

            if self._board.check_win():
                messagebox.showinfo("Game over","You win!")
                raise SystemExit


    def _handle_right_click(self, pixel):
        """
        Handle right clicking on presenting or cancelling pokeballs.
        """
        position = self.pixel_to_position(pixel)
        index = self.position_to_index(position, self._grid_size)

        self._board.flag_cell(index)
        self.draw_board(self._board)

    def position_to_index(self, position, grid_size):
        """Convert the row, column coordinate in the grid to the game strings index.

        Parameters:
            position (tuple<int, int>): The row, column position of a cell.
            grid_size (int): The grid size of the game.

        Returns:
            (int): The index of the cell in the game string.
        """
        x, y = position
        return x * grid_size + y

    def pixel_to_position(self, pixel):
        """
        Converts the supplied pixel to the position of the cell it is contained within

        """
        x, y = pixel
        return y // 60, x // 60

class StatusBar(tk.Frame):
    """
    Add a StatusBar class that inherits from tk.Frame
    """
    def __init__(self, master, num_pokemon):
        """
        A game timer, attempted catches and pokeballs.

        Parameters:
            master (tk.Widget): Widget within which to place the selection panel.
            num_pokemon(int): The number of hidden pokemon.

        """
        super().__init__(master)
        self._num_pokemon = num_pokemon
        self._master = master
        self.pokeballs = 0

        #insert image of pokeball
        frame1 = tk.Frame(self._master)
        frame1.pack(side=tk.LEFT)

        self.ballimage = tk.PhotoImage(file="./images/full_pokeball.gif")
        self.ball = tk.Label(frame1, image=self.ballimage)
        self.ball.pack(side=tk.LEFT)

        self.balls = frame1
        self.ballup = tk.Label(self.balls, text=f'{self.pokeballs} attemped catches')
        self.ballup.pack(side=tk.TOP)
        self.balldown = tk.Label(self.balls, text=f'{self._num_pokemon - self.pokeballs} pokeballs left')
        self.balldown.pack(side=tk.BOTTOM)
        self.balls.pack(side=tk.LEFT)

        #insert image of clock
        frame2 = tk.Frame(self._master)
        frame2.pack(side=tk.LEFT)

        self.clockimage = tk.PhotoImage(file="./images/clock.gif")
        self.clock = tk.Label(frame2, image=self.clockimage)
        self.clock.pack(side=tk.LEFT)

        #insert the  button of "New game" and " Restart game"
        self.buttons = tk.Frame(self)
        self.n = tk.Button(self.buttons, text="New game")
        self.r = tk.Button(self.buttons, text="Restart game")
        self.n.pack(side=tk.TOP)
        self.r.pack(side=tk.BOTTOM)
        self.buttons.pack(side=tk.RIGHT)


# a new view class
class ImageBoardView(BoardView):
    """
    Extending the existing BoardView class, and images should be used to display each square rather than rectangles.
    """

    def __init__(self,master, grid_size, board_width=600, *args, **kwargs):
        """
        Construct a boardview with a given name.

        Parameters:
            master (tk.Widget): Widget within which to place the selection view.
            grid_size (int): the number of rows (equal to the number of columns) in the board.
            board_width(int): the number of pixels the board should span (both width and height).
        """
        super().__init__(master,grid_size, board_width=600, *args, **kwargs)

    def draw_board(self, board: BoardModel):
        """
        Given an appropriate representation of the current state of the game board,
        draw the view to reflect this game state.
        """
        self._picture=[]
        self._board = board
        self.delete(tk.ALL)

        for i in range(self._grid_size):
            for j in range(self._grid_size):
                char = self._board.get_game()[self.position_to_index((j, i), self._grid_size)]
                x1 = i * 60
                y1 = j * 60
                x2 = x1 + 60
                y2 = y1 + 60

                #insert the image of unexposed cell
                if char == UNEXPOSED:
                    photo=tk.PhotoImage(file="./images/unrevealed.gif")


                # insert the image of exposed cell
                elif char == EXPOSED:
                    photo=tk.PhotoImage(file="./images/zero_adjacent.gif")

                # insert the image of cell of pokemon
                elif char == POKEMON:
                    pokemon_list=["./images/pokemon_sprites/charizard.gif",
                                  "./images/pokemon_sprites/cyndaquil.gif",
                                  "./images/pokemon_sprites/pikachu.gif",
                                  "./images/pokemon_sprites/psyduck.gif",
                                  "./images/pokemon_sprites/togepi.gif"]
                    a=random.choice(pokemon_list)
                    photo = tk.PhotoImage(file=a)
                    print(a)

                # insert the image of cell of digit
                elif char.isdigit():
                    if char=="1":
                        photo = tk.PhotoImage(file="./images/one_adjacent.gif")

                    elif char=="2":
                        photo = tk.PhotoImage(file="./images/two_adjacent.gif")

                    elif char=="3":
                        photo = tk.PhotoImage(file="./images/three_adjacent.gif")

                    elif char=="4":
                        photo = tk.PhotoImage(file="./images/four_adjacent.gif")

                    elif char=="5":
                        photo = tk.PhotoImage(file="./images/five_adjacent.gif")

                    elif char=="6":
                        photo = tk.PhotoImage(file="./images/six_adjacent.gif")

                    elif char=="7":
                        photo = tk.PhotoImage(file="./images/seven_adjacent.gif")

                    else:
                        photo = tk.PhotoImage(file="./images/eight_adjacent.gif")

                # insert the image of pokeball
                elif char == FLAG:
                    photo = tk.PhotoImage(file="./images/pokeball.gif")

                self.create_image(x1 + 60 / 2, y1 + 60 / 2, image=photo)
                self._picture.append(photo)

        self.bind_clicks()



# the controller class
class PokemonGame:
    """
    Managing necessary communication between any model and view classes, as well as event handling.
    """

    def __init__(self, master, grid_size=10, num_pokemon=15, task=TASK_TWO):
        """
        Create a name app within a master widget.

        Parameters:
            grid size(int): the number of rows (equal to the number of columns) in the board.
            num_pokemon(int): The number of hidden pokemon.
            TASK ONE(str): some constant that allows the game to be displayed.
        """
        self._master = master
        self._grid_size = grid_size
        self._num_pokemon = num_pokemon
        self._task=task
        self._model = BoardModel(self._grid_size, num_pokemon)
        self._board = None
        self.draw()

    def draw(self):
        """
        Draw the game to the master widget.
        """
        #create the label of the game
        label = tk.Label(self._master,
                         bg="lightcoral",
                         fg="white",
                         text="Pokemon: Got 2 Find Them All!",
                         font=('Times New Roman', 20, 'bold'),
                         heigh=2)
        label.pack(fill=tk.X)

        #the transformation between task_one and task_two
        if self._task==TASK_ONE:
            self._board = BoardView(self._master, self._grid_size, self._grid_size * 60)

        else:
            self._board = ImageBoardView(self._master, self._grid_size, self._grid_size * 60)

        self._board.pack()
        self._board.draw_board(self._model)

        self._bar = StatusBar(self._master, self._num_pokemon)
        self._bar.pack()



def main():
    root = tk.Tk()
    root.title("Pokemon: Got 2 Find Them All!")
    root.resizable(False, False)
    PokemonGame(root)
    root.update()
    root.mainloop()



if __name__ == "__main__":
    main()
