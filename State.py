from RushHour import RushHour
from collections import deque
import copy

class State:
    plateau : RushHour
    pos : list[int]
    c : int
    d : int 
    prev : "State"

    def __init__(self, path : str):
        self.plateau = RushHour(path)
        self.pos = [0]*self.plateau.nbCars
        with open(path,'r') as file:
            lines = file.readlines()
        for k in range(self.plateau.nbCars):
            lineCarK = lines[2+k].split()
            if self.plateau.horizontal[k]:
                self.pos[k] = int(lineCarK[3])
            else:
                self.pos[k] = int(lineCarK[4])
        self.TabRepresente()

    
    def TabRepresente(self) -> list[list[int]]:
        tab = [[0 for k in range(self.plateau.size)] for k in range(self.plateau.size)]
        for i in range(self.plateau.nbCars):
            for j in range(self.plateau.len[i]):
                if self.plateau.horizontal[i]:
                    if self.pos[i]+j-1 < 0 :
                        raise ValueError('Cars outside the board')
                    if tab[self.plateau.moveOn[i]-1][self.pos[i]+j-1] != 0:
                        raise ValueError('Overlapping cars')
                    tab[self.plateau.moveOn[i]-1][self.pos[i]+j-1] = i+1
                else:
                    if self.pos[i]+j-1 < 0 :
                        raise ValueError('Cars outside the board')
                    if tab[self.pos[i]+j-1][self.plateau.moveOn[i]-1] != 0:
                        raise ValueError('Overlapping cars')
                    tab[self.pos[i]+j-1][self.plateau.moveOn[i]-1] = i+1
        return tab


    def __repr__(self):
        tab = self.TabRepresente()
        tabstr = []
        for i in range(self.plateau.size):
            s = []
            for j in range(self.plateau.size):
                s.append(str(tab[i][j]))
            tabstr.append(" ".join(s))
        return "\n" + "\n".join(tabstr) + "\n"
    

    def NewState(s : "State", c : int, d : int) -> "State":
        snv = copy.copy(s)
        snv.pos = snv.pos.copy()
        snv.pos[c] += d
        snv.prev = s
        snv.c = c
        snv.d = d
        snv.TabRepresente()
        return snv
    
    def success(self) -> bool:
        return self.pos[0] + self.plateau.len[0]-1 == self.plateau.size
    
    def __eq__(self, value):
        if not isinstance(value, State ):
            raise TypeError(f"State compared to {type(value)}")
        return self.__repr__() == value.__repr__()

    def __hash__(self):
        return self.__repr__().__hash__()

    def move(s : "State") -> deque["State"]:
        dqstate = deque()
        tab = s.TabRepresente()
        for i in range(s.plateau.nbCars):
            if s.plateau.horizontal[i]:
                if s.pos[i]+s.plateau.len[i]-1< s.plateau.size and tab[s.plateau.moveOn[i]-1][s.pos[i]+s.plateau.len[i]-1] == 0:
                    dqstate.append(State.NewState(s,i,+1))
                if s.pos[i]-2 >= 0 and tab[s.plateau.moveOn[i]-1][s.pos[i]-2] == 0:
                    dqstate.append(State.NewState(s,i,-1))
            else:
                if s.pos[i]+s.plateau.len[i]-1< s.plateau.size and tab[s.pos[i]+s.plateau.len[i]-1][s.plateau.moveOn[i]-1] == 0:
                    dqstate.append(State.NewState(s,i,+1))
                if s.pos[i]-2 >= 0 and tab[s.pos[i]-2][s.plateau.moveOn[i]-1] == 0:
                    dqstate.append(State.NewState(s,i,-1))

        return dqstate

    def printSolution(s : "State"):
        count = 0
        count = State.printSolutionAux(s, count)
        print(f'Using {count} steps')

    def printSolutionAux(s : "State", count : int):
        print(s)
        if hasattr(s,"prev"):
            if s.plateau.horizontal[s.c]:
                if s.d == 1:
                    str = "right"
                else:
                    str = "left"
            else:
                if s.d == 1:
                    str = "bottom"
                else:
                    str = "top"
            print(f'Moving the car number {s.c+1} to the {str}')
            count = State.printSolutionAux(s.prev, count+1)
            return count
        return count


    def Solve(s : "State"):
        D = {}
        D[s] = 0
        Pile = deque()
        Pile.append(s)
        t = 0
        while Pile:
            t += 1
            si : State = Pile.popleft()
            for k in si.move():
                if k not in D:
                    if k.success():
                        return (k,t)
                    D[k] = D[si]+1
                    Pile.append(k)
                    
        return "Solution Not Found"


if __name__ == "__main__":
    # s40 = State('ExRushHour/GameP40.txt')
    # ssolve40 = State.Solve(s40)
    # ssolve40.printSolution()
    # for i in range(1,41):
    #     if i < 10:
    #         s1 = State('ExRushHour/GameP0' + str(i) + '.txt')
    #     else:
    #         s1 = State('ExRushHour/GameP' + str(i) + '.txt')
    #     ssolve = State.Solve(s1)
    #     State.printSolution(ssolve)
    with open('NONheuristic_results.txt','w') as f:
        for i in range(1,41):
            if i < 10:
                s1 = State('ExRushHour/GameP0' + str(i) + '.txt')
            else:
                s1 = State('ExRushHour/GameP' + str(i) + '.txt')
            _, res = State.Solve(s1)
            f.write(f'GameP{str(i).zfill(2)} -  result: {res}\n')