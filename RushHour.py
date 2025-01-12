class RushHour:
    size : int
    nbCars : int
    horizontal : list[bool]
    len : list[int]
    moveOn : list[int]

    def __init__(self, path : str):
        with open(path,'r') as file:
            lines = file.readlines()
        self.size = int(lines[0])
        self.nbCars = int(lines[1])
        self.horizontal = [False]*self.nbCars
        self.len = [0]*self.nbCars
        self.moveOn = [0]*self.nbCars
        for k in range(self.nbCars):
            lineCarK = lines[2+k].split()
            self.horizontal[k] = lineCarK[1] == "h"
            self.len[k] = int(lineCarK[2])
            if self.horizontal[k]:
                self.moveOn[k] = int(lineCarK[4])
            else:
                self.moveOn[k] = int(lineCarK[3])


if __name__ == "__main__":
    RH1 = RushHour('ExRushHour/GameP01.txt')
    print(RH1.horizontal)