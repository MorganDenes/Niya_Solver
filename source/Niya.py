from random import randint
import time
import dis



# def profile(func):
#     def wrapper(*args, **kwargs):
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = func(*args, **kwargs)
#         s = io.StringIO()
#         sortby = 'cumulative'
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         print(s.getvalue())
#         return retval
#     return wrapper




def PrintMainMenu():
    print("\n  What do you want to do?")
    print("    Play a game : play")
    # print("Generate boards : generate")
    print("       Exit : exit")

def PrintBoard(board):
    for b in board:
        print('  ' + str(b))

def PrintPlayableBoard(board, player, lastPlay):
    print("\n    %s's turn."%('X' if player == 0 else 'O'))
    if lastPlay is not None:
        print("    Last Play: %s"%lastPlay)
    else:
        print("  Can only play on the edge")
    PrintBoard(board)
    print()
    return




# @profile
def CreateBoard():
    board = [['','','',''],
             ['','','',''],
             ['','','',''],
             ['','','','']]
    # 我是一棵樹
    # When the scorching sun arise, my leaves won't wither and die
    # I am a tree with roots by the river of the Lord
    emptySpaces = 16
    for let in ['A', 'B', 'C', 'D']:
        for num in ['1', '2', '3', '4']:
            addToHere = randint(0, emptySpaces - 1)

            here = 0
            for r in range(4):
                for c in range(4):
                    if board[r][c] == '':
                        if here == addToHere:
                            board[r][c] = let + num
                            emptySpaces -= 1
                        here += 1
    return board

# @profile
def CreateBoardHash(board, lastTurn):
    boardHash = ''
    for row in board:
        for col in row:
            if 'X' in col:
                boardHash += 'X'
            elif 'O' in col:
                boardHash += 'O'
            else:
                boardHash += '-'
    return "%s:%s"%(lastTurn, boardHash)




def CheckRow(board):
    for row in board:
        if all(x == row[0] for x in row):
            return True
    return False

def CheckCol(board):
    for col in range(4):
        for spot in range(1, 4):
            if board[0][col] != board[spot][col]:
                break
        else:
            return True
    return False

def CheckDia(board):
    for i in range(1, 4):
        if board[3][0] != board[3 - i][i]:
            break
    else:
        return True

    for i in range(1, 4):
        if board[0][0] != board[i][i]:
            break
    else:
        return True
    return False

def CheckBox(board):
    for row in range(3):
        for col in range(3):
            # for i in range(1,4):
            #     if board[row][col] != board[row + (i % 2)][col + (0 if i < 2 else 1)]:
            #         break
            # else:
            #     return True
            if board[row][col] == board[row][col + 1] and \
               board[row][col] == board[row + 1][col] and \
               board[row][col] == board[row + 1][col + 1]:
                    return True
    return False

def CheckWin(board):
    if CheckCol(board) or \
       CheckRow(board) or \
       CheckDia(board) or \
       CheckBox(board):
            return True
    return False




def FindPlayable(board, lastPlay):
    playable = []
    try:
        let, num = lastPlay[0], lastPlay[1]
        for row in range(4):
            for col in range(4):
                spot = board[row][col]
                if let == spot[0] or num == spot[1]:
                    playable.append([row, col])
    except:
        # Only executes if it is the first move
        for row in range(4):
            for col in range(4):
                if row % 3 == 0 or col % 3 == 0:
                    playable.append([row, col])
    return playable


def PlayPiece(board, player, play):
    temp = board[play[0]][play[1]]
    board[play[0]][play[1]] = playerMark[player]
    return temp

def UnplayPiece(board, play, lastPlay):
    board[play[0]][play[1]] = lastPlay


def NoPlays(board, player):
    count = 0
    for row in board:
        for col in row:
            if col == playerMark[player]:
                count += 1
    if count <= 7:
        return 1 - player
    else:
        return 2




def AddSmartScore(myScore, otherScore, player):
    myScore[player] += otherScore[player]

    # Other player can't win, 1. correct my score then 2. correct-add theirs
    if otherScore[1 - player] == 0:
        if myScore[1 - player] != 0:
            myScore[player] += myScore[1 - player]
            myScore[1 - player] = 0
        myScore[player] += otherScore[1 - player]
    elif myScore[1 - player] == 0 and myScore[player] != 0:
        myScore[player] += otherScore[1 - player]
    # If other player can win just add their score normally
    else:
        myScore[1 - player] += otherScore[1 - player]

    myScore[2] += otherScore[2]
    return




