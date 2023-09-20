import os, time, string
import colorama
from colorama import Fore, Back
colorama.init(autoreset=True)
from pynput.keyboard import Key, Listener

from Server import *
from Player import *
from Enemy import *
from EnemyList import *

server = Server("MISTWOOD GROVE")

double_bar = "═"
option_num = 1

build = "0.4 [INCOMPLETE]"

class Terminal:
    def __init__(self):
        pass

    def ClearTerminal(self):
        os.system("cls")

    def CheckMenuInput(self, key):
        global option_num
        if key == Key.down:
            option_num += 1
            if option_num > 3:
                option_num = 3
            self.ChangeMenuSelection(option_num)
        elif key == Key.up:
            option_num -= 1
            if option_num < 1:
                option_num = 1
            self.ChangeMenuSelection(option_num)
        elif key == Key.enter:
            return False

    def CheckAdminInput(self, key):
        global option_num
        if key == Key.down:
            option_num += 1
            if option_num > 3:
                option_num = 3
            self.ChangeAdminSelection(option_num)
        elif key == Key.up:
            option_num -= 1
            if option_num < 1:
                option_num = 1
            self.ChangeAdminSelection(option_num)
        elif key == Key.enter:
            return False

    def ChangeMenuSelection(self, option):
        self.ClearTerminal()
        print(f"{Fore.CYAN}╔{double_bar*15}╗")
        print(f"{Fore.CYAN}║    SYNFORD    ║")
        print(f"{Fore.CYAN}╚{double_bar*15}╝")
        print(f"{Fore.RESET}(version {build})")
        print("(use up and down arrow keys to navigate, enter key to select)")
        print("(admin panel is still a wip)\n")
        if option == 1:
            print(f"{Fore.CYAN}{Back.WHITE}| PLAY NORMALLY |")
            print(f"{Fore.CYAN}| PLAY WITH ADMIN PANEL |")
            print(f"{Fore.CYAN}| QUIT |")
        elif option == 2:
            print(f"{Fore.CYAN}| PLAY NORMALLY |")
            print(f"{Fore.CYAN}{Back.WHITE}| PLAY WITH ADMIN PANEL |")
            print(f"{Fore.CYAN}| QUIT |")
        elif option == 3:
            print(f"{Fore.CYAN}| PLAY NORMALLY |")
            print(f"{Fore.CYAN}| PLAY WITH ADMIN PANEL |")
            print(f"{Fore.CYAN}{Back.WHITE}| QUIT |")

    def ChangeAdminSelection(self, option):
        self.ClearTerminal()
        print(f"{Fore.CYAN}╔{double_bar*19}╗")
        print(f"{Fore.CYAN}║    ADMIN PANEL    ║")
        print(f"{Fore.CYAN}╚{double_bar*19}╝\n")
        if option == 1:
            print(f"{Fore.CYAN}{Back.WHITE}| SPAWN ENEMY |")
            print(f"{Fore.CYAN}| CHANGE STATS |")
            print(f"{Fore.CYAN}| BACK |\n")
        elif option == 2:
            print(f"{Fore.CYAN}| SPAWN ENEMY |")
            print(f"{Fore.CYAN}{Back.WHITE}| CHANGE STATS |")
            print(f"{Fore.CYAN}| BACK |\n")
        elif option == 3:
            print(f"{Fore.CYAN}| SPAWN ENEMY |")
            print(f"{Fore.CYAN}| CHANGE STATS |")
            print(f"{Fore.CYAN}{Back.WHITE}| BACK |\n")

    def ResetPlayer(self):
        player = Player()
        current_player_health = player.health
        return player, current_player_health

    def LoadPlayer(self):
        player.name = input(f"{Fore.CYAN}ENTER YOUR NAME: {Fore.RESET}\n").upper()
        print(f"{Fore.CYAN}ENTERING AS {Fore.GREEN}{player.name}")
        time.sleep(0.5)
        while True:
            difficulty = input(f"{Fore.CYAN}ENTER 'SOLO' OR 'COOP'{Fore.RESET}\n")
            if difficulty.lower() == "solo":
                server.SetDifficulty(difficulty.lower())
                break
            elif difficulty.lower() == "coop":
                server.SetDifficulty(difficulty.lower())
                break

    def UpdateAdminPanel(self):
        global option_num
        option_num = 1
        self.ChangeAdminSelection(option_num)
        with Listener(on_press = self.CheckAdminInput) as listener:  
            listener.join()
    
    def LoadAdminPanel(self):
        self.UpdateAdminPanel()
        if option_num == 1:
            self.LoadPlayer()
            locations = EnemyList.enemy_list.keys()
            while True:
                print(f"{Fore.CYAN}TYPE THE LOCATION: ")
                location = input()
                if location.lower() in locations:
                    break
            while True:
                enemies = list(EnemyList.enemy_list[location][index].get("name") for index in range(len(EnemyList.enemy_list[location])))
                print(f"{Fore.CYAN}TYPE THE NAME OF THE ENEMY TO SPAWN: ")
                name = input()
                if name.upper() in enemies:
                    print("")
                    enemy_index = enemies.index(name.upper())
                    server.SpawnEnemy(EnemyList.enemy_list[location][enemy_index], player, player.health)
                    break
        elif option_num == 2:
            print("change stats")
        else: 
            self.LoadMenu()

    def LoadMenu(self):
        player, current_player_health = self.ResetPlayer()
        time.sleep(0.5)
        self.ChangeMenuSelection(option_num)
        with Listener(on_press = self.CheckMenuInput) as listener:  
            listener.join()
        self.ClearTerminal()
        listener.stop()
        os.system("pause")
        if option_num == 1:
            while True:
                answer = input(f"{Fore.CYAN}IS THIS YOUR FIRST TIME PLAYING? (yes/no or y/n)\n{Fore.RESET}")
                if answer.lower() == "yes" or answer.lower() == "y":
                    print("loading tutorial...")
                    time.sleep(0.5)
                    self.ClearTerminal()
                    current_player_health = server.LoadTutorial(player)
                    break
                elif answer.lower() == "no" or answer.lower() == "n":
                    player.UpdateInventory("dabloon(s)", 4, 0, "")
                    player.UpdateInventory("RUSTY IRON SWORD", 1, 3, "weapon")
                    while True:
                        name = input(f"{Fore.CYAN}ENTER YOUR NAME: {Fore.RESET}").upper()
                        if support.CheckValidName(name):
                            player.name = name
                            break
                        else: continue
                    server.ChooseDifficulty()
                    print("loading game...")
                    time.sleep(0.5)
                    self.ClearTerminal()
                    current_player_health = server.LoadSceneTwo(player)
                    break
            if current_player_health <= 0:
                os.system("pause")
                self.LoadMenu()
        elif option_num == 2:
            self.LoadAdminPanel()
        else: quit()