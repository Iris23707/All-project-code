from a1_support import *

def display_game(game,grid_size):
    """This function prints out a grid-shaped representation of the game.
    Parameters:
		game (str): Game string.
 		grid_size (int): Size of game.

	Returns:
        None
    """
    row_wall = '----'*(grid_size+1)
    #first row
    str_print = '  | '
    for i in range(grid_size):
        #samll number
        if i < 9:
            str_print = str_print+str(i+1)+' | '
        else:
            str_print = str_print+str(i+1)+'| '
    print(str_print[:-1])
    print(row_wall)
    #2 to end row
    for i in range(grid_size):
        str_print = ALPHA[i]+' | '
        for j in range(grid_size):
            str_print = str_print+game[i*grid_size+j]+' | '
        print(str_print[:-1])
        print(row_wall)

def parse_position(action,grid_size):
    """This function checks if the input action is in a valid format.
    If a non-valid action is entered, None should be returned.
    If the action is \Select a cell" or
    Flag/remove a cell", the position of the cell should be returned as a tuple.
    Parameters:
		action (str): user action.
 		grid_size (int): Size of game.

	Returns:
        None or postion(tuple)
    """
    if action == None or len(action) == 0:
        return None
    #'-Upper Case Character--number-'
    if action[0] in ALPHA[:grid_size] and action[1:].isdigit():
        if 0 <= int(action[1:]) <= grid_size:
            return (ALPHA.index(action[0]),int(action[1:])-1)
    return None

def position_to_index(position, grid_size):
    """This function should convert the row, column coordinate in the grid 
    to the game strings index.
    Parameters:
		position (tuple): position.
 		grid_size (int): Size of game.

	Returns:
        index of the cell in the game string (int)
    """
    return position[0]*grid_size+position[1]

def replace_character_at_index(game, index, character):
    """This function returns an updated game string
    with the specied character placed at the specied index.
    Parameters:
        game (str): Game string.
		index (int): index of character.
 		character (str): character to place.

	Returns:
        game (str): Game string.
    """
    game = game[:index]+character+game[index+1:]
    return game

def flag_cell(game, index):
    """This function returns an updated game string
    after "toggling" the ag at the specied index in the game string.
    Parameters:
        game (str): Game string.
		index (int): index of game position.

	Returns:
        game (str): Game string.
    """
    if game[index] != FLAG:
        #not flagged
        game = replace_character_at_index(game, index, FLAG)
    else:
        #flagged
        game = replace_character_at_index(game, index, UNEXPOSED)
    return game

def index_in_direction(index, grid_size, direction):
    """This function takes in the index to a cell in the game string
    and returns a new index corresponding to an 
    adjacent cell in the specied direction. Return None for invalid directions.
    Parameters:
		index (int): index of game position.
        grid_size (int): Size of game.
        direction (str): direction(left,right,...).

	Returns:
        index (int): index of game position.
    """
    pos_to_return = 0
    #position to return
    if direction == 'up':
        pos_to_return = index-grid_size
    if direction == 'down':
        pos_to_return = index+grid_size
    if direction == 'left':
        pos_to_return = index-1
        if (pos_to_return+1)%grid_size == 0:
            return None
    if direction == 'right':
        pos_to_return = index+1
        if (pos_to_return)%grid_size == 0:
            return None
    if direction == 'up-right':
        pos_to_return = index-grid_size+1
        if (pos_to_return)%grid_size == 0:
            return None
    if direction == 'up-left':
        pos_to_return = index-grid_size-1
        if (pos_to_return+1)%grid_size == 0:
            return None
    if direction == 'down-right':
        pos_to_return = index+grid_size+1
        if (pos_to_return)%grid_size == 0:
            return None
    if direction == 'down-left':
        pos_to_return = index+grid_size-1
        if (pos_to_return+1)%grid_size == 0:
            return None
    if 0 <= pos_to_return < grid_size*grid_size:
        return pos_to_return
    return None

