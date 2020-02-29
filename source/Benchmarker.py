import cProfile, pstats, time, dis, io

def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return wrapper



class CheckRowFaster:
    runAmount = 5000000
    array = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    board1D1 = ['XX','B2','C2','D2', 'XX','B2','OO','A2', 'XX','B2','XX','D3', 'XX','B2','XX','XX']
    board1 = [['XX','B2','C2','D2'], # , 1, 6, 'C3'
              ['XX','B2','OO','A2'],
              ['XX','B2','XX','D3'],
              ['XX','B2','XX','XX']]
    board2 = [['XX','XX','C2','D2'], # , 1, 6, 'C3'
              ['XX','XX','OO','A2'],
              ['XX','XX','OO','D3'],
              ['XX','XX','OO','XX']]
    board3 = [['XX','XX','XX','D2'], # , 1, 6, 'C3'
              ['XX','XX','XX','A2'],
              ['XX','XX','XX','D3'],
              ['XX','XX','XX','D3']]
    board4 = [['XX','XX','XX','XX'], # , 1, 6, 'C3'
              ['XX','XX','XX','XX'],
              ['XX','XX','XX','XX'],
              ['XX','XX','XX','XX']]
    board5 = [['XX','XX','XX','D2'], # , 1, 6, 'C3'
              ['XX','XX','XX','A2'],
              ['XX','XX','XX','D3'],
              ['XX','XX','XX','XX']]
    board1D6 = ['XX','B2','C2','D2', 'XX','B2','OO','A2', 'XX','B2','XX','D3', 'XX','XX','XX','XX']
    board6 = [['XX','B2','C2','D2'], # , 1, 6, 'C3'
              ['XX','B2','OO','A2'],
              ['XX','B2','XX','D3'],
              ['XX','XX','XX','XX']]


    @profile
    def __init__(self):
        # for i in range(self.runAmount):
        #     self.CheckRow1(self.board6)
        for i in range(self.runAmount):
            self.CheckRow2(self.board1)
        for i in range(self.runAmount):
            self.CheckRow2(self.board6)
        # for i in range(self.runAmount):
        #     self.CheckRow3(self.board6)
        # for i in range(self.runAmount):
        #     self.CheckRow4(self.board6)
        # for i in range(self.runAmount):
        #     self.CheckRow5(self.board6)
        for i in range(self.runAmount):
            self.CheckRow1D1(self.board1D1)
        for i in range(self.runAmount):
            self.CheckRow1D1(self.board1D6)
        return


    def CheckRow1(self, board):
        for row in board:
            if all(x == row[0] for x in row):
                return True
        return False

    def CheckRow2(self, board):
        for row in board:
            if row[0] == row[1] and \
               row[0] == row[2] and \
               row[0] == row[3]:
                return True
        return False

    def CheckRow3(self, board):
        for row in board:
            first = row[0]
            if first == row[1] and \
            first == row[2] and \
            first == row[3]:
                return True
        return False

    def CheckRow4(self, board):
        for row in board:
            first = row[0]
            if all(x == first for x in row):
                return True
        return False

    def CheckRow5(self, board):
        for row in board:
            first = row[0]
            if all(x == first for x in row[1:]):
                return True
        return False

    # def CheckRow6(board):
    #     if all(x == row[0] for x in row for row in board):
    #         return True
    #     return False

    # def CheckRow7(board):
    #     if all(x == row[0] for x in row[1:] for row in board):
    #         return True
    #     return False

    def CheckRow1D1(self, board):
        for index in [0,4,8,12]:
            if board[index] == board[index+1] and \
            board[index] == board[index+2] and \
            board[index] == board[index+3]:
                return True
        return False




