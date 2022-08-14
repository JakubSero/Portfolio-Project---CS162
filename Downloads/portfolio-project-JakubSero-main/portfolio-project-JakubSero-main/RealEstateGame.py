# Author: Jakub Kowalski
# GitHub username: JakubSero
# Date: 5/23/2022
# Description: Simple real estate game with a moving function, buy function, and renting when a player lands on an
# owned space.

class RealEstateGame:
    """
    Starts the game and initializes a player dictionary and a space dictionary.
    No parameters for init.
    """

    def __init__(self):
        self._player_dictionary = {}
        self._spaces_dictionary = {}

    def create_spaces(self, money_given, rent_amounts):
        """
        Creates the spaces needed for the board.
        Rent amount is set as 5x the rent amount for that space.
        Money_given is an integer of money given when the player lands or passes go
        Rent_amounts is a list of rent integers
        Doesn’t return anything but does fill in the spaces dictionary
        """
        counter = 0
        self._spaces_dictionary[0] = Spaces(money_given, 99999999999999999999)
        self._spaces_dictionary[0].set_owner("NOT ALLOWED")
        for space_name in range(1, 25):
            self._spaces_dictionary[space_name] = Spaces(money_given, rent_amounts[counter])
            self._spaces_dictionary[space_name].set_purchase_price(5 * rent_amounts[counter])
            counter += 1

    def create_player(self, name, balance):
        """
        Creates the player object and fills in the player dictionary
        Name is the player name as a string
        Balance is the player’s starting balance
        """
        self._player_dictionary[name] = Player(name, balance)

    def get_player_dictionary(self):
        """
        returns the player dictionary
        """
        return self._player_dictionary

    def get_spaces_dictionary(self):
        """
        returns the spaces dictionary
        """
        return self._spaces_dictionary

    def get_player_account_balance(self, name):
        """
        returns the player account balance
        name is the player name as a string
        """
        if name in self._player_dictionary:
            return self._player_dictionary[name].get_account_balance()
        else:
            return "Player not found."

    def get_player_current_position(self, name):
        """
        returns the players current position on the board
        name is the player name as a string
        """
        if name in self._player_dictionary:
            return self._player_dictionary[name].get_position()
        else:
            return "Player not found."

    def buy_space(self, name):
        """
        This method purchases the space the player is standing on
        Name is the player name as a string
        Returns True if it can be bought and False otherwise
        """
        current_player = self._player_dictionary[name]
        current_space = self._player_dictionary[name].get_position()
        if current_player.get_account_balance() > self._spaces_dictionary[current_space].get_purchase_price() and \
                self._spaces_dictionary[current_space].get_owner() == "":
            self._spaces_dictionary[current_space].set_owner(name)
            current_player.set_player_account_balance(-self._spaces_dictionary[current_space].get_purchase_price())
            return True
        else:
            return False

    def move_player(self, name, number_of_spaces):
        """
        Moves the player a certain amount of spaces on the board.
        If the player passes go or lands on it, they receive money.
        Name is the player name as a string
        Number of spaces is an integer representing numbers on a die
        """
        current_player = self._player_dictionary[name]
        if current_player.get_account_balance() == 0:
            return
        else:
            current_space = self._player_dictionary[name].get_position()
            elements = [space for space in self._spaces_dictionary]
            if current_space == 0:
                new_space = elements[0 + number_of_spaces]
                current_player.set_player_position(new_space)
                self.check_for_renting(name)
            elif number_of_spaces + current_space > 24:
                self._player_dictionary[name].set_player_account_balance \
                    (self._spaces_dictionary[current_space].get_money_given())
                remaining_spaces = 25 - current_space
                extra_moves = number_of_spaces - remaining_spaces
                new_space = elements[extra_moves]
                current_player.set_player_position(new_space)
                self.check_for_renting(name)
            else:
                new_space = elements[current_space + number_of_spaces]
                current_player.set_player_position(new_space)
                self.check_for_renting(name)

    def check_for_renting(self, name):
        """
        Is used in the move_player method
        After a player moves, this method checks if the player has to pay any rent to the
        current owner of the space
        name is the player name as a string
        """
        current_player = self._player_dictionary[name]
        current_space = self._player_dictionary[name].get_position()
        if current_space == 0 or self._spaces_dictionary[current_space].get_owner() == "" or self._spaces_dictionary[
            current_space].get_owner() == name:
            return
        else:
            if current_player.get_account_balance() - self._spaces_dictionary[current_space].get_rent_amount() > 0:
                current_player.set_player_account_balance(-self._spaces_dictionary[current_space].get_rent_amount())

                self._player_dictionary[self._spaces_dictionary[current_space].get_owner()].set_player_account_balance \
                    (self._spaces_dictionary[current_space].get_rent_amount())
            else:
                remaining_balance = current_player.get_account_balance()
                current_player.set_player_account_balance(-remaining_balance)

                self._player_dictionary[self._spaces_dictionary[current_space].get_owner()].set_player_account_balance \
                    (remaining_balance)

                for space in self._spaces_dictionary:
                    if space == 0:
                        continue
                    if self._spaces_dictionary[space].get_owner() == name:
                        self._spaces_dictionary[space].set_owner("")

    def check_game_over(self):
        """
        Checks the bankruptcy status of each player.
        If one player remains not bankrupt, they win.
        Returns the winning player’s name, otherwise, if nobody won, returns an empty
        """
        bankrupt_count = 0
        for player in self._player_dictionary:
            if self._player_dictionary[player].get_account_balance() == 0:
                bankrupt_count += 1
        if bankrupt_count == len(self._player_dictionary) - 1:
            for player in self._player_dictionary:
                if self._player_dictionary[player].get_account_balance() != 0:
                    return self._player_dictionary[player].get_player_name()
        else:
            return ""


