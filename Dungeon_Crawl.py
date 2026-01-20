import random

#Note: Added class difference for level up stats + mage (double attack), thief (steal item after battle), warrior (ATK +0.2 after battle)

# ---------- CLASSES ----------
CLASSES = {
    "warrior": {"HP": 120, "MP": 20, "ATK": 8, "DEF": 6, "DODGE": 2},
    "mage":    {"HP": 80,  "MP": 60, "ATK": 10,"DEF": 3, "DODGE": 3},
    "thief":   {"HP": 90,  "MP": 30, "ATK": 7, "DEF": 4, "DODGE": 6},
}


#---------------File Saver------------

FILENAME = "top_floors.txt"

def save_if_top3(name, klass, f_id, lvl, swds, shlds, arm):
    
    f_id = int(f_id)

    records = []

    # Read existing records
    try:
        with open(FILENAME, "r") as f:
            for line in f:
                if line.strip():
                    # Extract Floor-ID from saved line
                    # Example saved line:
                    # Player: Ryan,| Class: Warrior| Final Floor: 12|Level: 5|Swords: 3|Shields: 1|Armor: 2
                    parts = line.strip().split("|")
                    floor_part = parts[2]  # "Final Floor: 12"
                    saved_floor = int(floor_part.split(":")[1])
                    records.append((saved_floor, line.strip()))
    except FileNotFoundError:
        pass

    # Format new record
    formatted = (
        f"Player: {name},| Class: {klass} | Final_Floor: {f_id}|Level: {lvl}"
        f"|Swords: {swds}|Shields: {shlds}|Armor: {arm}"
    )

    records.append((f_id, formatted))

    # Sort by Final Floor (descending)
    records.sort(key=lambda x: x[0], reverse=True)

    # Keep only top 3
    top3 = records[:3]

    # Save only if new record made top 3
    if any(r[1] == formatted for r in top3):
        with open(FILENAME, "w") as f:
            for _, line in top3:
                f.write(line + "\n")
        return True

    return False

# ---------- PLAYER ----------
class Player:
    def __init__(self, cls, name):
        base = CLASSES[cls]
        self.cls = cls
        self.level = 1
        self.floor = 1
        self.exp = 0
        self.exp_to_next = 25
        self.max_stamina = 30
        self.stamina = 30
        self.swords = 0
        self.armor = 0
        self.shields = 0
        self.name = name

        self.max_hp = base["HP"]
        self.hp = self.max_hp
        self.max_mp = base["MP"]
        self.mp = self.max_mp

        self.atk = base["ATK"]
        self.defense = base["DEF"]
        self.dodge = base["DODGE"]

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_next += 25

        if self.cls == "warrior":
            self.max_hp += 20
            self.max_mp += 1
            self.atk += 3
            self.defense += 3
            self.dodge += 1
        elif self.cls == "mage":
            self.max_hp += 15
            self.max_mp += 5
            self.atk += 2
            self.defense += 2
            self.dodge += 2
        else:
            self.max_hp += 10
            self.max_mp += 5
            self.atk += 3
            self.defense += 1
            self.dodge += 3
            
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.stamina += 5
        if self.stamina >= self.max_stamina:
            self.stamina = self.max_stamina
            
        print("🔥 LEVEL UP! Stats boosted.\n")
        print(f"Attack: {self.atk} | Dodge: {self.dodge} | Defense: {self.defense} | Stamina: {self.stamina}")

    def heal(self):
            self.stamina -=1
            current = self.hp
            heal = int(self.max_hp/random.randint(5,10))
            full = self.hp + heal
            if full > self.max_hp:
                self.hp = self.max_hp
                print(f"Player healed for: {full-heal} HP")
            else:
                self.hp += heal
                print(f"Player healed for: {heal} HP")
            print(f"\n📍 Floor {self.floor} | HP {self.hp}/{self.max_hp} | Stamina: {self.stamina}/{self.max_stamina}")

    def magic(self):
            current = self.stamina
            if self.mp - 10 >= 0:
                if (current + 2) > self.max_stamina:
                    self.stamina = self.max_stamina
                    self.mp -= 10
                    print(f"Player used 10MP to raise stamina to: {self.stamina}")
                else:
                    self.stamina += 2
                    self.mp -= 10
                    print(f"Player used 10MP to raise stamina to: {self.stamina}")
            else:
                print(f"Player does not have 10MP to use. MP left: {self.mp}")
                
            print(f"\n📍 Floor {self.floor} | HP {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | Stamina: {self.stamina}/{self.max_stamina}")
    