def directions_to_int(index,grid_size,directions):
    """This function convert list of direction to list of int
    Parameters:
		index (int): index of game position.
        grid_size (int): Size of game.
        direction (str): direction(left,right,...).

	Returns:
        index (int): index of game position.
    """
    res=[]
    #results to return
    for direction in directions:
        res.append(index_in_direction(index, grid_size, direction))
    return res

def neighbour_directions(index, grid_size):
    """This function returns a list of indexes that have a neighbouring cell.
    Parameters:
		index (int): index of game position.
        grid_size (int): Size of game.

	Returns:
        indexs (list<int>): indexes of game position that have a neighbouring cell.
    """
    #4 corner
    if index == 0:
        directions = ['down','right','down-right']
        return directions_to_int(index,grid_size,directions)
    if index == grid_size*grid_size-1:
        directions = ['up','left','up-left']
        return directions_to_int(index,grid_size,directions)
    if index == grid_size-1:
        directions = ['down','left','down-left']
        return directions_to_int(index,grid_size,directions)
    if index == grid_size*grid_size-grid_size:
        directions = ['up','right','up-right']
        return directions_to_int(index,grid_size,directions)
    
    # 4 edge 
    if index< grid_size:
        directions = ['down','right','left','down-right','down-left']
        return directions_to_int(index,grid_size,directions)
    if index > grid_size*grid_size-grid_size:
        directions = ['up','right','left','up-right','up-left']
        return directions_to_int(index,grid_size,directions)
    if index%grid_size == 0:
        directions = ['up','down','right','up-right','down-right']
        return directions_to_int(index,grid_size,directions)
    if (index+1)%grid_size == 0:
        directions = ['up','down','left','up-left','down-left']
        return directions_to_int(index,grid_size,directions)
    
    #middle
    return directions_to_int(index,grid_size,DIRECTIONS)

def number_at_cell(game, pokemon_locations, grid_size, index):
    """This function returns the number of Pokemon in neighbouring cells.
    Parameters:
        game (str): Game string.
        pokemon_locations (list<int>): pokemons locations
        grid_size (int): Size of game.
        index (int): index of game position.

	Returns:
        num (int): number of Pokemon in neighbouring cells
    """
    num = 0
    # number of Pokemon in neighbouring cells
    neighbours = neighbour_directions(index,grid_size)
    for neighbour in neighbours:
        if neighbour in pokemon_locations:
            num += 1
    return num

def check_win(game, pokemon_locations):
    """This function returns True if the player has won the game, and returns False otherwise.
    Parameters:
        game (str): Game string.
        pokemon_locations (list<int>): pokemons locations

	Returns:
        win? (bool): win or not
    """
    #traverse game
    for i in range(len(game)):
        if game[i] == FLAG:#flagged
            if i not in pokemon_locations:
                return False
        elif game[i] == '~':
            return False
    return True

# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
def big_fun_search(game, grid_size, pokemon_locations, index):
    """Searching adjacent cells to see if there are any Pokemon"s present.
    
    Using some sick algorithms.
    
    Find all cells which should be revealed when a cell is selected.
    
    For cells which have a zero value (i.e. no neighbouring pokemons) all the cell"s
    neighbours are revealed. If one of the neighbouring cells is also zero then
    all of that cell"s neighbours are also revealed. This repeats until no
    zero value neighbours exist.

    For cells which have a non-zero value (i.e. cells with neightbour pokemons), only 	the cell itself is revealed.

    Parameters:
		game (str): Game string.
 		grid_size (int): Size of game.
		pokemon_locations (tuple<int, ...>): Tuple of all Pokemon's locations.
 		index (int): Index of the currently selected cell

	Returns:
    (list<int>): List of cells to turn visible.
    """
    queue = [index]
    discovered = [index]
    visible = []

    if game[index] == FLAG:
    	return queue

    number = number_at_cell(game, pokemon_locations, grid_size, index)
    if number != 0:
        return queue

    while queue:
        node = queue.pop()
        for neighbour in neighbour_directions(node, grid_size):
            if neighbour in discovered or neighbour is None:
                continue

            discovered.append(neighbour)
            if game[neighbour] != FLAG:
                number = number_at_cell(game, pokemon_locations, grid_size, neighbour)
                if number == 0:
                    queue.append(neighbour)
            visible.append(neighbour)
    return visible
