from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from stack import ArrayStack, T
from queue import CircularQueue

class Fighter(ABC, Generic[T]):
    def __init__(self, life:int, exp:int) -> None:
        '''Initiates a fighter's data. 

        :complexity: Best and Worst O(1) as assignment are all constant
        :precondition: life and exp arguments must be greater or equal to zero
        '''
        if life < 0 or exp < 0:
            raise Exception("Both life and experience inputs must be greater or equal to zero")

        self.life = life
        self.exp = exp
    
    def is_alive(self) -> bool:
        '''Returns boolean if alive or not'''
        return self.life > 0 
    
    def lose_life(self, lost_life:int) -> None:
        '''Decreases the life points of particular fighter
        
        :precondition: lost_life argument must be greater or equal to zero
        :complexity: Best and Worst O(1) as assignment, arithmetic and variable calls are all constant
        '''
        assert lost_life >= 0, "ERROR: life lost must be greater or equal to zero"
        self.life = self.life - lost_life 
        # this was done to utilise the lost_life argument, otherwise I would've done self.life -= 1
    
    @abstractmethod
    def gain_experience(self, exp_gain:int) -> None:
        pass
    
    def get_experience(self) -> int:
        '''Returns the experience value of particular fighter'''
        return self.exp
    
    def get_speed(self) -> int:
        '''Returns the speed of the particular cavalry'''
        return self.speed
    
    def get_cost(self) -> int:
        '''Returns the cost of cavalry, which is the same for all cavalry'''
        return self.cost
    
    def attack_damage(self) -> int:
        '''Returns the damage dealt by cavalry based on damage attribute'''
        return self.damage 

    @abstractmethod
    def defend(self) -> int:
        pass

    def __str__(self) -> str:
        return self.name + "'s life = " + str(self.life) + " and experience = " + str(self.exp)

class Soldier(Fighter[T]): 
    cost = 1

    def __init__(self) -> None:
        ''' Initialises soldier data
        
        :complexity: Best and Worst O(1) as these are all constant assignments
        '''
        Fighter.__init__(self, 3, 0)
        self.name = "Soldier"
        self.speed = 1 
        self.damage = 1
    
    def gain_experience(self, exp_gain:int) -> None:
        '''Increases soldier's experience, which will increase its speed, damage and defence
        
        :complexity: Best and Worst O(1) as assignment, arithmetic and variable calls are all constant
        :preconditions: exp_gain given by the function caller must be greater than or equal to zero
        '''
        assert exp_gain >= 0, "Experience gained must be greater or equal to zero"

        self.exp = self.exp + exp_gain
        self.speed = self.speed + exp_gain
        self.damage = self.damage + exp_gain
        # this was done to utilise the exp_gain argument, otherwise I would've done self.exp += 1
    
    def defend(self, damage: int) -> None: 
        '''Adjusts the life points of soldier after defending from an attack

        Damage will be inflicted only if attacker damage exceeds the soldier's experience

        :complexity: Best and Worst O(1) as lose_life function, comparison and variable calls are all constant
        :preconditions: damage given by the function caller must be greater than or equal to zero
        '''
        assert damage >= 0, "Damage needs to be greater or equal to zero"

        if damage > self.exp:
            # executes only when attacker's damage exceed the defender's experience
            self.lose_life(1)

class Archer(Fighter[T]): 
    cost = 2

    def __init__(self) -> None:
        '''Initialises archer data
        
        :complexity: Best and Worst O(1) as these are all constant assignments
        '''
        Fighter.__init__(self, 3, 0)
        self.name = "Archer"
        self.speed = 3
        self.damage = 1
    
    def gain_experience(self, exp_gain:int) -> None:
        '''Increases archer's experience, which will increase its damage and defence
        
        :complexity: Best and Worst O(1) as assignment, arithmetic and variable calls are all constant
        :preconditions: exp_gain given by the function caller must be greater than or equal to zero
        '''
        assert exp_gain >= 0, "Experience gained must be greater or equal to zero"

        self.exp = self.exp + exp_gain
        self.damage = self.damage + exp_gain
        # this was done to utilise the exp_gain argument, otherwise I would've done self.exp += 1
    
    def defend(self, damage: int) -> None: 
        '''Adjusts the life points of archer after defending from an attack

        Damage will always be inflicted to archers, because archers can never defend
        themselves properly.

        :complexity: Best and Worst O(1) as lose_life function, comparison and variable calls are all constant
        '''
        self.lose_life(1)

class Cavalry(Fighter[T]): 
    cost = 3

    def __init__(self) -> None:
        '''Initialises cavalry data
        
        :complexity: Best and Worst O(1) as these are all constant assignments
        '''
        Fighter.__init__(self, 4, 0)
        self.name = "Cavalry"
        self.speed = 2 
        self.damage = 1
    
    def gain_experience(self, exp_gain:int) -> None:
        '''Increases cavalry's experience, which will increase its damage and defence
        
        :complexity: Best and Worst O(1) as assignment, arithmetic and variable calls are all constant
        :preconditions: exp_gain given by the function caller must be greater than or equal to zero
        '''
        assert exp_gain >= 0, "Experience gained must be greater or equal to zero"

        self.exp = self.exp + exp_gain
        self.damage = self.damage + 2*exp_gain
        # this was done to utilise the exp_gain argument, otherwise I would've done self.exp += 1
    
    def defend(self, damage: int) -> None: 
        '''Adjusts the life points of cavalry after defending from an attack

        Damage is inflicted only if attacker damage exceeds the cavalry's experience halved

        :complexity: Best and Worst O(1) as lose_life function, comparison, arithmetic and variable calls are all constant
        :preconditions: damage given by the function caller must be greater than or equal to zero
        '''
        assert damage >= 0, "Damage needs to be greater or equal to zero"

        if damage > (self.exp/2):
            # executes only when attacker's damage exceed the defender's experience halved
            self.lose_life(1)