# ---------- MONSTERS ----------
class Monster:
    def __init__(self, floor, boss=False):
        scale = max(1,(floor + random.randint(-1, 1)))
        self.boss = boss
        mult = 3 if boss else 2

        self.hp = max(20, scale + (30 * mult))
        self.max_hp = self.hp
        self.atk = scale * 1.2 * mult
        self.defense = scale * mult
        self.exp = scale * 4 * mult

# ---------- COMBAT ----------
def combat(player, monster):
    print("⚔️ Combat started!\n")
    print(f"\n📍 MonsterHP: {monster.hp} | Player HP {player.hp}/{player.max_hp}")
    while player.hp > 0 and monster.hp > 0:
        # Player attack
        if player.cls == "mage":
            amount = 2
        else:
            amount = 1
        
        for i in range(amount):
            if random.randint(1,4) < 3:
                atk = int(player.atk - monster.defense)
                if atk <= 1:
                    atk = 2
                dmg = max(1,random.randint(int(atk/2), atk))
                monster.hp -= dmg
                print(f"You hit for {dmg} dmg. Monster HP: {int(monster.hp)}/{int(monster.max_hp)}")
            else:
                print(f"Enemy blocked! Monster HP: {int(monster.hp)}/{int(monster.max_hp)}")

        if monster.hp <= 0:
            print("💀 Enemy defeated!\n")

            player.exp += monster.exp
            
            if player.cls == "thief":
                find_loot(player)
                
            elif player.cls == "warrior":
            	player.atk +=0.2
            	print(f"Player attack went up by 0.2. Attack is now {player.atk}")
                    
            print(f"PlayerHP: {player.hp}/{player.max_hp} | Player EXP {player.exp}/{player.exp_to_next} | Stamina {player.stamina}/{player.max_stamina}")
            if player.exp >= player.exp_to_next:
                player.level_up()
            return True

        # Monster attack
        if random.randint(1, 100) > min(50,player.dodge) and monster.hp > 0:
            atk = int(monster.atk - player.defense)
            if atk <= 1:
                atk = 2
            dmg = max(1,random.randint(1, atk))
            player.hp -= dmg
            print(f"You take {dmg} dmg. Player HP: {player.hp}/{player.max_hp}")
        else:
            print("You dodged!")

    return False

# ---------- LOOT ----------
def find_loot(player):
    loot = random.choice(["sword", "shield", "armor"])
    bonus = random.randint(1, 3) + player.floor // 3

    if loot == "sword":
        player.atk += bonus
        player.swords +=1
        print(f"🗡 Sword found! ATK +{bonus}")
    elif loot == "shield":
        player.dodge += bonus
        player.shields += 1
        print(f"🛡 Shield found! DODGE +{bonus}")
    else:
        player.defense += bonus
        player.armor += 1
        print(f"🥋 Armor found! DEF +{bonus}")

# ---------- GAME LOOP ----------
def game():
    name = input("What is your players name?\n")
    
    cls = input("Choose class (warrior/mage/thief): ").lower()
    if cls not in CLASSES:
        print("Invalid class.")
        return

    player = Player(cls,name)
    print("🏰 Dungeon crawl begins.")
    end = False
    print ("Commands: y = continue; n = end game; h = heal; m = magic +2 stamina")
    while player.hp > 0:
    
        quest = input("\nWould you like to continue or heal? (y/n/h/m): ").lower()

        if quest == "h" and player.stamina >= 1:
            player.heal()

        elif quest == "m" and player.stamina >= 1:
            player.magic()
            
        elif quest == "y" and player.stamina >= 1:

            player.stamina -= 1
        
            print(f"\n📍 Floor {player.floor} | HP {player.hp}/{player.max_hp} | Stamina: {player.stamina}/{player.max_stamina}")

            roll = random.randint(1, 100)

            # Boss every 10 floors
            if player.floor % 10 == 0:
                print("👑 BOSS FLOOR!")
                if not combat(player, Monster(player.floor, boss=True)):
                    break
                find_loot(player)
                player.stamina = player.max_stamina
                player.floor += 1
                continue

            if roll <= 40:
                if not combat(player, Monster(player.floor)):
                    break
            elif roll <= 65:
                find_loot(player)
            elif roll <= 80:
                print("🚪 You found the stairs.")
                player.floor += 1
            else:
                print("😌 Quiet floor...")

        elif quest == "n" and player.stamina > 0:
            player.hp = 0
        elif player.stamina <= 0:
            print("You ran out of stamina.")
            player.hp = 0
        else:
            print("That wasn't an option")
            
    print("\n☠️ GAME OVER")
    print(f"Final Floor: {player.floor} | Level: {player.level} | Swords: {player.swords} | Shields: {player.shields} | Armor: {player.armor}")
    save_if_top3(player.name,player.cls,player.floor,player.level,player.swords,player.shields,player.armor)
# ---------- RUN ----------
if __name__ == "__main__":
    game()
