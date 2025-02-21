import random
#la classe Arme
class Arme:
    def __init__(self, nom, degats):
        self.nom = nom
        self.degats = degats

#liste d'armes disponibles
armes_disponibles = [
    Arme("Épée", 5),
    Arme("Arc", 4),
    Arme("Bâton magique", 6),
    Arme("Dague", 3),
    Arme("Lance", 6),
    Arme("Rayon laser", 8),
    Arme("Baguette magique", 5),
    Arme("Toile d'araigné", 7),
    Arme("Griffes", 4)
]
#la classe Creature
class Creature:
    def __init__(self, nom, description, pv, defense, initiative, typeDegats):
        self.nom = nom
        self.description = description
        self.pv_max = pv
        self.pv = pv
        self.defense = defense
        self.initiative = initiative
        self.typeDegats = typeDegats
        self.etats = [] #liste pour stocker les effets d'état
        self.actions = []
        self.force = 10
        self.arme = None
        self.objets = [] #liste pour stocker les objets

#afficher les caractéristiques de la créature
    def afficher_caracteristiques(self):
        print(f"Nom: {self.nom}")
        print(f"PV: {self.pv}/{self.pv_max}")
        print(f"Défense: {self.defense}")
        print(f"Force: {self.force}")
        print(f"Arme: {self.arme.nom if self.arme else 'Aucune'}")
        print(f"États: {', '.join([etat['effet'] for etat in self.etats]) if self.etats else 'Aucun'}")

#attaquer une cible
    def attaquer(self, cible):
        degats = random.randint(1, 6) + self.force - cible.defense
        if self.arme:
            degats += self.arme.degats
        degats = max(degats, 0)
        cible.pv -= degats
        cible.pv = max(cible.pv, 0)
        print(f"{self.nom} attaque {cible.nom} et inflige {degats} dégâts!")

#augmenter la force (buff)
    def buff(self):
        buff_value = random.randint(2, 5)
        self.force += buff_value
        print(f"{self.nom} se renforce et gagne {buff_value} en Force!")

#réduire la défense de la cible (debuff)
    def debuff(self, cible):
        debuff_value = random.randint(1, 3)
        cible.defense -= debuff_value
        cible.defense = max(cible.defense, 0)
        print(f"{self.nom} affaiblit {cible.nom}, réduisant sa défense de {debuff_value}!")

#appliquer un effet d'état à une créature
def appliquer_effet(creature, effet, duree):
    creature.etats.append({"effet": effet, "duree": duree})
    print(f"{creature.nom} est maintenant {effet} pour {duree} tours!")

#appliquer un effet d'état à une créature
def gerer_effets(creature):
    for etat in creature.etats:
        if etat["effet"] == "empoisonné":
            degats = random.randint(1, 3)
            creature.pv -= degats
            print(f"{creature.nom} subit {degats} dégâts de poison!")
        elif etat["effet"] == "paralysé":
            if random.random() < 0.5:
                print(f"{creature.nom} est paralysé et ne peut pas agir ce tour!")
                return False
        etat["duree"] -= 1
    creature.etats = [etat for etat in creature.etats if etat["duree"] > 0]
    return True

#utiliser un objet
def utiliser_objet(creature, objet):
    if objet == "Potion de soin":
        soin = random.randint(15, 25)
        creature.pv = min(creature.pv + soin, creature.pv_max)
        print(f"{creature.nom} utilise une Potion de soin et récupère {soin} PV!")
    elif objet == "Potion de force":
        buff = random.randint(2, 5)
        creature.force += buff
        print(f"{creature.nom} utilise une Potion de force et gagne {buff} en Force!")
    elif objet == "Antidote":
        creature.etats = [etat for etat in creature.etats if etat["effet"] != "empoisonné"]
        print(f"{creature.nom} utilise un Antidote et n'est plus empoisonné!")

#sélectionner une créature parmi une liste
def selectionner_creature(creatures):
    while True:
        for i, creature in enumerate(creatures):
            print(f"{i + 1}. {creature.nom} - {creature.description}")
        try:
            choix = int(input("Choisissez une créature: ")) - 1
            if 0 <= choix < len(creatures):
                return creatures[choix]
            else:
                print("Erreur: Veuillez entrer un nombre valide parmi les choix proposés.")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide.")

#choisir une action
def choisir_action(creature, cible):
    actions = ["Attaquer", "Buff", "Debuff", "Utiliser un objet"]
    while True:
        print("Actions disponibles:")
        for i, action in enumerate(actions):
            print(f"{i + 1}. {action}")
        try:
            choix = int(input("Choisissez une action: ")) - 1
            if 0 <= choix < len(actions):
                action = actions[choix]
                if action == "Attaquer":
                    creature.attaquer(cible)
                elif action == "Buff":
                    creature.buff()
                elif action == "Debuff":
                    creature.debuff(cible)
                elif action == "Utiliser un objet":
                    if creature.objets:
                        print("\nObjets disponibles:")
                        for i, objet in enumerate(creature.objets):
                            print(f"{i + 1}. {objet}")
                            choix_objet = int(input("Choisissez un objet à utiliser: ")) - 1
                        if 0 <= choix_objet < len(creature.objets):
                            objet_utilise = creature.objets.pop(choix_objet)
                            utiliser_objet(creature, objet_utilise)
                        else:
                            print("Objet invalide, action annulée.")
                            continue
                    else:
                        print("Vous n'avez pas d'objets à utiliser.")
                        continue
                return action
            else:
                print("Erreur: Veuillez entrer un nombre valide parmi les actions proposées.")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide.")

