import random

class EnemyList:
    def __init__(self):
        self.enemy_list = {
        "mistwood grove": [
            {
                "name": "GHOUL",
                "health": 1,
                "damage": [0,1],
                "dabloons dropped": [1,3]
            },
            {
                "name": "SKELETON BANDIT",
                "health": 5,
                "damage": [1,3],
                "dabloons dropped": [1,3]
            },
            {
                "name": "BANISHED ASTRAL KNIGHT",
                "health": 10,
                "damage": [5,8],
                "dabloons dropped": [5,10],
                "item drops": {
                    "DAMAGED ASTRAL HELMET": [1, 5, "head"],
                    "DAMAGED ASTRAL CHESTPLATE": [1, 15, "top"],
                    "DAMAGED ASTRAL LEGGINGS": [1, 10, "bottom"],
                    "DAMAGED ASTRAL BOOTS": [1, 5, "shoes"],
                    "DAMAGED ASTRAL CLAYMORE": [1, 10, "weapon"]
                }
            }
        ],
        "astral cemetery": [
            {
                "name": "ROTTEN CORPSE",
                "health": 15,
                "damage": [5,10],
                "dabloons dropped": [10,12]
            },
            {
                "name": "PLAGUE DOCTOR",
                "health": 25,
                "damage": [10,15],
                "dabloons dropped": [10,15],
                "item drops": {
                    #fix stats
                    "BLACK LEATHER HAT": 10,
                    "SUSPICIOUS-LOOKING MASK": 10,
                    "DARK ROBE": 25,
                    "SCYTHE OF THE ABYSS": 15
                }
            },
            {
                "name": "ASTRAL KNIGHT",
                "health": 35,
                "damage": [10,20],
                "dabloons dropped": [15,20],
                "item drops": {
                    "REFINED ASTRAL HELMET": 15,
                    "REFINED ASTRAL CHESTPLATE": 30,
                    "REFINED ASTRAL LEGGINGS": 20,
                    "REFINED ASTRAL BOOTS": 10,
                    "ASTRAL CLAYMORE": 25
                }
            },
            {
                "name": "WITHERED ASTRAL SKELETON",
                "health": 40,
                "damage": [15,25],
                "dabloons dropped": [20,25],
                "item drops": {
                    "WITHERED SKULL": 0
                }
            },
            {
                "name": "WENDIGO",
                "health": 65,
                "damage": [25,30],
                "dabloons dropped": [50,60],
                "item drops": {
                    "ABNORMAL DEER SKULL": [1, 30, "health"],
                    "WENDIGO CLAW DAGGER": [1, 35, "damage"],
                    "BLADE OF SACRIFICE": [1, 50, "damage"]
                }
            }
        ]
    }

    def GetDamage(self, num1, num2):
        damage = random.randint(num1, num2)
        return damage

    def GetDabloons(self, num1, num2):
        dabloons = random.randint(num1, num2)
        return dabloons

