import random


def main():

    while True:

        domino_set = []

        for i in range(7):
            for j in range(i, 7):
                domino_set.append([i, j])

        random.shuffle(domino_set)
        stock_pieces = domino_set[:14]
        computer_pieces = domino_set[14:21]
        player_pieces = domino_set[21:28]

        # Find the highest double for both players
        comp_highest = get_highest_double(computer_pieces)
        player_highest = get_highest_double(player_pieces)

        if not comp_highest and not player_highest:
            continue

        if comp_highest and player_highest:
            if comp_highest > player_highest:
                starting_peace = comp_highest
                computer_pieces.remove(starting_peace)
                player_starts = True
            else:
                starting_peace = player_highest
                player_pieces.remove(starting_peace)
                player_starts = False
        elif comp_highest:
            starting_peace = comp_highest
            computer_pieces.remove(starting_peace)
            player_starts = True
        else:
            starting_peace = player_highest
            player_pieces.remove(starting_peace)
            player_starts = False

        break

    domino_snake = [starting_peace]

    while True:
        print("======================================================================")
        print(f"Stock size: {len(stock_pieces)}")
        print(f"Computer pieces: {len(computer_pieces)}")
        print()

        if len(domino_snake) > 6:
            first_three = "".join(str(p) for p in domino_snake[:3])
            last_three = "".join(str(p) for p in domino_snake[-3:])
            snake_str = f"{first_three}...{last_three}"
        else:
            snake_str = "".join(str(p) for p in domino_snake)
        print(snake_str)

        print()
        print("Your pieces:")
        count = 1
        for piece in player_pieces:
            print(f"{count}:{piece}")
            count += 1

        print()

        # Check for game end conditions
        if len(player_pieces) == 0:
            print("Status: The game is over. You won!")
            break
        elif len(computer_pieces) == 0:
            print("Status: The game is over. The computer won!")
            break

        # 1. Standard Draw: Both snake ends match and that number appears 8 times in snake
        elif domino_snake[0][0] == domino_snake[-1][-1]:
            val = domino_snake[0][0]
            count_val = sum(piece.count(val) for piece in domino_snake)
            if count_val == 8:
                print("Status: The game is over. It's a draw!")
                break

        # 2. Blocked Game Draw: Stock is empty and neither player can make a legal move
        if len(stock_pieces) == 0:
            left_end = domino_snake[0][0]
            right_end = domino_snake[-1][-1]

            player_can_move = any(
                p[0] == left_end or p[1] == left_end or p[0] == right_end or p[1] == right_end
                for p in player_pieces
            )
            comp_can_move = any(
                p[0] == left_end or p[1] == left_end or p[0] == right_end or p[1] == right_end
                for p in computer_pieces
            )

            if not player_can_move and not comp_can_move:
                print("Status: The game is over. It's a draw!")
                break

        if player_starts:
            print("Status: It's your turn to make a move. Enter your command.")
            while True:
                try:
                    move = int(input())
                    if -len(player_pieces) <= move <= len(player_pieces):
                        break
                    else:
                        print("Invalid input. Please try again.")
                except ValueError:
                    print("Invalid input. Please try again.")



            if move < 0:
                index = abs(move) - 1
                domino = player_pieces[index]
                left_end = domino_snake[0][0]
                if domino[1] == left_end:
                    domino_snake.insert(0, player_pieces.pop(index))
                elif domino[0] == left_end:
                    player_pieces.pop(index)
                    domino_snake.insert(0, [domino[1], domino[0]])
                else:
                    print("Illegal move. Please try again.")
                    continue
            elif move == 0:
                if len(stock_pieces) != 0:
                    player_pieces.append(stock_pieces.pop())
            else:
                index = move -1
                domino = player_pieces[index]
                right_end = domino_snake[-1][-1]
                if domino[0] == right_end:
                    domino_snake.append(player_pieces.pop(index))
                    domino_snake.append(domino)
                elif domino[1] == right_end:
                    player_pieces.pop(index)
                    domino_snake.append([domino[1], domino[0]])
                else:
                    print("Illegal move. Please try again.")
                    continue

            player_starts = False


        else:
            print("Status: Computer is about to make a move. Press Enter to continue...")
            input()
            calculate_score(computer_pieces, domino_snake, stock_pieces)

            player_starts = True





def get_highest_double(dominoes):
    doubles = [piece for piece in dominoes if piece[0] == piece[1]]
    return max(doubles) if doubles else None

def calculate_score(computer_pieces, domino_snake, stock_pieces):
    all_pieces = computer_pieces + domino_snake

    number_scores = {i: 0 for i in range(7)}

    for piece in all_pieces:
        for num in piece:
            number_scores[num] += 1

    scored_pieces = []
    for piece in computer_pieces:
        score = number_scores[piece[0]] + number_scores[piece[1]]
        scored_pieces.append((score, piece))

    scored_pieces.sort(key=lambda x: x[0], reverse=True)


    left_end = domino_snake[0][0]
    right_end = domino_snake[-1][-1]

    #Find the highest scoring piece that can be player
    for score, piece in scored_pieces:
        #check right placement
        if piece[0] == right_end:
            domino_snake.append(piece)
            computer_pieces.remove(piece)
            return
        elif piece[1] == right_end:
            domino_snake.append([piece[1], piece[0]])
            computer_pieces.remove(piece)
            return

        #check left placement
        elif piece[1] == left_end:
            domino_snake.insert(0, piece)
            computer_pieces.remove(piece)
            return
        elif piece[0] == left_end:
            domino_snake.insert(0, [piece[1], piece[0]])
            computer_pieces.remove(piece)
            return

    if len(stock_pieces) != 0:
        computer_pieces.append(stock_pieces.pop())

if __name__ == '__main__':
    main()