gameBoards = {}
playerMark = ["XX", "OO"]
def Solve(board, player = 0, turn = 1, lastPlay = None):
    try:
        playOptions = [0, 0, 0]
        playable = FindPlayable(board, lastPlay)
        if playable == []:
            playOptions[NoPlays(board, player)] += 1

        boardHash = ''
        for play in playable:
            lastPlayTemp = PlayPiece(board, player, play)

            boardHash = CreateBoardHash(board, lastPlayTemp)
            # if boardHash == 'D3:-----OO-O--X--XX':
            #     a = 21
            if boardHash in gameBoards:
                AddSmartScore(playOptions, gameBoards[boardHash], player)
            elif turn >= 7 and CheckWin(board):
                AddSmartScore(playOptions, [1,0,0] if player == 0 else [0,1,0], player)
            else:
                AddSmartScore(playOptions, Solve(board, (1 - player), turn + 1, lastPlayTemp), player)

            UnplayPiece(board, play, lastPlayTemp)
        gameBoards[CreateBoardHash(board, lastPlay)] = playOptions
    except Exception as ex:
        print(ex)
    return playOptions




def CreateGame():
    board = CreateBoard()
    PrintBoard(board)
    print('\nGenerating AI; please wait.')
    begin = time.time()
    Solve(board)
    end = time.time()
    print('Took %.2f seconds to generate AI.\n'%(end - begin))
    return board


def GetWinChances(board, playable, player, turn, lastPlay):
    last = []
    win = [0.0, None]
    tie = [0.0, None]
    for play in playable:
        tempPlay = PlayPiece(board, player, play)

        hash = CreateBoardHash(board, tempPlay)
        if hash in gameBoards:
            last = [play, gameBoards[hash]]
        else:
            last = [play, Solve(board, player, turn, lastPlay)]

        winChance = last[1][player] / sum(last[1])
        tieChance = last[1][2] / sum(last[1])
        print('%s:%s - %s'%(play, tempPlay, hash))
        print('Win: %.2f Tie: %.2f\n'%(winChance, tieChance))
        if winChance > win[0]:
            win = [winChance, last[0]]
        if tieChance > tie[0]:
            tie = [tieChance, last[0]]

        UnplayPiece(board, play, tempPlay)
    return win, tie, last


def PlayerChoice(board, player, turn, lastPlay):
    plays = {}
    for p in FindPlayable(board, lastPlay):
        plays[board[p[0]][p[1]]] = p
    while True:
        choice = input("Pick a play: ")
        choice = choice.upper()

        if choice in plays:
            return PlayPiece(board, player, plays[choice])
        elif 'CH' in choice:
            GetWinChances(board, FindPlayable(board, lastPlay), player, turn, lastPlay)
        elif  'RE' in choice:
            PrintPlayableBoard(board, player, lastPlay)
        elif choice in gameBoards:
            print(gameBoards[choice])
        else:
            print("Can't make that play.\n")
    return


def AIChoice(board, player, turn, lastPlay):
    # Once was painful trying
    # Now it's perfect trust
    win, tie, default = GetWinChances(board, FindPlayable(board, lastPlay), player, turn, lastPlay)
    choice = default[0]
    if win[0] > 0.0:
        choice = win[1]
    elif tie[0] > 0.0:
        choice = tie[1]
    print( 'AI picks %s'%(board[choice[0]][choice[1]]) )
    time.sleep(2)
    return PlayPiece(board, player, choice)


def PlayCheckWin(board, player, lastPlay):
    if CheckWin(board):
        return player
    if FindPlayable(board, lastPlay) == []:
        return NoPlays(board, player)
    return -1



def PlayGame(board, _player=0, _turn=1, lastPlay=None):
    playerXO = 0 if input('Do you want to be X\'s or O\'s: ').upper() == 'X' else 1
    player, turn, lastPlay = _player, _turn, lastPlay
    winCheck = -1
    while True:
        PrintPlayableBoard(board, player, lastPlay)
        if playerXO == player:
            lastPlay = PlayerChoice(board, player, turn, lastPlay)
        else:
            lastPlay = AIChoice(board, player, turn, lastPlay)

        winCheck = PlayCheckWin(board, player, lastPlay)
        if winCheck != -1:
            break
        player = 1 - player
        turn += 1
        print('\n------------------------')
    if winCheck != 2:
        print("\n%s win!!"%(playerMark[winCheck]))
    else:
        print("\nGame was a tie.")
    return 




def main():
    global gameBoards
    print("\n   Welcome to Niya!!!")
    while True:
        PrintMainMenu()
        response = input("\nDecision: ").upper()
        print()

        if 'P' in response:
            del gameBoards
            gameBoards = {}
            board = CreateGame()
            # board = [['A4','B2','C2','D2'], # , 1, 6, 'C3'
            #          ['C1','D3','OO','A2'],
            #          ['OO','A3','D4','XX'],
            #          ['C4','B4','XX','XX']]
            PlayGame(board) #, 1, 6, 'C3')
        elif response in gameBoards:
            print(gameBoards[response])
        # elif 'g' in responce:
        #     GenerateBoards()
        elif 'X' in response:
            break

    print("\nPlay again soon!!!")
    return


def SolveWrapper():
    Solve(CreateBoard())

main()
# SolveWrapper()

# dis.dis(CheckRow)
