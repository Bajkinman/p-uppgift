from random import choice, shuffle

class Board:
    def __init__(self):
        self.squares = [["." for _ in range(8)] for _ in range(8)]
        self.visited = [[False for _ in range(8)] for _ in range(8)]
        self.moveNumber = 0
        self.xpos = -1
        self.ypos = -1
        self.knightWalk = []

    def setKnightPos(self,square):
        self.xpos = square[0]
        self.ypos = square[1]
        self.knightWalk.append((self.xpos,self.ypos))
        self.squares[self.ypos][self.xpos] = "N"
        self.visited[self.ypos][self.xpos] = True

    def wipe(self):
        self.squares = [["." for _ in range(8)] for _ in range(8)]
        self.visited = [[False for _ in range(8)] for _ in range(8)]
        self.knightWalk = []
        self.moveNumber = 0

    def legalMoves(self):
        legal = [] 
        moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        for x,y in moves:
            if 0 <= self.xpos+x <= 7 and 0 <= self.ypos+y <= 7:
                legal.append((self.xpos+x,self.ypos+y))
        return legal

    def notVisitedMoves(self):
        available = []
        for x,y in self.legalMoves():
            if not self.visited[y][x]:
                available.append((x,y))
        return available
    
    def moveKnight(self,square):
        if square not in self.legalMoves():
            #print("not a legal move, try again")
            return False

        if self.visited[square[1]][square[0]]:
            #print("already visited, try again")
            return False

        self.moveNumber += 1
        self.squares[self.ypos][self.xpos] = str(self.moveNumber)
        self.xpos = square[0]
        self.ypos = square[1]
        self.squares[self.ypos][self.xpos] = "N"
        self.visited[self.ypos][self.xpos] = True
        self.knightWalk.append((self.xpos,self.ypos))
        return True

    def undoLastMove(self):
        xremove,yremove = self.knightWalk.pop()
        self.visited[yremove][xremove] = False
        self.squares[yremove][xremove] = "."
        self.xpos,self.ypos = self.knightWalk[-1]
        self.squares[self.ypos][self.xpos] = "N"
        self.moveNumber -= 1

    def printBoard(self):
        print("-"*41)
        print("|   "+"-"*33+"   |")
        for i in range(7,-1,-1):
            print(f"|{i+1}  ",end="")
            for j in range(8):
                print("|"+" "*(2-len(self.squares[i][j]))+self.squares[i][j]+" ",end="")
            print("|   |")
            print("|   "+"-"*33+"   |")
        print("|     A   B   C   D   E   F   G   H     |")
        print("-"*41)


def squareToCoords(square):
    columnMap = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7 }
    return (columnMap[square[0]],int(square[1])-1)

def coordsToSquare(square):
    reverseMap = list('abcdefgh')
    return reverseMap[square[0]]+str(square[1]+1)

def validSquareInput(square):
    if len(square) != 2 or square[0] not in list('abcdefgh') or square[1] not in ['1','2','3','4','5','6','7','8']:
        print("Invalid input square, try again")
        return False
    return True

def getStartingSquare(board):
    validInput = False
    while not validInput:
        startSquare = input("Enter the starting square of the path: ")
        validInput = validSquareInput(startSquare)
        if not validInput:
            print("Invalid  square, try again")
    board.setKnightPos(squareToCoords(startSquare))
    
def randomWalk(start): 
    # generate next move randomly by choosing uniformly from the not visited legal moves
    board = Board()
    walk = [start]

    while True:
        moveCandidates = board.notVisitedMoves()
        if len(moveCandidates) == 0:
            break
        nextmove = choice(moveCandidates)
        board.moveKnight(nextmove)
        walk.append(nextmove)
    return walk

# have to fix so that it actually checks if it's a valid knight path, it's pretty ez
def inputWalk(showValidMoves = 'n'):
    # change so that they start by specifying the starting square
    # and then the number of moves (0 <= moves <= 63)
    board = Board()
    validInput = False
    while not validInput:
        numberOfSquares = input("Enter the number of squares in your walk (or q to quit to menu): ")
        if numberOfSquares == "q":
            return
        try:
            numberOfSquares = int(numberOfSquares)
        except Exception:
            numberOfSquares = -1
           
        if 1 <= int(numberOfSquares) <= 64:
                validInput = True
        else:
            print("Invalid input, try again")
   
    getStartingSquare(board)

    # loop through to get the rest of the squares
    for squareNumber in range(2,numberOfSquares+1):
        if showValidMoves == 'y':
            print("Available squares:",*[coordsToSquare(square) for square in board.notVisitedMoves()])
        validInput = False
        while not validInput:
            nextSquare = input(f"Enter square number {squareNumber} of your walk: ")
            validInput = validSquareInput(nextSquare)
            
            validInput = board.moveKnight(squareToCoords(nextSquare))
 
    print(board.knightWalk)
    print("-"*40)
    print("Your path:")
    print(", ".join([f"{i+1}.{coordsToSquare(board.knightWalk[i])}" for i in range(numberOfSquares)]))
    board.printBoard()
    input("Enter anything to return back to the menu ")


# this algorithm is called Warnsdorff's algorithm and it's actually just a heuristic
# that often works. 
def completeWalk(start):
    board = Board()

    foundWalk = False
    while not foundWalk:
        board.wipe()
        board.setKnightPos(start)
        walk = [start]
        for i in range(63):
            moves = board.notVisitedMoves()
            if len(moves) == 0:
                break
             
            topcandidate = -1
            minimumMoves = 9
            shuffle(moves)
            # loop through moves, move knight to candidate square, check how many 
            # options it has there, store that number, then move back and proceed to next move.
            for move in moves:
                board.moveKnight(move)
                childMoves = len(board.notVisitedMoves())-1
                board.undoLastMove()
                if childMoves < minimumMoves:
                    minimumMoves = childMoves
                    topCandidate = move
            board.moveKnight(topCandidate)
            walk.append(topCandidate)

        cond = True
        
        for row in board.visited:
            if sum(row) < 8:
                cond = False
                break
        if cond:
            foundWalk = True

    return walk

#testing if a complete walk can be generated from any starting square
"""
for initx in range(8):
    for inity in range(8):
        print(initx,inity)

        knightwalk = completeWalk((initx,inity))
        #print(knightwalk)
"""