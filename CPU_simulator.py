import random

class Memory:
    def __init__(self):
        self.memory_store = [0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, 0, 0, 0, 0, 0, 0,
                               ]
        self.memory_no = 0
        
    def to_add(self, num, location):
        self.memory_store[location] = num
        return
    def add_in_order(self, num):
        self.memory_store[self.memory_no] = num
        self.memory_no += 1


class CPU:
    def __init__(self):
        self.cache = {0 : None,
                    1 : None,
                    2 : None,
                    3 : None}
        self.instruction_list = {"ADD" : 0, "ADDI": 1, "SUB": 2, 
                                 "SLT": 3, "BNE": 4, "J": 5, 
                                 "JAL": 6, "LW": 7, "SW": 8,
                                 "CACHE": 9, "HALT": 10}
        self.memory_storage = Memory()
        self.cache_no = 0
        self.saved_link = None
                
    def take_instr(self, inp):
        if inp != None:
            split_instru = inp.split(" ")
            if len(split_instru) == 4:
                x = split_instru[0]
                y = int(split_instru[1])
                z = int(split_instru[2])
                w = int(split_instru[3])
                self.read_instru(x, y, z, w)
            elif len(split_instru) == 3:
                x = split_instru[0]
                y = int(split_instru[1])
                z = int(split_instru[2])
                self.read_instru(x, y, z)
            elif len(split_instru) == 2:
                x = split_instru[0]
                y = split_instru[1]
                if "(" in y:
                    y_split = y.split("(")
                    z = int(y_split[0])
                    split_2 = y_split[1]
                    w = int(split_2[:-1])
                    self.read_instru(x, z, w)
                else:
                    self.read_instru(x, y)
        else:
            print("Unable to process")
            
    def read_instru(self, x, y, z = None, w = None):
        outp = None
        if x in self.instruction_list:
            outp = self.instruction_list[x]
        if outp != None:
            if z != None and w != None:
                self.execute_instr(outp, y, z, w)
            elif z != None:
                self.execute_instr(outp, y, z)
            else: 
                self.execute_instr(outp, y)
        else:
            return outp
    
    def store_in_cache(self, location, num):
        self.cache[location] = num
    
    def store_in_memory(self, location, num):
        self.memory_storage.memory_store[location] = num
        
    def add_to_cache(self, num):
        self.cache[self.cache_no] = num
        self.cache_no += 1
        
    def execute_instr(self, outp, y, z = None, w = None):
        if outp == 0:
            if z == None or w == None:
                print("Unable to process")
                return
            x = self.memory_storage.memory_store[z] + self.memory_storage.memory_store[w] 
            print(f"{x} has been added to memory storage address: {y}")
            self.memory_storage.to_add(x, y)
        elif outp == 1:
            if z == None or w == None:
                print("Unable to process")
                return
            x = self.memory_storage.memory_store[z] + w
            print(f"{x} has been added to memory storage address: {y}")
            self.memory_storage.to_add(x, y)
        elif outp == 2:
            if z == None or w == None:
                print("Unable to process")
                return
            x = self.memory_storage.memory_store[z] - self.memory_storage.memory_store[w] 
            print(f"{x} has been added to memory storage address: {y}")
            self.memory_storage.to_add(x, y)
        elif outp == 3:
            if z == None or w == None:
                print("Unable to process")
                return
            if self.memory_storage.memory_store[z] < self.memory_storage.memory_store[w]:
                x = 1
                print(f"{self.memory_storage.memory_store[z]} is less then {self.memory_storage.memory_store[w]}")
            else:
                x = 0
                print(f"{self.memory_storage.memory_store[z]} is not less then {self.memory_storage.memory_store[w]}")
            print(f"{x} has been added to memory storage address: {y}")
            self.memory_storage.to_add(x, y)
        elif outp == 4:
            if z == None or w == None:
                print("Unable to process")
                return
            if self.memory_storage.memory_store[z] == self.memory_storage.memory_store[w]:
                x = 1
                print(f"Memory register:{z} is equal to memory register:{w}")
            else:
                x = 0
                print(f"Memory register: {z} is not equal to memory register: {w}")
            print(f"{x} has been added to memory storage address: {y}")
            self.memory_storage.to_add(x, y)
        elif outp == 5:
            print(f"{self.memory_storage.memory_store[int(y)]} is stored at memory register: {y}")
        elif outp == 6:
            self.saved_link = self.memory_storage.memory_store[y]
        elif outp == 7:
            if z == None:
                print("Unable to process")
                return
            if y  > 32:
                print("Unable to process, number outside of memory registery")
                return
            if z > 3:
                print("Unable to process, number outside of cache registery")
                return
            self.store_in_cache(z, self.memory_storage.memory_store[y])
            print(f"Adding {self.memory_storage.memory_store[y]} at memory register: {z} ")
        elif outp == 8:
            if z == None:
                print("Unable to process")
                return
            if y > 3:
                print("Unable to process, number outside of cache registery")
                return
            if z> 32:
                print("Unable to process, number outside of memory registery")
                return
            if self.cache[y] == None:
                print("No value to load to memory")
                return
            self.store_in_memory(y, self.cache[z])
            print(f"Adding {self.cache[z]} at memory register: {y} ")
        elif outp == 9:
            if x != 2:
                print("Unable to process")
            else:
                print("Flushing cache")
                self.cache = {0 : None,
                    1 : None,
                    2 : None,
                    3 : None}
        elif outp == 10:
            print("Termination Executed")
            exit()
        else:
            print("Unable to process")
            return

def welcome():
    print("""
          Welcome to my Basic MIPS instruction reader.\n
        """)  
    x = input("Press enter to initialise...\n")  
    cpusim = CPU()
    for i in range(len(cpusim.memory_storage.memory_store)):
        cpusim.memory_storage.memory_store[i] = random.randint(0, 20)
    for j in range(len(cpusim.cache)):
        cpusim.cache[j] = random.randint(0,20)
    print("""
          Please see below instructions and enter accordingly:
            Instruction	    Operand	            Meaning
            ADD	            Rd, Rs, Rt	        Rd <- Rs + Rt;
            ADDI	        Rt, Rs, immd	    Rt <- Rs + immd
            SUB	            Rd, Rs, Rt	        Rd <- Rs - Rt
            SLT	            Rd, Rs, Rt	        If (Rs < Rt) then Rd <- 1 else Rd <- 0
            BNE	            Rs, Rt, offset	    If (Rs not equal Rt) then PC <- (PC + 4) + offset * 4
            J	            target	            PC <- target * 4
            JAL	            target	            R7 <- PC + 4; PC <- target *4
            LW	            Rt, offset(Rs)	    Rt <- MEM[Rs + offset]
            SW	            Rt, offset(Rs)	    MEM[Rs + offset] <- Rt
            CACHE	        Code	            Code = 2(Flush cache)
            HALT	        ;	                Terminate Execution
          """)
    oper = input("Enter command... \n").upper()
    cpusim.take_instr(oper)


if __name__ == "__main__":
    welcome()         