class Army():
    def __init__(self) -> None:
        self.name = ""
        self.force = ""
    
    def choose_army(self, name:str, formation:int) -> None:
        '''Sets player name and allows player to form army
        
        To create army, user input must be given as integers in S A C form, with spaces in between the integers.

        :complexity: Best O(sold*arch*cav) due to the __assign_army function call which has the same best complexity, 
        and the user inputs their army correctly the first time. Worst O(boolean*sold*arch*cav) where boolean is based on how 
        many times the user inputs incorrectly and due to the __assign_army function call. 
        '''

        # displays message for user
        print("\nPlayer "+name+" choose your army as S A C")
        print("where S is the number of soldiers")
        print("      A is the number of archers")
        print("      C is the number of cavalry")

        # while loop to check input is correct
        correct_input_boolean = False # initialises to start while loop
        while not correct_input_boolean:
            try:
                army_input = input("Please input as S A C: ")
                army = army_input.split() # separates input into elements of an array

                # checks if user gave three integers. if not, skips and continues while loop
                if len(army) == 3:
                    soldiers_input = int(army[0])
                    archers_input = int(army[1])
                    cavalry_input = int(army[2])
                    correct_input_boolean = self.__correct_army_given(soldiers_input, archers_input, cavalry_input)
            except ValueError:
                # if inputs were not integers, sets boolean to false and continues while loop
                print("Positive integers separated into S A C are only accepted, values given raised a ValueError")
                correct_input_boolean = False
        
        # once input is correct, function calls __assign_army
        self.__assign_army(name, soldiers_input, archers_input, cavalry_input, formation)
            
    def __correct_army_given(self, soldiers:int, archers:int, cavalry:int) -> bool:
        '''Performs two checks and returns boolean whether both checks have been passed
        
        First check: Player input for Soldiers, Archers and Cavalry must be greater or equal to zero
        Second check: Player did not spend more than the allocated budget $30

        :complexity: Best and Worst O(1) as assignments, comparison and arithmetic are all constant
        :precondition: Inputs need to be integers
        '''

        if soldiers < 0 or archers < 0 or cavalry < 0:
            # executes if one or more units is less than zero 
            print("Positive integers separated into S A C are only accepted, values given were negatives")
            return False

        # calculates costs for each type of unit and sums total
        soldier_cost = soldiers*Soldier.cost
        archer_cost = archers*Archer.cost
        cavalry_cost = cavalry*Cavalry.cost
        total_cost = soldier_cost + archer_cost + cavalry_cost

        if total_cost > 30:
            # checks if player exceed the budget
            print("Army exceeds budget")
            return False
        
        return True # if user passes both tests

    def __assign_army(self, name:str, soldier_size:int, archer_size:int, cavalry_size:int, formation:int) -> None:
        '''Creates size of army based on user's choices. 

        Formations can only be in Stack (0) or Queue (1) formations.
        Soldiers will go first, then Archers, and lastly Cavalry.

        :complexity: Best and Worst O(sold*arch*cav) as the for loops run based on the inputs made by the users, 
        and there was no early exit condition
        :preconditions: formation argument can only accept 0 or 1 as integers
        '''
        if not formation == 0 and not formation == 1:
            # precondition check
            raise Exception("Formation must either by STACK(0) or QUEUE(1)")

        total_size = soldier_size + archer_size + cavalry_size # to create size of army

        if formation == 0:
            # Formation will be in Stack ADT, follows First In Last Out 
            army = ArrayStack(total_size) 
        
            # pushes cavalry into formation
            for _ in range(cavalry_size):
                army.push(Cavalry())

            # pushes archers into formation
            for _ in range(archer_size):
                army.push(Archer())
            
            # pushes soldiers into formation
            for _ in range(soldier_size):
                army.push(Soldier())   
        elif formation == 1:
            # Formation will be in Queue ADT, follows First In First Out
            army = CircularQueue(total_size)

            # pushes soldiers into formation
            for _ in range(soldier_size):
                army.append(Soldier())
            
            # pushes archers into formation
            for _ in range(archer_size):
                army.append(Archer())

            # pushes cavalry into formation
            for _ in range(cavalry_size):
                army.append(Cavalry())

        # returns the attributes of the player and their army
        self.name = name
        self.force = army 
    
    def __str__(self) -> str:
        '''Prints the fighters in array, from top to bottom.
        
        :complexity: Best O(1) when the army has no fighters and prints an empty string. Worst O(N), where N represents the 
        number of fighters in the army, and the method runs for each fighter in the army. 
        '''
        length = len(self.force.array)
        if length > 0:
            output = str(self.force.array[length-1])
            for i in range(length-2,-1,-1):
                output += "," + str(self.force.array[i])
        else:
            output = ""
        return output
