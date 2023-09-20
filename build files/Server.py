import random
import time, os
import colorama
from colorama import Fore
colorama.init(autoreset=True)

from Support import *
from Enemy import *
from EnemyList import *
from MerchantStore import store_items

support = Support()

double_bar = "═"
current_enemy = None
current_difficulty = ""
current_player_health = 20
merchant_exists = False

class Server:
    def __init__(self, location):
        self.current_location = location

    def ClearTerminal(self):
        os.system("cls")

    def PrintLocation(self, location):
        current_location = location
        print(f"{Fore.CYAN}╔{double_bar*16}╗")
        print(f"{Fore.CYAN}║ {current_location} ║")
        print(f"{Fore.CYAN}╚{double_bar*16}╝\n")
        print(f"{Fore.CYAN}CURRENT LEVEL: \n")
    
    def SetDifficulty(self, diff):
        global current_difficulty
        current_difficulty = diff

    def CheckDifficulty(self):
        return current_difficulty

    def ChooseDifficulty(self):
        while True:
            print(f"{Fore.CYAN}| TRAVEL WITH {Fore.GREEN}SCHULTZ{Fore.CYAN}? |")
            answer = input()
            if answer.lower() == "yes" or answer.lower() == "y":
                self.SetDifficulty("coop")
                break
            elif answer.lower() == "no" or answer.lower() == "n":
                self.SetDifficulty("solo")
                print(f"You tell {Fore.GREEN}SCHULTZ {Fore.RESET}that you must do this quest on your own.")
                time.sleep(0.5)
                self.TypeText("Well...", Fore.RESET, True, True, "[SCHULTZ]")
                self.TypeText("Good luck to you, traveler!", Fore.RESET, True, True, "[SCHULTZ]")
                break
    
    def SpawnEnemy(self, enemy, player, player_health, in_battle):
        global current_player_health
        enemy_name = self.GetEnemyData(enemy, "name")
        #setting enemy stats
        max_enemy_health, damage, dabloons_dropped = self.GetEnemyData(enemy, "health"), self.GetEnemyData(enemy, "damage"), self.GetEnemyData(enemy, "dabloons dropped")
        if "item drops" in enemy.keys():
            current_drops = self.GetEnemyData(enemy, "item drops")
        else:
            current_drops = {}
        current_enemy = Enemy(enemy_name, max_enemy_health, damage, dabloons_dropped, current_drops)
        current_player_health = current_enemy.EncounterEnemy(player, player_health, support, enemy, self.CheckDifficulty(), in_battle)
    
    def GetEnemyData(self, enemy, key):
        data = enemy.get(key)
        return data

    def TypeText(self, text, highlight, toggleName, toggleContinue, name):
        if toggleName:
            print(f"{Fore.GREEN}{name}: ", end="")
        for letter in text:
            print(f"{highlight}{letter}", end="")
            time.sleep(0.05)
        if toggleContinue:
            time.sleep(0.5)
            print("")

    def LoadCommands(self, player):
        global current_player_health
        while True:
            answer = ""
            answer = input(f"{Fore.CYAN}ENTER COMMAND HERE: (TYPE 'help' OR 'h' TO VIEW A LIST OF COMMANDS){Fore.RESET}\n")
            current_item = answer.split(maxsplit=1)
            if len(current_item) == 2:
                current_item[1] = current_item[1].upper()
                equip_item = player.inventory.get(current_item[1])
                if current_item[1] in player.inventory and current_item[0].lower() == "equip" or current_item[1] in player.inventory and current_item[0].lower() == "e":
                    player.EquipItem(equip_item, current_item[1])
                elif current_item[1] in player.inventory and current_item[0].lower() == "unequip" or current_item[1] in player.inventory and current_item[0].lower() == "u":
                    player.UnequipItem(current_item[1])
                elif current_item[1] in player.inventory and current_item[0].lower() == "use":
                    if current_item[1] == "HEALING FLASK":
                        player.UpdateInventory(current_item[1], -1, 0, "")
                        current_player_health = player.UseItem(current_player_health)
                    else:
                        print(f"{Fore.CYAN}YOU CANNOT USE THIS ITEM!")
            else:
                equipped_items = player.equipped.keys()
                if answer.lower() == "view inventory" or answer.lower() == "vi":
                    player.ViewInventory()
                elif answer.lower() == "view equipped" or answer.lower() == "ve":
                    player.ViewEquipped()
                elif answer.lower() == "view stats" or answer.lower() == "vs":
                    player.ViewStats(current_player_health)
                elif answer.lower() == "help" or answer.lower() == "h":
                    self.ClearTerminal()
                    support.DisplayCommands()
                elif answer.lower() == "continue" and "weapon" not in (player.equipped.get(item)[2] for item in list(equipped_items)) or answer.lower() == "c" and "weapon" not in (player.equipped.get(item)[2] for item in list(equipped_items)):
                    while True:
                        answer = input(f"{Fore.CYAN}YOU DON'T HAVE A WEAPON EQUIPPED. ARE YOU SURE YOU WANT TO CONTINUE?\n{Fore.RESET}")
                        if answer.lower() == "yes" or answer.lower() == "y" or answer.lower() == "no" or answer.lower() == "n":
                            break
                        else: continue
                    if answer.lower() == "yes" or answer.lower() == "y":
                        self.ClearTerminal()
                        break
                elif answer.lower() == "continue" or answer.lower() == "c":
                    self.ClearTerminal()
                    break
            continue
    
    def LoadMerchantCommands(self, player):
        global merchant_exists
        while True:
            answer = ""
            answer = input(f"{Fore.CYAN}ENTER COMMAND HERE: (TYPE 'help' OR 'h' TO VIEW MERCHANT COMMANDS){Fore.RESET}\n")
            current_item = answer.split(maxsplit=1)
            if len(current_item) == 2:
                current_item[1] = current_item[1].upper()
                if current_item[0].lower() == "buy" or current_item[0].lower() == "b":
                    while True:
                        amount = input(f"{Fore.CYAN}ENTER AMOUNT TO BUY: {Fore.RESET}\n")
                        try:
                            amount = int(amount)
                            price = store_items.get(current_item[1]) * amount
                            if player.inventory.get("dabloon(s)")[0] >= price: #amount
                                player.inventory.get("dabloon(s)")[0] -= price
                                player.UpdateInventory(current_item[1], amount, 0, "")
                                player.ViewInventory()
                            else:
                                print(f"{Fore.CYAN}YOU DO NOT HAVE ENOUGH TO BUY THIS ITEM!")
                            break
                        except ValueError:
                            print(f"{Fore.CYAN}THIS IS NOT A VALID NUMBER!")
                elif current_item[0].lower() == "info":
                    print(current_item[0])
            else:
                equipped_items = player.equipped.keys()
                if answer.lower() == "help" or answer.lower() == "h":
                    support.DisplayMerchantCommands()
                elif answer.lower() == "continue" and "weapon" not in (player.equipped.get(item)[2] for item in list(equipped_items)) or answer.lower() == "c" and "weapon" not in (player.equipped.get(item)[2] for item in list(equipped_items)):
                    while True:
                        answer = input(f"{Fore.CYAN}YOU DON'T HAVE A WEAPON EQUIPPED. ARE YOU SURE YOU WANT TO CONTINUE?\n{Fore.RESET}")
                        if answer.lower() == "yes" or answer.lower() == "y" or answer.lower() == "no" or answer.lower() == "n":
                            break
                        else: continue
                    if answer.lower() == "yes" or answer.lower() == "y":
                        self.ClearTerminal()
                        break
                elif answer.lower() == "continue" or answer.lower() == "c":
                    self.ClearTerminal()
                    break
            merchant_exists = False

    def SpawnEnemies(self, player, enemy_type, in_battle):
        global merchant_exists
        enemyList= EnemyList()
        while True:
            #spawn merchant
            merchant_spawn = random.random()
            if merchant_spawn <= 0.3: #30% spawn chance
                support.SpawnMerchant()
                merchant_exists = True
            else:
                enemy = random.choice(enemyList.enemy_list[enemy_type])
                self.SpawnEnemy(enemy, player, current_player_health, in_battle)
            #everything below is for testing only
            if current_player_health <= 0:
                return current_player_health
            elif merchant_exists:
                self.LoadMerchantCommands(player)
                self.LoadCommands(player)
            else:
                self.LoadCommands(player)

    def LoadTutorial(self, player):
        global current_player_health
        print(f"{Fore.CYAN}╔{double_bar*16}╗")
        print(f"{Fore.CYAN}║    TUTORIAL    ║")
        print(f"{Fore.CYAN}╚{double_bar*16}╝\n")
        print(f"{Fore.RESET}You slowly open your eyes and see a young boy before you at the campfire.\n")
        time.sleep(0.5)
        self.TypeText("Oh, you are awake!", Fore.RESET, True, True, "[???]")
        self.TypeText("You were knocked unconscious for awhile now. Those ", Fore.RESET, True, False,"[???]")
        self.TypeText("SKELETON BANDITS", Fore.RED, False, False, "[???]")
        self.TypeText(" really did a number on you.", Fore.RESET, False, False, "[???]")
        time.sleep(0.5)
        print("\n")
        print(f"{Fore.RESET}You blankly stare at the stranger in confusion.\n")
        time.sleep(0.5)
        player.name = support.PlayGreeting(player)
        self.TypeText("We are currently in ", Fore.RESET, True, False,"[SCHULTZ]")
        self.TypeText("MISTWOOD GROVE", Fore.CYAN, False, False,"[SCHULTZ]")
        self.TypeText(". A lot of hostile creatures around here...", Fore.RESET, False, True, "[SCHULTZ]")
        self.TypeText("You should have a weapon equipped at all times.", Fore.RESET, True, True, "[SCHULTZ]")
        self.TypeText("You never know when you'll run into an enemy.", Fore.RESET, True, False, "[SCHULTZ]")
        time.sleep(0.5)
        print("\n")
        while True:
            answer = input(f"{Fore.CYAN}TO OPEN YOUR INVENTORY, TYPE 'view inventory' OR 'vi'{Fore.RESET}\n")
            if answer.lower() == "view inventory" or answer.lower() == "vi":
                player.ViewInventory()
                break
            else: continue
        while True:
            answer = input(f"{Fore.CYAN}TO VIEW YOUR EQUIPPED ITEMS, TYPE 'view equipped' OR 've'{Fore.RESET}\n")
            if answer.lower() == "view equipped" or answer.lower() == "ve":
                player.ViewEquipped()
                break
            else: continue
        while True:
            answer = input(f"{Fore.CYAN}TO EQUIP AN ITEM, TYPE 'equip' OR 'e' FOLLOWED BY THE ITEM NAME{Fore.RESET}\n").upper()
            current_item = answer.split(maxsplit=1)
            if len(current_item) == 2:
                equip_item = player.inventory.get(current_item[1])
                if current_item[1] in player.inventory and current_item[0].lower() == "equip" or current_item[1] in player.inventory and current_item[0].lower() == "e":
                    player.EquipItem(equip_item, current_item[1])
                    break
            continue
        while True:
            answer = input(f"{Fore.CYAN}TO UNEQUIP AN ITEM, TYPE 'unequip' OR 'u' FOLLOWED BY THE ITEM NAME {Fore.RESET}\n").upper()
            current_item = answer.split(maxsplit=1)
            if len(current_item) == 2:
                if current_item[1] in player.inventory and current_item[0].lower() == "unequip" or current_item[1] in player.inventory and current_item[0].lower() == "u":
                    player.UnequipItem(current_item[1])
                    break
            continue
        time.sleep(1)
        print(f"{Fore.CYAN}THE {Fore.YELLOW}RUSTY IRON SWORD {Fore.CYAN}WAS RE-EQUIPPED FOR YOU")
        player.EquipItem([1,3,"weapon"],"RUSTY IRON SWORD")
        time.sleep(0.5)
        player.ViewEquipped()
        time.sleep(1)
        print(f"{Fore.RESET}You hear a distant rustling from the bushes ahead.")
        time.sleep(0.5)
        self.TypeText("There is an enemy approaching!", Fore.RESET, True, False,"[SCHULTZ]")
        time.sleep(0.5)
        print("\n")
        enemyList= EnemyList()
        enemy = enemyList.enemy_list["mistwood grove"][1]
        self.SpawnEnemy(enemy, player, current_player_health, False)
        print(f"{Fore.CYAN}YOU OBTAINED A {Fore.YELLOW}HEALING FLASK{Fore.CYAN}!\n")
        player.UpdateInventory("HEALING FLASK", 1, 0, "")
        time.sleep(0.5)
        player.ViewInventory()
        while True:
            answer = input(f"{Fore.CYAN}TO USE ITEMS, TYPE 'use' FOLLOWED BY THE ITEM NAME.{Fore.RESET}\n").upper()
            current_item = answer.split(maxsplit=1)
            if current_item[1] in player.inventory and current_item[0].lower() == "use":
                if current_item[1] == "HEALING FLASK":
                    player.UpdateInventory(current_item[1], -1, 0, "")
                    current_player_health = player.UseItem(current_player_health)
                    break
                else:
                    print(f"{Fore.CYAN}YOU CANNOT USE THIS ITEM!")
                    continue
            elif current_item[1].lower() in player.inventory and current_item[0].lower() == "use":
                print(f"{Fore.CYAN}YOU CANNOT USE THIS ITEM!")
        while True:
            answer = input(f"{Fore.CYAN}TO VIEW YOUR STATS, TYPE 'view stats' OR 'vs'{Fore.RESET}\n")
            if answer.lower() == "view stats" or answer.lower() == "vs":
                player.ViewStats(current_player_health)
                break
        time.sleep(1)
        while True:
            answer = input(f"{Fore.CYAN}IF YOU WANT TO VIEW THE COMMANDS AGAIN, TYPE 'help' OR 'h'. TYPE 'continue' OR 'c' TO CONTINUE.'{Fore.RESET}\n")
            if answer.lower() == "help" or answer.lower() == "h":
                self.ClearTerminal()
                support.DisplayCommands()
            elif answer.lower() == "continue" or answer.lower() == "c":
                self.ClearTerminal()
                break
        time.sleep(0.5)
        print(f"You mention to {Fore.GREEN}SCHULTZ {Fore.RESET}that you are trying to find a {Fore.YELLOW}NETHER STAR{Fore.RESET}.\n")
        time.sleep(0.5)
        self.TypeText("WHAT.", Fore.RESET, True, True,"[SCHULTZ]")
        time.sleep(2)
        self.TypeText("Do you know how hard it is to get such a high-rarity item??", Fore.RESET, True, True,"[SCHULTZ]")
        self.TypeText("Nevermind that, it will take you ages to get one with your current gear.", Fore.RESET, True, True,"[SCHULTZ]")
        print("")
        time.sleep(0.5)
        print(f"You explained that you were sent on a quest to deliver a {Fore.YELLOW}NETHER STAR {Fore.RESET}to {Fore.CYAN}SYNFORD KINGDOM{Fore.RESET}.")
        time.sleep(0.5)
        print(f"{Fore.GREEN}SCHULTZ {Fore.RESET}looked at you with a confused expression for a moment and fixed his wizard hat.\n")
        time.sleep(0.5)
        self.TypeText("I can help you on your quest if you'd like.", Fore.RESET, True, True,"[SCHULTZ]")
        self.TypeText("I was heading to ", Fore.RESET, True, False,"[SCHULTZ]")
        self.TypeText("SYNFORD KINGDOM", Fore.CYAN, False, False,"[SCHULTZ]")
        self.TypeText(" myself, anyway.", Fore.RESET, False, True,"[SCHULTZ]")
        time.sleep(0.5)
        print("")
        self.ChooseDifficulty()
        time.sleep(0.5)
        self.ClearTerminal()
        current_player_health = self.LoadSceneTwo(player)
        return current_player_health

    def LoadSceneTwo(self, player):
        global current_player_health
        current_player_health = player.health
        self.PrintLocation(self.current_location)
        enemy_type = self.current_location.lower()
        in_battle = False
        if self.CheckDifficulty() == "coop":
            self.TypeText("If you're trying to get a ", Fore.RESET, True, False, "[SCHULTZ]")
            self.TypeText("NETHER STAR", Fore.YELLOW, False, False, "[SCHULTZ]")
            self.TypeText(", we should head to ", Fore.RESET, False, False, "[SCHULTZ]")
            self.TypeText("ASTRAL CEMETERY", Fore.CYAN, False, False, "[SCHULTZ]")
            self.TypeText(".", Fore.RESET, False, True, "[SCHULTZ]")
            time.sleep(0.5)
            self.TypeText("First, we need to get you some better gear.", Fore.RESET, True, True, "[SCHULTZ]")
            print("")
        self.LoadCommands(player)
        current_player_health = self.SpawnEnemies(player, enemy_type, in_battle)
        return current_player_health