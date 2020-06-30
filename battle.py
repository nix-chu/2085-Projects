from army import Army

class Battle():
    def gladiatorial_combat(self, player_one:str, player_two:str) -> int:
        '''Sets up two players and creates their desired enemies. Returns the value of the victor. 
        Only uses Stack ADT formation. 
        
        0 - Draw
        1 - Player 1 wins
        2 - Player 2 wins
        :complexity: Best O(1) occurs when the __conduct_combat method returns the winner, due to one army having no fighters.
        Worst O(Army*Life), where Army represents the length of the army with the smallest number of fighters and Life 
        represents the life of each figher, and this occurs when the __conduct_combat method iterates through the entire armies.
        '''
        p1 = Army()
        p1.choose_army(str(player_one), 0)
        p2 = Army()
        p2.choose_army(str(player_two), 0)

        return self.__conduct_combat(p1,p2,0)

    def fairer_combat(self, player_one:str, player_two:str) -> int:
        '''Sets up two players and creates their desired enemies. Returns the value of the victor. 
        Only uses Queue ADT formation. 
        
        0 - Draw
        1 - Player 1 wins
        2 - Player 2 wins

        :complexity: Best O(1) occurs when the __conduct_combat method returns the winner, due to one army having no fighters.
        Worst O(Army*Life), where Army represents the length of the army with the smallest number of fighters and Life 
        represents the life of each figher, and this occurs when the __conduct_combat method iterates through the entire armies.
        '''
        p1 = Army()
        p1.choose_army(str(player_one), 1)
        p2 = Army()
        p2.choose_army(str(player_two), 1)

        return self.__conduct_combat(p1,p2,1)
    
    def __conduct_combat(self, army1:Army, army2:Army, formation:int) -> int:
        '''Conducts a battle between the two armies (depends on the formations). 

        The first fighter from both armies will fight until one dies. The survivor will return to the stack and the next fighter
        will pop out to battle. This will continue until one army runs out of fighters.
        
        Battles are conducted by the following instructions
        1. Checks the speed of either fighter. The fighter with faster speed attacks first. If identical speeds, then both fighters attack.
        2. The fighter with faster speed attacks. 
        3. The opposing fighter will defend. If defense condition is met then no damage will be inflicted.
        4. Checks if opposing fighter is still alive. 
        5. If opposing fighter is still alive, they can attack. The initial fighter will defend. 
        6. Checks if initial fighter is still alive.
        7. If both fighters are still alive, they will lose one life. Repeat until either fighter dies. 

        :complexity: Best O(1) occurs only when an army has no fighters and the method returns a number to signify the winner.
        Worst O(Army*Life), where Army represents the length of the army with the smallest number of fighters and 
        Life represents the life of each fighter, and this occurs when both armies have fighters with life. 
        :precondition: formation argument can only accept 0 or 1 as integers
        :postcondition: The army of the losing side should have no fighters leftover, therefore army.force.length = 0 
        '''
        if formation != 0 and formation != 1:
            raise Exception("Formation must either by STACK(0) or QUEUE(1)")

        # while loop to check if either army has ran out of fighters
        while not army1.force.is_empty() and not army2.force.is_empty():
            army1_fighter = None # army1_fighter will be an instance of the Fighter class for Army 1
            army2_fighter = None # army2_fighter will be an instance of the Fighter class for Army 2
            
            if formation == 0:
                # this means that battle is conducted using Stack ADT formation (self.force is an instance of ArrayStack class)
                army1_fighter = army1.force.pop() 
                army2_fighter = army2.force.pop() 
            elif formation == 1:
                # this means that battle is conducted using Queue ADT function (self.force is an instance of CircularQueue class)
                army1_fighter = army1.force.serve() 
                army2_fighter = army2.force.serve() 

            # checks if both fighters are still alive
            while army1_fighter.is_alive() and army2_fighter.is_alive():
                # checks which fighter is faster
                if army1_fighter.get_speed() > army2_fighter.get_speed():
                    # army 1 fighter is faster than army 2 fighter
                    damage = army1_fighter.attack_damage()
                    army2_fighter.defend(damage)

                    if army2_fighter.is_alive():
                        # army 2 fighter is still alive and can attack
                        damage = army2_fighter.attack_damage()
                        army1_fighter.defend(damage)
                    
                    if army1_fighter.is_alive() and army2_fighter.is_alive():
                        # if both fighters are still alive, both will lose one life.
                        army1_fighter.lose_life(1)
                        army2_fighter.lose_life(1)
                elif army2_fighter.get_speed() > army1_fighter.get_speed():
                    # army 2 fighter is faster than army 1 fighter
                    damage = army2_fighter.attack_damage()
                    army1_fighter.defend(damage)

                    if army1_fighter.is_alive():
                        # army 2 fighter is still alive and can attack
                        damage = army1_fighter.attack_damage()
                        army2_fighter.defend(damage)
                    
                    if army1_fighter.is_alive() and army2_fighter.is_alive():
                        # if both fighters are still alive, both will lose one life.
                        army1_fighter.lose_life(1)
                        army2_fighter.lose_life(1)
                else:
                    # both fighters have the same speed and fight at the same time
                    damage = army1_fighter.attack_damage()
                    army2_fighter.defend(damage)

                    damage = army2_fighter.attack_damage()
                    army1_fighter.defend(damage)
                    
                    if army1_fighter.is_alive() and army2_fighter.is_alive():
                        # if both fighters are still alive, both will lose one life.
                        army1_fighter.lose_life(1)
                        army2_fighter.lose_life(1)
                
            # Post condition check if both fighters are still alive, if TRUE then code is broken
            if army1_fighter.is_alive() and army2_fighter.is_alive():
                raise Exception("ERROR: both fighters are still alive and therefore this script is broken")

            # checks which fighter is still alive, surviving fighter earns experience and pops them back into their army stack
            if formation == 0:
                # Stack ADT formation
                if army1_fighter.is_alive():
                    army1_fighter.gain_experience(1)
                    army1.force.push(army1_fighter)
                elif army2_fighter.is_alive():
                    army2_fighter.gain_experience(1)
                    army2.force.push(army2_fighter)
            elif formation == 1:
                # Queue ADT formation
                if army1_fighter.is_alive():
                    army1_fighter.gain_experience(1)
                    army1.force.append(army1_fighter)
                elif army2_fighter.is_alive():
                    army2_fighter.gain_experience(1)
                    army2.force.append(army2_fighter)
            
            # end of ONE battle

        # end of all battles 
        # Post-condition check if either army still has fighters, if TRUE then code is broken
        if army1.force.length > 0 and army2.force.length > 0:
            raise Exception("ERROR: both armies still have troops and therefore this script is broken")

        if army1.force.is_empty() and army2.force.is_empty():
            # Both armies have no more troops, it is a draw
            return 0 
        elif army1.force.is_empty():
            # Army 1 has no more troops, therefore Army 2 wins!
            return 2
        elif army2.force.is_empty():
            # Army 2 has no more troops, therefore Army 1 wins!
            return 1

# manual tests
if __name__ == '__main__':
    the_battle = Battle()
    print(the_battle.gladiatorial_combat("North Korea","USA"))
    # print(the_battle.fairer_combat("China", "USA"))