# #########################UNCOMMENT THIS FUNCTION WHEN READY#######################


def main():
    """Main function to run a game

    Parameters:
		None

	Returns:
        None
    """
    grid_size = ''
    pokemons_num = ''

    #input grid_size
    while True:
        grid_size = input('Please input the size of the grid: ')
        if grid_size.isdigit() == True and 1 <= int(grid_size) <= 26:
            break
    #input pokemons_num
    while pokemons_num.isdigit() == False:
        pokemons_num = input('Please input the number of pokemons: ')
    grid_size = int(grid_size)
    pokemons_num = int(pokemons_num)

    #initalize game
    pokemon_locations = generate_pokemons(grid_size, pokemons_num)
    #print(pokemon_locations)
    game = UNEXPOSED*(grid_size**2)
    
    display_game(game,grid_size)

    #loop until win or lose
    while True:
        print('')
        user_input = input('Please input action: ')
        #no input
        if len(user_input) == 0:
            print("That ain't a valid action buddy.")
            display_game(game,grid_size)
            continue
        #help
        if user_input == 'h':
            print(HELP_TEXT)
            display_game(game,grid_size)
            continue
        #quit
        if user_input == 'q':
            input_tmp = input('You sure about that buddy? (y/n): ')
            if input_tmp == 'y':
                print('Catch you on the flip side.')
                break
            elif input_tmp == 'n':
                print("Let's keep going.")
                display_game(game,grid_size)
                continue
            else:
                print("That ain't a valid action buddy.")
                display_game(game,grid_size)
                continue
        #restart
        if user_input == ':)':
            game = UNEXPOSED*(grid_size**2)
            pokemon_locations = generate_pokemons(grid_size, pokemons_num)
            print("It's rewind time.")
            display_game(game,grid_size)
            continue
        #flag
        if user_input[0] == 'f':
            user_input = user_input[2:]
            position = parse_position(user_input,grid_size)
            if position != None:
                index_tmp = position_to_index(position,grid_size)
                game = flag_cell(game, index_tmp)
            else:
                print("That ain't a valid action buddy.")
            display_game(game,grid_size)
        else:
            position = parse_position(user_input,grid_size)
            if position != None:
                #valid action
                index_tmp = position_to_index(position,grid_size)
                #if position flagged
                if game[index_tmp] == FLAG:
                    display_game(game,grid_size)
                    continue
                #lose
                if position_to_index(position,grid_size) in pokemon_locations:
                    for loc in pokemon_locations:
                        game = replace_character_at_index(game,loc,POKEMON)
                    display_game(game,grid_size)
                    print('You have scared away all the pokemons.')
                    break
                #next step
                positions_to_show = big_fun_search(game, grid_size, pokemon_locations, position_to_index(position,grid_size))
                game = replace_character_at_index(game, index_tmp, str(number_at_cell(game, pokemon_locations, grid_size, index_tmp)))
                for posi in positions_to_show:
                    #if flagged
                    if game[posi] == FLAG:
                        continue
                    game = replace_character_at_index(game, posi, str(number_at_cell(game, pokemon_locations, grid_size, posi)))
            else:#not valid action
                print("That ain't a valid action buddy.")
            display_game(game,grid_size)
        #check win
        if check_win(game, pokemon_locations) == True:
            print('You win.')
            break
            

if __name__ == "__main__":
    main()
