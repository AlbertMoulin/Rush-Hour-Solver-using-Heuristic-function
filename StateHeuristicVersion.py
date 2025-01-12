from RushHour import RushHour
from collections import deque
from typing import Callable
import copy
import heapq

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

    def __lt__(self, value):
        return True

    
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
        return count

    def printSolutionAux(s : "State", count : int):
        # print(s)
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
            # print(f'Moving the car number {s.c+1} to the {str}')
            count = State.printSolutionAux(s.prev, count+1)
            return count
        return count


    def Solve(s: "State", h: Callable[["State"], float]):
        D = {}
        D[s] = 0
        Pile = []
        heapq.heappush(Pile, (h(s), s))
        t = 0
        while Pile:
            t +=1
            _, si = heapq.heappop(Pile)
            if si.success():
                return (si,t)
            for k in si.move():
                new_cost = D[si] + 1
                if k not in D or new_cost < D[k]:
                    D[k] = new_cost
                    priority = new_cost + h(k)
                    heapq.heappush(Pile, (priority, k))
        return "Solution Not Found"
    
    def heurstic_cons(s : "State") -> float:
        return 0
    
    def heuristicBlockingCars(s: "State") -> float:
        tab = s.TabRepresente()
        count = 0
        for k in range(s.plateau.size):
            if tab[s.plateau.moveOn[0]-1][k] == 1:
                count = 0
            if tab[s.plateau.moveOn[0]-1][k] >1:
                count += 1
        return count


if __name__ == "__main__":


    # s40 = State('ExRushHour/GameP40.txt')
    # ssolve40 = State.Solve(s40, State.heurstic_cons)
    # # ssolve40.printSolution()

    # with open('heuristic_results.txt','w') as f:
    #     for i in range(1,41):
    #         print(i)

    #         s1 = State('ExRushHour/GameP' + str(i).zfill(2) + '.txt')
            
    #         _, rescons = State.Solve(s1, State.heurstic_cons)
    #         f.write(f'GameP{str(i).zfill(2)} - heuristic_cons result: {rescons}\n')
    #         _, resBloc = State.Solve(s1, State.heuristicBlockingCars)
    #         f.write(f'GameP{str(i).zfill(2)} - heuristicBlockingCars result: {resBloc}\n')
            

    # # Test heuristicBlockingCars function
    # test_state = State('ExRushHour/GameP40.txt')
    # blocking_cars = test_state.heuristicBlockingCars()
    # print(test_state)
    # print(f'Blocking cars heuristic for GameP40: {blocking_cars}')
    
    # Additional tests
    # test_state_1 = State('ExRushHour/GameP01.txt')
    # blocking_cars_1 = test_state_1.heuristicBlockingCars()
    # print(test_state_1)
    # print(f'Blocking cars heuristic for GameP01: {blocking_cars_1}')
    
    # test_state_2 = State('ExRushHour/GameP02.txt')
    # blocking_cars_2 = test_state_2.heuristicBlockingCars()
    # print(test_state_2)
    # print(f'Blocking cars heuristic for GameP02: {blocking_cars_2}')
    
    # test_state_3 = State('ExRushHour/GameP03.txt')
    # blocking_cars_3 = test_state_3.heuristicBlockingCars()
    # print(test_state_3)
    # print(f'Blocking cars heuristic for GameP03: {blocking_cars_3}')

    # Test Solve function for evey game and number of steps of the function
    for i in range(1,41):
        print(i)
        s1 = State('ExRushHour/GameP' + str(i).zfill(2) + '.txt')
        _1, rescons = State.Solve(s1, State.heurstic_cons)
        print(f'GameP{str(i).zfill(2)} - heuristic_cons result: {rescons}')
        count1 = _1.printSolution()
        _2, resBloc = State.Solve(s1, State.heuristicBlockingCars)
        print(f'GameP{str(i).zfill(2)} - heuristicBlockingCars result: {resBloc}')
        count2 = _2.printSolution()
        # raise error if number of steps is not the same
        assert count1 == count2


