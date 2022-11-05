import random
import typing

# TODO: Fix battlesnake and opponent move onto the same square
# TODO: Don't move into dead ends
# TODO: Purposefully kill other snakes?

# info is called when you create your Battlesnake on play.battlesnake.com


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Davis Stanko",
        "color": "#ff0000",
        "head": "dragon",
        "tail": "dragon",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # list of valid moves
    is_move_safe = {
        "up": True,
        "down": True,
        "left": True,
        "right": True
    }

    # don't move backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        print("Neck is left of head, don't move left")
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        print("Neck is right of head, don't move right")
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        print("Neck is below head, don't move down")
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        print("Neck is above head, don't move up")

    # don't move out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head['x'] == 0:
        is_move_safe['left'] = False
        print("Border is left of head, don't move left")
    if my_head['x'] == board_width - 1:
        is_move_safe['right'] = False
        print("Border is right of head, don't move right")
    if my_head['y'] == 0:
        is_move_safe['down'] = False
        print("Border is below head, don't move down")
    if my_head['y'] == board_height - 1:
        is_move_safe['up'] = False
        print("Border is above head, don't move up")

    # OPTIMIZE: ingnore parts behind neck
    # Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    for body_part in my_body[1:]:
        # Check if body part is to the left of head
        if body_part['x'] == my_head['x'] - 1 and body_part['y'] == my_head['y']:
            is_move_safe['left'] = False
            print("Body is left of head, don't move left")
        # Check if body part is to the right of head
        if body_part['x'] == my_head['x'] + 1 and body_part['y'] == my_head['y']:
            is_move_safe['right'] = False
            print("Body is right of head, don't move right")
        # Check if body part is below head
        if body_part['y'] == my_head['y'] - 1 and body_part['x'] == my_head['x']:
            is_move_safe['down'] = False
            print("Body is below head, don't move down")
        # Check if body part is above head
        if body_part['y'] == my_head['y'] + 1 and body_part['x'] == my_head['x']:
            is_move_safe['up'] = False
            print("Body is above head, don't move up")

    # Prevent the Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for opponent in opponents:
        for body_part in opponent['body']:
            # Check if body part is to the left of head
            if body_part['x'] == my_head['x'] - 1 and body_part['y'] == my_head['y']:
                is_move_safe['left'] = False
                print("Opponent is left of head, don't move left")
            # Check if body part is to the right of head
            if body_part['x'] == my_head['x'] + 1 and body_part['y'] == my_head['y']:
                is_move_safe['right'] = False
                print("Opponent is right of head, don't move right")
            # Check if body part is below head
            if body_part['y'] == my_head['y'] - 1 and body_part['x'] == my_head['x']:
                is_move_safe['down'] = False
                print("Opponent is below head, don't move down")
            # Check if body part is above head
            if body_part['y'] == my_head['y'] + 1 and body_part['x'] == my_head['x']:
                is_move_safe['up'] = False
                print("Opponent is above head, don't move up")

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    # If no safe moves
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # If only one option
    if len(safe_moves) == 1:
        print(f"MOVE {game_state['turn']}: {safe_moves[0]}")
        return {"move": safe_moves[0]}

    # TODO: LOGIC: better pathfinding
    # Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    # Find the closest food
    closest_food = None
    closest_food_distance = 9999
    for piece_of_food in food:
        distance = abs(my_head['x'] - piece_of_food['x']) + abs(my_head['y'] - piece_of_food['y'])
        if distance < closest_food_distance:
            closest_food = piece_of_food
            closest_food_distance = distance

    # Move towards the closest food if it's safe
    if closest_food is not None:
        if my_head['x'] < closest_food['x'] and is_move_safe['right']:
            next_move = 'right'
        elif my_head['x'] > closest_food['x'] and is_move_safe['left']:
            next_move = 'left'
        elif my_head['y'] < closest_food['y'] and is_move_safe['up']:
            next_move = 'up'
        elif my_head['y'] > closest_food['y'] and is_move_safe['down']:
            next_move = 'down'
    else:
        # Random move
        next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end
    })
