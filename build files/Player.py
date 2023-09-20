import time, random
import colorama
from colorama import Fore
colorama.init(autoreset=True)

double_bar = "═"
armor_types = ["head", "top", "bottom", "shoes"]

class Player:
    def __init__(self):
        self.name = ""
        self.health = 20
        self.damage = 0
        self.turn = True
        self.inventory = {}
        self.equipped = {}
        
    def ViewInventory(self):
        print(f"{Fore.YELLOW}╔{double_bar*15}╗")
        print(f"{Fore.YELLOW}║   INVENTORY   ║")
        print(f"{Fore.YELLOW}╚{double_bar*15}╝")
        for item, amount in self.inventory.items():
            print(f"{Fore.YELLOW}{item} (x{amount[0]})")
        print()
    
    def UpdateInventory(self, item, amount, stats, upgrade):
        if item in self.inventory:
            self.inventory[item][0] += amount
            if self.inventory[item][0] == 0 and item != "dabloon(s)":
                del self.inventory[item]
        else:
            self.inventory[item] = [amount, stats, upgrade]
        return self.inventory

    def EquipItem(self, item, item_name):
        equipped_items = list(self.equipped.keys())
        if item_name in equipped_items:
            print(f"{Fore.CYAN}YOU ALREADY HAVE THIS ITEM EQUIPPED!\n")
            return self.equipped
        elif item_name not in equipped_items and self.inventory.get(item_name)[2] in armor_types:
            for name in self.equipped:
                if self.equipped[name][2] == self.inventory.get(item_name)[2]:
                    print(f"{Fore.CYAN}YOU ALREADY HAVE A {self.equipped[item_name][2]} EQUIPPED!\n")
                    return self.equipped
        elif item_name not in equipped_items and self.inventory.get(item_name)[2] == "weapon":
            for name in self.equipped:
                if self.equipped[name][2] == self.inventory.get(item_name)[2]:
                    print(f"{Fore.CYAN}YOU ALREADY HAVE A WEAPON EQUIPPED!\n")
                    return self.equipped
        print(f"{Fore.CYAN}YOU EQUIPPED {Fore.YELLOW}{item_name}\n")
        self.equipped[item_name] = item
        if self.equipped[item_name][2] in armor_types:
            self.health += self.equipped[item_name][1]
        elif self.equipped[item_name][2] == "weapon":
            self.damage += self.equipped[item_name][1]
        return self.equipped
    
    def UnequipItem(self, item_name):
        if item_name not in self.equipped:
            print(f"{Fore.CYAN}YOU DO NOT HAVE THIS ITEM EQUIPPED!\n")
        else:
            print(f"{Fore.CYAN}YOU UNEQUIPPED {Fore.YELLOW}{item_name}\n")
            if self.equipped[item_name][2] in armor_types:
                self.health -= self.equipped[item_name][1]
            elif self.equipped[item_name][2] == "weapon":
                self.damage -= self.equipped[item_name][1]
            del self.equipped[item_name]
        return self.equipped

    def UseItem(self, current_health):
        if current_health + 10 > 20:
            healed_amount = 20-current_health
            current_health = 20
            print(f"{Fore.CYAN}YOU WERE HEALED FOR {Fore.GREEN}♥{healed_amount}{Fore.CYAN}!")
        elif current_health == self.health:
            print(f"{Fore.CYAN}YOU ARE ALREADY AT FULL HEALTH!!")
        else:
            current_health += 10
            print(f"{Fore.CYAN}YOU WERE HEALED FOR {Fore.GREEN}♥10{Fore.CYAN}!")
        return current_health

    def ViewEquipped(self):
        print(f"{Fore.YELLOW}╔{double_bar*16}╗")
        print(f"{Fore.YELLOW}║    EQUIPPED    ║")
        print(f"{Fore.YELLOW}╚{double_bar*16}╝")
        if self.equipped == {}:
            print(f"{Fore.YELLOW}YOU CURRENTLY DO NOT HAVE ANYTHING EQUIPPED")
        for item in self.equipped:
            print(f"{Fore.YELLOW}{item}")
        print()

    def ViewStats(self, current_health):
        print(f"{Fore.YELLOW}╔{double_bar*9}╗")
        print(f"{Fore.YELLOW}║  STATS  ║")
        print(f"{Fore.YELLOW}╚{double_bar*9}╝")
        print(f"{Fore.YELLOW}[NAME]: {Fore.RESET}{self.name}")
        print(f"{Fore.YELLOW}[HEALTH]: {Fore.RESET}♥{current_health}/{self.health}")
        print(f"{Fore.YELLOW}[DAMAGE]: {Fore.RESET}{self.damage}")
        print()

    def UpdatePlayerHealth(self, enemy, enemy_damage, player_name, current_player_health, current_difficulty, support):
        time.sleep(0.5)
        print(f"{Fore.RED}{enemy} {Fore.RESET}hit you for {enemy_damage} damage!\n")
        print(f"{Fore.GREEN}[{player_name}]\n♥{Fore.RESET} {current_player_health}/{self.health}\n")
        if current_difficulty == "coop" and current_player_health > 0:
            current_player_health = support.HealPlayer(current_player_health, self.health)
        return current_player_health
    
    def DealDamage(self, current_enemy_health):
        time.sleep(0.5)
        print(f"You dealt {self.damage} damage!\n")
        current_enemy_health -= self.damage
        return current_enemy_health