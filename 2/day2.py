import sys

def first_strategy(lines):
    points = 0
    for line in lines:
        encrypted_opponent_move, encrypted_player_move = line.split(' ')
        # Rock: 1; Paper: 2; Scissors: 3
        if 'A' <= encrypted_opponent_move <= 'C':
            opponent_move = ord(encrypted_opponent_move) - ord('A') + 1
        if 'X' <= encrypted_player_move <= 'Z':
            player_move = ord(encrypted_player_move) - ord('X') + 1

        points += player_move
        # Draw
        if player_move == opponent_move:
            points += 3
        # Win
        elif (player_move - opponent_move) % 3 == 1:
            points += 6
        # Loss: do nothing
    print('Points earned with first strategy:', points)

def second_strategy(lines):
    points = 0

    for line in lines:
        encrypted_opponent_move, encrypted_player_strategy = line.split(' ')
        # Rock: 0; Paper: 1; Scissors: 2
        if 'A' <= encrypted_opponent_move <= 'C':
            opponent_move = ord(encrypted_opponent_move) - ord('A')
        # Loss: 0; Draw: 3; Win: 6
        if 'X' <= encrypted_player_strategy <= 'Z':
            player_strategy = (ord(encrypted_player_strategy) - ord('X')) * 3

        # Convert {0,1,2} to {1,2,3}
        points += 1
        # Loss: losing move
        if player_strategy == 0:
            points += (opponent_move - 1) % 3
        # Draw: same move
        elif player_strategy == 3:
            points += opponent_move
        # Win: winning move
        elif player_strategy == 6:
            points += (opponent_move + 1) % 3

        points += player_strategy

    print('Points earned with second strategy:', points)

def main(input_file):
    try:
        with open(input_file) as f:
            lines = f.read().splitlines()
            first_strategy(lines)
            second_strategy(lines)

    except OSError as err:
        print('Error while opening file:', err)
    except ValueError as err:
        print('Error while parsing file:', err)

if __name__ == '__main__':
    default_file = '2/input.txt'
    if len(sys.argv) != 2:
        print('Using default file')
    else:
        default_file = sys.argv[1]
    main(default_file)