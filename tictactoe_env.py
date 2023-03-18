# source: https://github.com/MauroLuzzatto/OpenAI-Gym-TicTacToe-Environment
import gym
import numpy as np
from tabulate import tabulate

from typing import Tuple, List


class tictactoeEnv(gym.Env):
    """
    Implementation of a TicTacToe Environment based on OpenAI Gym standards
    """

    def __init__(
        self, small: int, large: int, n_actions: int = 9, n_states: int = 8953
    ) -> None:
        """This class contains a TicTacToe environment in the OpenAI Gym format

        Args:
            small (int): Reward/punishment per move
            large (int): Reward for winning game
            n_actions (int, optional): _description_. Defaults to 9.
            n_states (int, optional): 8953  # 3**n**2 (n=3) possible combinations, legal states 8953. Defaults to 8953.
        """
        self.action_space = gym.spaces.Discrete(n_actions)
        self.observation_space = gym.spaces.Discrete(n_states)
        self.small = small
        self.large = large
        self.state = np.zeros((3, 3), dtype=int)

    def reset(self) -> np.array:
        """
        reset the board game and state

        TODO: return a info dict -> https://github.com/openai/gym
        """
        self.state = np.zeros((3, 3), dtype=int)
        return self.state.flatten()

    def step(self, action: Tuple[int, int]) -> Tuple[np.array, int, bool, dict]:
        """step function of the tictactoeEnv

        Args:
          Tuple(int, int):
            action (int): integer between 0-8, each representing a field on the board
            color (int): 1 or 2, representing the color of stones of the players

        Returns:
          self.state (np.array): state of the current board position, 0 means no stone, 1 or 2 are stones placed by the players
          reward (int): reward of the currrent step
          done (boolean): true, if the game is finished
          (dict): empty dict for futur game related information
        """
        # unpack the input Tuple into action and color
        action, color = action

        assert self.action_space.contains(
            action
        ), f"this action '{action}' is not in action_space"

        reward = self.small  # give (negative) reward for every move done
        (row, col) = self.decode_action(action)

        if self.state[row, col] == 0 or color==0:
            self.state[row, col] = color  # postion the token on the field
        else:
            raise ValueError('Invalid move: position already taken')
        done = self._is_winner(color) or self._is_draw()

        if self._is_winner(color):
            reward += self.large

        return self.state, reward, done, {}

    def _is_draw(self):
        return np.count_nonzero(self.state == 0) == 0


    def _is_winner(self, color: int) -> bool:
        """check if there is a winner

        Args:
            color (int): of the player

        Returns:
            bool: indicating if there is a winner
        """
        done = False
        boolean_matrix = self.state == color
        for ii in range(3):
            # check if three equal coins are aligned (horizontal, verical or diagonal)
            if (
                np.sum(boolean_matrix[:, ii]) == 3
                or np.sum(boolean_matrix[ii, :]) == 3
                or np.sum(
                    [boolean_matrix[0, 0], boolean_matrix[1, 1], boolean_matrix[2, 2]]
                )
                == 3
                or np.sum(
                    [boolean_matrix[0, 2], boolean_matrix[1, 1], boolean_matrix[2, 0]]
                )
                == 3
            ):
                done = True
                break
        return done

    def decode_action(self, i: int) -> List[int]:
        """decode the action integer into a colum and row value

        0 = upper left corner
        8 = lower right corner

        Args:
            i (int): action

        Returns:
            List[int, int]: a list with the [row, col] values
        """
        out = []
        out.append(i % 3)
        i = i // 3
        out.append(i)
        assert 0 <= i < 3
        return reversed(out)

    def render(self):
        """render the board

        The following charachters are used to represent the fields,
        '-' no stone, 'O' for player 0, and 'X' for player 1

        TODO: make an example
        """
        board = np.zeros((3, 3), dtype=str)
        for ii in range(3):
            for jj in range(3):
                if self.state[ii, jj] == 0:
                    board[ii, jj] = "-"
                elif self.state[ii, jj] == 1:
                    board[ii, jj] = "X"
                elif self.state[ii, jj] == 2:
                    board[ii, jj] = "O"
        board = tabulate(board, tablefmt="fancy_grid")
        return board
    
    def load_state(self, new_state):
        self.state = new_state
