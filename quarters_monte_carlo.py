# This is a monte carlo simulation of the quarters game played at Christen's house. The rules:

# Every person at a round table starts with 5 quarters.
# Each turn, the current player rolls a dice for each quarter they have
# (so, each person starts with 5 dice).
# For each dice, if the dice roll comes up 4, then a quarter goes into a pot.
# If it's 5, then the player gives the quarter to the player on the left,
# If it's 6, then the quarter goes to the player on the right
# Otherwise the quarter stays with the player.
# If the player has lost all of his quarters, he is out of the game
# This continues until all but one player are out of quarters.
# The last player rolls. If their money doesn't go into the pot, they win the pot

# This code is a simulation, originally to find out what chances a player has
# depending on how big the table is, but then I realized that
# because each game is flatly distrubuted randomly, each player has an equal chance....
# Now I'm playing with the number of turns to see how it increases with respect to number
# of players and number of quarters

# I've already demonstrated the normal distribution that tends to appear
# around the number of turns as a function of number of games.
# Next is plotting avg number of turns  as number of games increases

import collections
import pickle
import random
import statistics

import matplotlib.pyplot as plt


GameStats = collections.namedtuple('GameStats', 'num_players num_starting_quarters winner num_turns')


def simulate_game(num_players=10, num_starting_quarters=5, *, debug=False):

    assert num_players >= 1
    assert num_starting_quarters >= 1

    table = [num_starting_quarters] * num_players

    current_player_index = 0
    turn_count = 0
    while len([quarter for quarter in table if quarter > 0]) > 1:

        # make sure they have something to give...
        if table[current_player_index] > 0:
            turn_count += 1

            # make sure the player never rolls more dice than
            # the the number of starting quarters
            if table[current_player_index] >= num_starting_quarters:
                current_player_dice_rolls = [random.randint(1, 6)
                                             for i in range(num_starting_quarters)]
            else:
                current_player_dice_rolls = [random.randint(1, 6)
                                             for i in range(table[current_player_index])]

            if debug:
                print('starting player:', current_player_index)
                print("turn:", turn_count)

            for current_player_dice_roll in current_player_dice_rolls:
                if debug:
                    guess_list = [0] * num_players
                    guess_list[current_player_index] = current_player_dice_roll
                    print(table)
                    print(guess_list)
                    print()
                    # input()

                if current_player_dice_roll >= 4:
                    table[current_player_index] -= 1

                    if current_player_dice_roll == 5:
                        # rotate left while wrapping
                        next_player_index = (current_player_index + num_players - 1) % num_players
                        table[next_player_index] += 1

                    elif current_player_dice_roll == 6:
                        # rotate right while wrapping
                        next_player_index = (current_player_index + 1) % num_players
                        table[next_player_index] += 1

        current_player_index = (current_player_index + 1) % num_players

    # print(table)
    # get that last non-zero player
    # TODO: implement the final roll
    for index, player in enumerate(table):
        if player:
            return GameStats(num_players, num_starting_quarters, index, turn_count)

    raise IndexError("There should have been a winner...")


def test():
    print(simulate_game(num_players=3, num_starting_quarters=3, debug=True))


def get_data(num_games=1000, num_players=10, num_starting_quarters=5):
    """return a list of GameStats for pickling or passing to immediate evaluation"""
    return [simulate_game(num_players, num_starting_quarters) for n in range(num_games)]


def write_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)


def get_data_from_file(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def plot_data(data, bins=20):
    """Plot the number of turns"""
    num_turns = [n.num_turns for n in data]
    plt.hist(num_turns, bins=bins)
    plt.title("Quarters Histogram")
    plt.xlabel("Turns")
    plt.ylabel("Frequency")
    plt.show()


def main2():
    # write_data(get_data(num_games=10000), 'data.pickle')
    plot_data(get_data_from_file('data.pickle'), bins=50)


def main3():
    num_games = 1000
    max_players = 50
    avg_num_turns_list = []
    for num_players in range(1, max_players + 1):
        filename = '{}-{:03d}.pickle'.format(num_games, num_players)
        write_data(get_data(num_games=num_games, num_players=num_players),
                   filename)
        game_stats = get_data_from_file(filename)
        avg_num_turns = statistics.mean([gs.num_turns for gs in game_stats])
        print(num_players, avg_num_turns)
        avg_num_turns_list.append(avg_num_turns)

    # plot the sonofabitch
    plt.scatter(range(1, max_players + 1), avg_num_turns_list)
    plt.show()


if __name__ == "__main__":
    main3()
    # test()
