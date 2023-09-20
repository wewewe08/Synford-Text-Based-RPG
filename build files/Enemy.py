import random, time, os
import colorama
from colorama import Fore
colorama.init(autoreset=True)

from EnemyList import *

class Enemy:
    def __init__(self, name, health, damage, dabloons_dropped, item_drops):
        self.name = name
        self.health = health
        self.damage = damage
        self.dabloons_dropped = dabloons_dropped
        self.item_drops = item_drops
                
    def RollDrops(self, enemy):
        #this is horribly formatted, but im leaving it like this for now
        if enemy == "BANISHED ASTRAL KNIGHT":
            drops_list = list(self.item_drops.keys())
            current_drop_chance = random.random()
            if current_drop_chance <= 0.15: #0.15
                return drops_list[4], self.item_drops.get(drops_list[4]) #claymore
            elif current_drop_chance <= 0.25:
                return drops_list[1], self.item_drops.get(drops_list[1]) #chestplate
            elif current_drop_chance  <= 0.35:
                return drops_list[2], self.item_drops.get(drops_list[2]) #leggings
            elif current_drop_chance <= 0.45:
                return drops_list[3], self.item_drops.get(drops_list[3]) #boots
            elif current_drop_chance <= 0.55:
                return drops_list[0], self.item_drops.get(drops_list[0]) #helmet
        elif enemy == "PLAGUE DOCTOR":
            drops_list = list(self.item_drops.keys())
            current_drop_chance = random.random()
            if current_drop_chance <= 0.05:
                return drops_list[3], self.item_drops.get(drops_list[3]) #scythe
            elif current_drop_chance  <= 0.15:
                return drops_list[2], self.item_drops.get(drops_list[2]) #dark robe
            elif current_drop_chance <= 0.35:
                return drops_list[1], self.item_drops.get(drops_list[1])#mask
            elif current_drop_chance <= 0.45:
                return drops_list[0], self.item_drops.get(drops_list[0]) #hat
        return "", ""

    def DisplayDrops(self, player):
        enemy_list = EnemyList()
        drop, stats_list = self.RollDrops(self.name)
        db1, db2 = [self.dabloons_dropped[i] for i in range(2)]
        dabloons = enemy_list.GetDabloons(db1, db2)
        print(f"{Fore.RESET}You have defeated the {Fore.RED}{self.name}{Fore.RESET}!")
        print(f"You gained {Fore.YELLOW}{dabloons} dabloon(s){Fore.RESET}!")
        if drop != "":
            amount, stats, upgrade = stats_list
            print(f"You gained {Fore.YELLOW}{drop}{Fore.RESET}!")
            player.UpdateInventory(drop, amount, stats, upgrade)
        player.UpdateInventory("dabloon(s)", dabloons, 0, "")

    def UpdateEnemyHealth(self, enemy, current_enemy_health, max_enemy_health):
        print(f"{Fore.RED}[{enemy}]")
        print(f"{Fore.RED}♥ {Fore.RESET}{current_enemy_health}/{max_enemy_health}\n")
        return current_enemy_health

    def EncounterEnemy(self, player, player_health, support, current_enemy, difficulty, in_battle):
        current_enemy_health = self.health
        enemy_list = EnemyList()
        dmg1, dmg2 = [current_enemy.get("damage")[i] for i in range(2)]
        print(f"{Fore.RESET}A(n) {Fore.RED}{self.name} {Fore.RESET}has blocked your path!\n")
        print(f"{Fore.RED}[{self.name}]")
        print(f"{Fore.RED}♥ {Fore.RESET}{current_enemy_health}/{self.health}\n")
        while True:
            if player.turn:
                print("====================")
                answer = input(f"{Fore.CYAN}*ATTACK OR ESCAPE?*\n{Fore.RESET}")
                print("====================\n")
                if answer.lower() == "attack" or answer.lower() == "a":
                    in_battle = True
                    current_enemy_health = player.DealDamage(current_enemy_health)
                    if current_enemy_health <= 0:
                        current_enemy_health = 0
                        self.UpdateEnemyHealth(self.name, current_enemy_health, self.health)
                        self.DisplayDrops(player)
                        break
                    player.turn = not player.turn
                    current_enemy_health = self.UpdateEnemyHealth(self.name, current_enemy_health, self.health)
                elif answer.lower() == "escape" and not in_battle or answer.lower() == "esc" and not in_battle:
                    print(f"{Fore.CYAN}YOU ESCAPED!\n")
                    break
                elif answer.lower() == "escape" and not in_battle or answer.lower() == "esc" and in_battle:
                    print(f"{Fore.CYAN}YOU CANNOT ESCAPE AFTER ATTACKING!\n")
            elif not player.turn:
                self.damage = enemy_list.GetDamage(dmg1, dmg2)
                player_health -= self.damage
                if player_health <= 0:
                    player_health = 0
                    player.UpdatePlayerHealth(self.name, self.damage, player.name, player_health, difficulty, support)
                    print(f"{Fore.CYAN}YOU DIED!")
                    time.sleep(1)
                    del player
                    return player_health
                player_health = player.UpdatePlayerHealth(self.name, self.damage, player.name, player_health, difficulty, support)
                player.turn = not player.turn
        return player_health
