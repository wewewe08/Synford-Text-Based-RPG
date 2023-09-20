import random, string
import time, string
import colorama
from colorama import Fore
colorama.init(autoreset=True)

from MerchantStore import store_items

player_name = ""
double_bar = "═"

class Support:
    def __init__(self):
        self.heal = 5

    def TypeText(self, text, highlight, toggleName, toggleContinue, name):
        if toggleName:
            print(f"{Fore.GREEN}{name}: ", end="")
        for letter in text:
            print(f"{highlight}{letter}", end="")
            time.sleep(0.05)
        if toggleContinue:
            time.sleep(0.5)
            print("")

    def CheckValidName(self, name):
        invalid_characters = string.punctuation + " "
        for char in name:
            if char in invalid_characters:
                print(f"{Fore.CYAN}YOUR NAME INCLUDES INVALID CHARACTERS!\n")
                return False
        if len(name) < 3:
            print(f"{Fore.CYAN}YOUR NAME IS TOO SHORT!\n")
            return False
        elif len(name) > 20:
            print(f"{Fore.CYAN}YOUR NAME IS TOO LONG!\n")
            return False
        return True

    def PlayGreeting(self, player):
        global player_name
        self.TypeText("My name is ", Fore.RESET, True, False, "[SCHULTZ]")
        self.TypeText("SCHULTZ", Fore.GREEN, False, False, "[SCHULTZ]")
        self.TypeText("! I am an aspiring mage from the Western Border.", Fore.RESET, False, True, "[SCHULTZ]")
        self.TypeText("I happened to be passing by and I saw your camp had been ransacked by those fiends.", Fore.RESET, True, True, "[SCHULTZ]")
        self.TypeText("Unfortunately, this was all I could salvage.", Fore.RESET, True, False, "[SCHULTZ]")
        time.sleep(0.5)
        print("\n")
        player.UpdateInventory("dabloon(s)", 4, 0, "")
        player.UpdateInventory("RUSTY IRON SWORD", 1, 3, "weapon")
        print(f"{Fore.GREEN}SCHULTZ {Fore.RESET}handed you a {Fore.YELLOW}RUSTY IRON SWORD {Fore.RESET}and {Fore.YELLOW}4 dabloons{Fore.RESET}.\n")
        time.sleep(0.5)
        self.TypeText("What is your name?\n", Fore.RESET, True, False, "[SCHULTZ]")
        while True:
            player_name = input(f"{Fore.CYAN}ENTER YOUR NAME: {Fore.RESET}").upper()
            if self.CheckValidName(player_name):
                break
            else: continue
        time.sleep(0.5)
        self.TypeText(player_name, Fore.GREEN, True, False, "[SCHULTZ]")
        self.TypeText("... Nice to meet you!", Fore.RESET, False, True, "[SCHULTZ]")
        return player_name

    def HealPlayer(self, health, max_health):
        heal_player = random.randint(0, 100)
        if heal_player <= 40:
            if health + self.heal <= max_health:
                health += self.heal
                print(f"{Fore.GREEN}SCHULTZ {Fore.RESET}casted a healing spell! You regained {Fore.GREEN}♥{self.heal}")
                print(f"You now have {Fore.GREEN}♥{health}/{max_health}")
            else:
                health_gained = (max_health - health)
                health += (max_health - health)
                print(f"{Fore.GREEN}SCHULTZ {Fore.RESET}casted a healing spell! You regained {Fore.GREEN}♥{health_gained}")
                print(f"You now have {Fore.GREEN}♥{health}/{max_health}")
        return health

    def DisplayStore(self):
        for item,value in store_items.items():
            print(f"{Fore.MAGENTA}{item} {Fore.RESET}: {value}db")

    def SpawnMerchant(self):
        print(f"{Fore.RESET}A {Fore.GREEN}TRAVELING MERCHANT {Fore.RESET}has blocked your path!\n")
        time.sleep(0.5)
        self.TypeText("New wares have been restocked!\n", Fore.RESET, True, False, "[TRAVELING MERCHANT]")
        time.sleep(0.5)
        print()
        print(f"{Fore.MAGENTA}╔{double_bar*9}╗")
        print(f"{Fore.MAGENTA}║  STORE  ║")
        print(f"{Fore.MAGENTA}╚{double_bar*9}╝")
        self.DisplayStore()

    def DisplayMerchantCommands(self):
        print(f"{Fore.CYAN}╔{double_bar*16}╗")
        print(f"{Fore.CYAN}║    COMMANDS    ║")
        print(f"{Fore.CYAN}╚{double_bar*16}╝\n")
        print(f"{Fore.CYAN}BUY : {Fore.RESET}'buy' OR 'b' [item name]\n")
        print(f"{Fore.CYAN}INFO : {Fore.RESET}'info' [item name]\n")
        print(f"{Fore.CYAN}CONTINUE : {Fore.RESET}'continue' OR 'c'\n")

    def DisplayCommands(self):
        print(f"{Fore.CYAN}╔{double_bar*16}╗")
        print(f"{Fore.CYAN}║    COMMANDS    ║")
        print(f"{Fore.CYAN}╚{double_bar*16}╝\n")
        print(f"{Fore.CYAN}EQUIP : {Fore.RESET}'equip' OR 'e' [item name]\n")
        print(f"{Fore.CYAN}UNEQUIP : {Fore.RESET}'unequip' OR 'u' [item name]\n")
        print(f"{Fore.CYAN}USE ITEM : {Fore.RESET}'use' [item name]\n")
        print(f"{Fore.CYAN}VIEW INVENTORY : {Fore.RESET}'view inventory' OR 'vi'\n")
        print(f"{Fore.CYAN}VIEW EQUIPPED : {Fore.RESET}'view equipped' OR 've'\n")
        print(f"{Fore.CYAN}VIEW STATS : {Fore.RESET}'view stats' OR 'vs'\n")
        print(f"{Fore.CYAN}ATTACK : {Fore.RESET}'attack' OR 'a'\n")
        print(f"{Fore.CYAN}ESCAPE : {Fore.RESET}'escape' OR 'esc'\n")
        print(f"{Fore.CYAN}CONTINUE : {Fore.RESET}'continue' OR 'c'\n")