class CreateBoardHashFaster:
    runAmount = 100000
    lastPlay = None
    board1d1 = ['A1','D2','B3','C3','C2','A3','A4','D4','B2','B1','D3','C1','D1','A2','C4','XX']

    board1 = [['B4','B2','C2','D2'], # , 1, 6, 'C3'
              ['B5','B2','F5','F2'],
              ['C5','B2','C1','D3'],
              ['D4','B2','D1','H8']]
    board2 = [['XX','OO','XX','OO'], # , 1, 6, 'C3'
              ['XX','OO','XX','OO'],
              ['XX','OO','XX','OO'],
              ['XX','OO','XX','OO']]

    @profile
    def __init__(self):
        for i in range(self.runAmount):
            self.CreateBoardHash1D1(self.board1d1, self.lastPlay)
        for i in range(self.runAmount):
            self.CreateBoardHash1D2(self.board1d1, self.lastPlay)
        for i in range(self.runAmount):
            self.CreateBoardHash1D3(self.board1d1, self.lastPlay)
        for i in range(self.runAmount):
            self.CreateBoardHash1D4(self.board1d1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash4(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash5(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.CreateBoardHash6(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash7(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash8(self.board1, self.lastPlay)

        # for i in range(self.runAmount):
        #     self.CreateBoardHash4(self.board2, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash5(self.board2, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash6(self.board2, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash7(self.board2, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.CreateBoardHash8(self.board2, self.lastPlay)
        return


    def CreateBoardHash1D1(self, board, lastTurn):
        boardHash = str(lastTurn)
        for spot in board:
            boardHash += spot
        return boardHash

    def CreateBoardHash1D2(self, board, lastTurn):
        return str(lastTurn) + ''.join(board)

    def CreateBoardHash1D3(self, board, lastTurn):
        boardHash = str(lastTurn)
        return boardHash + ''.join(board)

    def CreateBoardHash1D4(self, board, lastTurn):
        boardHash = str(lastTurn) + ''.join(board)
        return boardHash

    def CreateBoardHash1(self, board, lastTurn):
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


    def CreateBoardHash2(self, board, lastTurn):
        boardHash = lastTurn + ':'
        for row in board:
            for col in row:
                if 'X' in col:
                    boardHash += 'X'
                elif 'O' in col:
                    boardHash += 'O'
                else:
                    boardHash += '-'
        return boardHash


    def CreateBoardHash3(self, board, lastTurn):
        boardHash = lastTurn
        for row in board:
            for col in row:
                if 'X' in col:
                    boardHash += 'X'
                elif 'O' in col:
                    boardHash += 'O'
                else:
                    boardHash += '-'
        return boardHash


    def CreateBoardHash4(self, board, lastTurn):
        boardHash = lastTurn
        boardHash += ':'
        for row in board:
            for col in row:
                boardHash += col[0]
        return boardHash


    def CreateBoardHash5(self, board, lastTurn):
        boardHash = lastTurn
        boardHash += ':'
        for row in board:
            for col in row:
                boardHash += col
        return boardHash


    def CreateBoardHash6(self, board, lastTurn):
        boardHash = str(lastTurn)
        for row in board:
            for col in row:
                boardHash += col
        return boardHash


    def CreateBoardHash7(self, board, lastTurn):
        boardHash = str(lastTurn)
        for row in board:
            boardHash += ''.join(row)
        return boardHash


    def CreateBoardHash8(self, board, lastTurn):
        boardHash = str(lastTurn)
        for row in board:
            boardHash += row[0] + row[1] + row[2] + row[3] 
        return boardHash



class FindPlayableFaster:
    runAmount = 20000000
    lastPlay = 'B4'
    board1 = [['A1','D2','B3','C3'], # , 1, 6, 'C3'
              ['C2','A3','A4','D4'],
              ['B2','B1','D3','C1'],
              ['D1','A2','C4','XX']]

    @profile
    def __init__(self):
        # for i in range(self.runAmount):
        #     self.FindPlayable1(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.FindPlayable2(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.FindPlayable3(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.FindPlayable4(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.FindPlayable5(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.FindPlayable6(self.board1, self.lastPlay)
        # for i in range(self.runAmount):
        #     self.FindPlayable7(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.FindPlayable8(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.FindPlayable9(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.FindPlayable10(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.FindPlayable11(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.FindPlayable12(self.board1, self.lastPlay)
        for i in range(self.runAmount):
            self.FindPlayable13(self.board1, self.lastPlay)



    def FindPlayable1(self, board, lastPlay):
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


    def FindPlayable2(self, board, lastPlay):
        playable = []
        try:
            let, num = lastPlay[0], lastPlay[1]
            for row in range(4):
                for col in range(4):
                    if let in board[row][col] or num in board[row][col]:
                        playable.append([row, col])
        except:
            # Only executes if it is the first move
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return playable

    def FindPlayable3(self, board, lastPlay):
        playable = []
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            for row in range(4):
                for col in range(4):
                    if let in board[row][col] or num in board[row][col]:
                        playable.append([row, col])
        except:
            # Only executes if it is the first move
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return playable

    def FindPlayable4(self, board, lastPlay):
        playable = []
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            for row in [0,1,2,3]:
                for col in [0,1,2,3]:
                    if let in board[row][col] or num in board[row][col]:
                        playable.append([row, col])
        except:
            # Only executes if it is the first move
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return playable

    def FindPlayable5(self, board, lastPlay):
        playable = []
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable.append([r, c])
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return playable

    def FindPlayable6(self, board, lastPlay):
        playable = []
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let == col[0] or num == col[1]:
                        playable.append([r, c])
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return playable

    def FindPlayable7(self, board, lastPlay):
        playable = []
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                for col in [0,1,2,3]:
                    if let in row[col] or num in row[col]:
                        playable.append([r, col])
                r += 1
        except:
            # Only executes if it is the first move
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return playable

    def FindPlayable8(self, board, lastPlay):
        i = 0
        playable = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable[i] =[r, c]
                        i += 1
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            playable = []
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return [] if i == 0 else playable

    def FindPlayable9(self, board, lastPlay):
        i = 0
        playable = [[3,3],[3,3],[3,3],[3,3],[3,3],[3,3]]
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable[i] = [r, c]
                        i += 1
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            playable = []
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return [] if i == 0 else playable

    def FindPlayable10(self, board, lastPlay):
        i = 0
        playable = [None,None,None,None,None,None]
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable[i] = [r, c]
                        i += 1
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            playable = []
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return [] if i == 0 else playable

    def FindPlayable11(self, board, lastPlay):
        i = 0
        playable = [16,16,16,16,16,16]
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable[i] = [r, c]
                        i += 1
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            playable = []
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return [] if i == 0 else playable

    def FindPlayable12(self, board, lastPlay):
        i = 0
        playable = [8,8,8,8,8,8]
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable[i] = [r, c]
                        i += 1
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            playable = []
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return [] if i == 0 else playable

    def FindPlayable13(self, board, lastPlay):
        i = 0
        playable = [32,32,32,32,32,32]
        try:
            let = lastPlay[0]
            num = lastPlay[1]
            r = 0
            for row in board:
                c = 0
                for col in row:
                    if let in col or num in col:
                        playable[i] = [r, c]
                        i += 1
                    c += 1
                r += 1
        except:
            # Only executes if it is the first move
            playable = []
            for row in range(4):
                for col in range(4):
                    if row % 3 == 0 or col % 3 == 0:
                        playable.append([row, col])
        return [] if i == 0 else playable



# dis.dis(FindPlayableFaster.FindPlayable2)
CreateBoardHashFaster()



array = [0, 1, 2, 3,
         4, 5, 6, 7,
         8, 9, 10,11,
         12,13,14,15]

# for index in range(0,15,4):
#     print(array[index:index+4])