#choisir une arme
def choisir_arme():
    print("\nArmes disponibles:")
    for i, arme in enumerate(armes_disponibles):
        print(f"{i + 1}. {arme.nom} (Dégâts: {arme.degats})")
    while True:
        try:
            choix = int(input("Choisissez une arme: ")) - 1
            if 0 <= choix < len(armes_disponibles):
                return armes_disponibles[choix]
            else:
                print("Erreur: Veuillez entrer un nombre valide parmi les choix proposés.")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide.")

#fonction principale du jeu
def main():
    print("Bienvenue dans le système de combat RPG!")

#définition des héros disponibles
    heros_disponibles = [
        Creature("Guerrier", "Un brave guerrier", 50, 15, 2, "Tranchant"),
        Creature("Mage", "Un puissant mage", 30, 10, 1, "Magique"),
        Creature("Archer", "Un archer précis", 40, 12, 3, "Percant"),
        Creature("Spider man", "L'araignée sympa du quartier", 60, 18, 4, "Toile"),
        Creature("Druide", "Un gardien de la nature", 45, 13, 5, "Nature"),
        Creature("Chevalier", "Un chevalier sacré", 55, 14, 6, "Tranchant"),
        Creature("Super man", "L'Homme d'Acier", 100, 20, 5, "Laser")
    ]

#définition des monstres disponibles
    monstres_disponibles = [
        Creature("Gobelin", "Un gobelin vicieux", 20, 10, 1, "Percant"),
        Creature("Dragon", "Un dragon redoutable", 100, 20, 5, "Feu"),
        Creature("Troll", "Un troll massif", 80, 18, 0, "Contondant"),
        Creature("Squelette", "Un guerrier mort-vivant", 30, 12, 2, "Tranchant"),
        Creature("Loup-garou", "Une bête féroce", 60, 15, 3, "Tranchant"),
        Creature("Golem de pierre", "Un colosse de roche", 90, 22, 1, "Écrasant"),
        Creature("Sorcière", "Une pratiquante de magie noire", 45, 11, 2, "Magique"),
    ]

#sélection du héros
    print("\nChoisissez votre héros:")
    hero = selectionner_creature(heros_disponibles)
    print(f"\nVous avez choisi {hero.nom}.")

#choix de l'arme du héros
    print("\nChoisissez une arme pour votre héros:")
    hero.arme = choisir_arme()
    print(f"{hero.nom} est équipé de {hero.arme.nom}.")

#sélection du monstre
    print("\nChoisissez le monstre à combattre:")
    monstre = selectionner_creature(monstres_disponibles)
    print(f"\nVous allez affronter {monstre.nom}!")

#choix de l'arme du monstre
    print("\nChoisissez une arme pour le monstre:")
    monstre.arme = choisir_arme()
    print(f"{monstre.nom} est équipé de {monstre.arme.nom}.")

#attribution d'objets au héros
    hero.objets = ["Potion de soin", "Potion de force", "Antidote"]

#boucle principale du combat
    tour = 1
    while hero.pv > 0 and monstre.pv > 0:
        print(f"\n--- Tour {tour} ---")

#tour du héros        
        if gerer_effets(hero):
            print(f"\nC'est au tour de {hero.nom}!")
            hero.afficher_caracteristiques()
            action_hero = choisir_action(hero, monstre)

#tour du monstre (si toujours en vie)        
        if monstre.pv > 0:
            if gerer_effets(monstre):
                print(f"\nC'est au tour de {monstre.nom}!")
                monstre.afficher_caracteristiques()
                action_monstre = random.choice(["Attaquer", "Buff", "Debuff"])
                if action_monstre == "Attaquer":
                    monstre.attaquer(hero)
                    #chance d'appliquer un effet d'état
                    if random.random() < 0.2:
                        effet = random.choice(["empoisonné", "paralysé"])
                        appliquer_effet(hero, effet, random.randint(1, 3))
                elif action_monstre == "Buff":
                    monstre.buff()
                else:
                    monstre.debuff(hero)
                print(f"{monstre.nom} a choisi l'action {action_monstre}!")

        tour += 1

#fin du combat
    if hero.pv <= 0:
        print(f"\n{hero.nom} a été vaincu. Game Over!")
    else:
        print(f"\nFélicitations! {hero.nom} a vaincu {monstre.nom}!")

#entrée du programme
if __name__ == "__main__":
    main()