class Player:
    """
    Creates a player object that has a name, balance, and position on the board
    Needs to be created by the user.
    Gets added into the player dictionary in the RealEstateGame class
    """
    def __init__(self, name, balance):
        self._player_name = name
        self._player_account_balance = balance
        self._player_position = 0

    def get_player_name(self):
        """
        Returns the players name as a string
        """
        return self._player_name

    def get_account_balance(self):
        """
        Returns the account balance of the player, integer
        """
        return self._player_account_balance

    def get_position(self):
        """
        Returns the position of the player on the board, integer
        """
        return self._player_position

    def set_player_account_balance(self, balance):
        """
        Sets the player account balance to the new balance.
        Balance is the new integer value to be added to the account balance
        """
        self._player_account_balance += balance

    def set_player_position(self, space):
        """
        Sets the player position to a new position on the board
        Space is the new position and is an integer
        """
        self._player_position = space


class Spaces:
    """
    Creates a spaces object that takes money_given and rent_amounts as a parameter.
    Also initializes purchase price to 0 and the owner to an empty string.
    Gets added to the spaces dictionary in the RealEstateGame class.
    """
    def __init__(self, money_given, rent_amounts):
        self._money_given = money_given
        self._rent_amount = rent_amounts
        self._purchase_price = 0
        self._owner = ""

    def get_money_given(self):
        """
        returns the money given when passing GO on the board, integer
        """
        return self._money_given

    def get_rent_amount(self):
        """
        Returns the rent amount for the space, integer
        """
        return self._rent_amount

    def get_purchase_price(self):
        """
        Returns the purchase price for the space, integer
        """
        return self._purchase_price

    def get_owner(self):
        """
        Returns the owner of the space, string
        """
        return self._owner

    def set_purchase_price(self, amount):
        """
        Sets the purchase price of the space. This gets used when creating the space in the RealEstateGame class.
        Amount is 5x the rent amount for the space, an integer
        """
        self._purchase_price = amount

    def set_owner(self, name):
        """
        Sets the owner of the space when they buy it from the board.
        Name is the players name as a string
        """
        self._owner = name
