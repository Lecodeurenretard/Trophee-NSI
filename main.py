import pygame
import subprocess
import sys
import time
import random


pygame.init()
pygame.display.set_caption("Menu Principal")

clock = pygame.time.Clock()

largeur = 800 ;   hauteur = 600
fenetre = pygame.display.set_mode((largeur, hauteur))
noir = [0, 0, 0]
blanc = [255, 255, 255]
rouge = [255, 0, 0]
bleu = [0, 0, 255]
vert = [0, 255, 0]
fenetre.fill((blanc))

BLANC = (255, 255, 255)
GRIS = (100, 100, 100)
BLEU = (50, 50, 255)
font = pygame.font.SysFont(None, 50)

nbr_combat = 1
police_ecriture = pygame.font.Font(None, 36)
police_ecriture2 = pygame.font.Font(None, 25)
texte_gagner = police_ecriture.render("Vous avez gagné !", True, noir)
texte_perdu = police_ecriture.render("Vous avez perdu !", True, noir)
texte_torgnole = police_ecriture.render("Torgnole", True, blanc)
texte_soin = police_ecriture.render("Soin", True, blanc)
texte_magique = police_ecriture.render("Att. magique", True, blanc)
texte_input_ligne1 = police_ecriture2.render("SPACE : utiliser", True, blanc)
texte_input_ligne2 = police_ecriture2.render("I : info", True, blanc)
tour_joueur = True
degat = 0
charge = 20
att_magique = 45
barre_vie_adversaire, barre_vie_joueur = 200, 200
perso_stat = {"vie": 50, "force": 35, "defense": 40, "magie": 20, "defense_magique": 30, "vitesse": 50}
blob_stat = {"vie": 40, "force": 30, "defense": 45, "magie": 0, "defense_magique": 25, "vitesse": 30}
sorcier_stat = {"vie": 30, "force": 10, "defense": 30, "magie": 15, "defense_magique": 80, "vitesse": 60}
curseur_x, curseur_y = 50, (13*(hauteur//16))
joueur_vie = perso_stat["vie"]
running = True


def demander_pseudo():
    pseudo = ""
    saisie = True
    font = pygame.font.SysFont(None, 48)
    while saisie:
        fenetre.fill(blanc)
        texte = font.render("Entrez votre pseudo :", True, noir)
        fenetre.blit(texte, (largeur // 2 - 180, hauteur // 2 - 60))
        pseudo_affiche = font.render(pseudo, True, bleu)
        fenetre.blit(pseudo_affiche, (largeur // 2 - 100, hauteur // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(pseudo) > 0:
                    saisie = False
                elif event.key == pygame.K_BACKSPACE:
                    pseudo = pseudo[:-1]
                else:
                    if len(pseudo) < 12 and event.unicode.isprintable():
                        pseudo += event.unicode
    return pseudo



def afficher_info():
    if curseur_x == 50 and curseur_y == (13 * (hauteur // 16)):
        info = police_ecriture.render("Puissance: 0,5", True, noir)
        info2 = police_ecriture.render("Soigner-vous de quelque pv ", True, noir)
        fenetre.fill(blanc)
        fenetre.blit(info, (3*(largeur//10), (hauteur//2)))
        fenetre.blit(info2, (3*(largeur//10)-100, (hauteur//2)+30))
        pygame.display.flip()
        time.sleep(2)
    elif curseur_x == 50 and curseur_y == (13 * (hauteur // 16)) + 70:
        info = police_ecriture.render("Puissance: 20", True, noir)
        info2 = police_ecriture.render("Infligez des dégâts physiques à l'adversaire", True, noir)
        fenetre.fill(blanc)
        fenetre.blit(info, (3*(largeur//10), (hauteur//2)))
        fenetre.blit(info2, (3*(largeur//10)-100, (hauteur//2)+30))
        pygame.display.flip()
        time.sleep(2)

def chek_monstre():
    global monstre_stat, sorcier_stat, blob_stat, color, monstre_vie, nom_adversaire
    monstre_stat = random.choice([blob_stat, sorcier_stat])
    monstre_vie = monstre_stat["vie"]
    if monstre_stat == blob_stat:
        color = rouge
        nom_adversaire = "Blob"
    else:
        color = bleu
        nom_adversaire = "Sorcier"

def monstre_attaque():
    global joueur_vie, barre_vie_joueur, barre_vie_adversaire, monstre_stat, perso_stat
    if nom_adversaire== "Blob":  # 50% de chance d'attaquer physiquement
        pygame.draw.rect(fenetre, rouge, (400, 300 , 200, 50), 5)
        degats = degat_recu_physique(monstre_stat, perso_stat, charge)
        joueur_vie = max(0, joueur_vie - degats)
        barre_vie_joueur = pourcentage_vie(joueur_vie, perso_stat["vie"])
        pygame.display.flip()
        time.sleep(1)
        pygame.event.clear()
    else:  # Attaque magique
        pygame.draw.rect(fenetre, rouge, (400, 300 , 200, 50), 5)
        degats = degat_recu_magique(monstre_stat, perso_stat, att_magique)
        joueur_vie = max(0, joueur_vie - degats)
        barre_vie_joueur = pourcentage_vie(joueur_vie, perso_stat["vie"])
        pygame.display.flip()
        time.sleep(1)
        pygame.event.clear()


def chargement():
    barre = 0
    while barre < 700:
        fenetre.fill(blanc)
        pygame.draw.rect(fenetre, noir, (50, 300, barre, 50), 0)
        texte_chargement = police_ecriture.render("Chargement...", True, noir)
        fenetre.blit(texte_chargement, (300, 350))
        pygame.display.flip()
        barre += 2
        time.sleep(0.01)
        pygame.event.clear()

def afficher_nombre_combat(nbr_combat):
    texte_combat = police_ecriture.render(f"Combat n°{nbr_combat}", True, noir)
    fenetre.fill(blanc)
    fenetre.blit(texte_combat, (largeur // 2 - 100, hauteur // 2 - 20))
    pygame.display.flip()
    time.sleep(2)



def attaque_soin(perso_stat, puissance_soin):
    soin = perso_stat["magie"] * puissance_soin * random.uniform(0.85, 1.0)
    soin = int(soin)
    return soin

def degat_infliger_physique(perso_stat, monstre_stat, puissance_attaque):
    attaque = perso_stat["force"]
    defense = monstre_stat["defense"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def degat_infliger_magique(perso_stat, monstre_stat, puissance_attaque):
    attaque = perso_stat["magie"]
    defense = monstre_stat["defense_magique"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def degat_recu_magique(monstre_stat, perso_stat, puissance_attaque):
    attaque = monstre_stat["magie"]
    defense = perso_stat["defense_magique"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def degat_recu_physique(monstre_stat, perso_stat, puissance_attaque):
    attaque = monstre_stat["force"]
    defense = perso_stat["defense"]
    degats = ((attaque * puissance_attaque) / (defense + 10)) * random.uniform(0.85, 1.0)
    degats = max(1, int(degats))
    return degats

def pourcentage_vie(vie_restante, vie_initiale):
    pourcentage = (vie_restante / vie_initiale) * 200
    return max(0, pourcentage)
    


class Button:
    def __init__(self, text, x, y, w, h, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = GRIS
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = font.render(self.text, True, BLANC)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.action:
                self.action()

def jouer():
    global running, pseudo_joueur
    running = False
    chargement()
    pseudo_joueur = demander_pseudo()
    afficher_nombre_combat(nbr_combat)
    

def ouvrir_parametres():
    print("→ Ouverture des paramètres...")

def afficher_credits():
    texte_credits = font.render("Développé par Jules et Lucas", True, BLANC)
    credit_y = hauteur
    running = False
    while credit_y > 0:
        fenetre.fill(noir)
        fenetre.blit(texte_credits, (150, credit_y))
        credit_y -= 1
        pygame.display.flip()
        pygame.time.delay(4)
    print("→ Affichage des crédits...")

boutons = [
    Button("Jouer", 300, 200, 200, 60, jouer),
    Button("Paramètres", 300, 300, 200, 60, ouvrir_parametres),
    Button("Crédits", 300, 400, 200, 60, afficher_credits),
]


def rafraichir_ecran():
    # Effacer l'écran en redessinant l'arrière-plan
    fenetre.fill(blanc)


    # Redessiner les éléments fixes (par exemple, les rectangles)
    pygame.draw.rect(fenetre, noir, (0, 3 * (hauteur // 4), 800, 600), 0)
    pygame.draw.rect(fenetre, bleu, ((largeur // 4), 3 * (hauteur // 4) - 100, 100, 100), 0)
    pygame.draw.rect(fenetre, color, (6 * (largeur // 10), (hauteur // 4) - 100, 100, 100), 0)
    pygame.draw.rect(fenetre, blanc, (70, (13*(hauteur//16))-25 , 200, 50), 5) # soin
    pygame.draw.rect(fenetre, blanc, (70, (13 * (hauteur // 16)) + 45 , 200, 50), 5) # torgnole
    pygame.draw.rect(fenetre, blanc, (375, (13*(hauteur//16))-25 , 200, 50), 5)
    pygame.draw.rect(fenetre, blanc, (375, (13 * (hauteur // 16)) + 45 , 200, 50), 5)

    # Afficher vie des personnages
    pygame.draw.rect(fenetre, vert, (50, 50 , barre_vie_adversaire, 10), 0)
    pygame.draw.rect(fenetre, noir, (49, 49 , 202, 11), 2)
    fenetre.blit(police_ecriture.render(nom_adversaire, True, noir), (49, 20))

    pygame.draw.rect(fenetre, vert, (500, 400 , barre_vie_joueur, 10), 0)
    pygame.draw.rect(fenetre, noir, (499, 399 , 202, 11), 2)
    fenetre.blit(police_ecriture.render(pseudo_joueur, True, noir), (499, 370))

    # Dessiner le cercle à la nouvelle position
    pygame.draw.circle(fenetre, vert, (curseur_x, curseur_y), 10, 0)

    # Afficher nom des attaques
    fenetre.blit(texte_soin, (140, (13 * (hauteur // 16)) - 12))
    fenetre.blit(texte_torgnole, (120, (13 * (hauteur // 16)) + 60))
    fenetre.blit(texte_magique, (400, (13 * (hauteur // 16)) - 12))
    fenetre.blit(texte_input_ligne1, (620, (13 * (hauteur // 16)) - 12))
    fenetre.blit(texte_input_ligne2, (620, (13 * (hauteur // 16)) + 20))


    # Mettre à jour l'affichage
    pygame.display.flip()





pygame.display.flip()
# Fonction bloquante incluse dans la bibliothèque Graphique.py
# permettant de fermer la fenêtre et de stopper le programme

chek_monstre()
while True:
    while running:
        fenetre.fill(BLEU)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for bouton in boutons:
                    bouton.check_click(event.pos)
        for bouton in boutons:
            bouton.draw(fenetre)
        pygame.display.flip()

    rafraichir_ecran()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and tour_joueur:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_i:
                afficher_info()
            if event.key == pygame.K_UP:
                if curseur_y != (13 * (hauteur // 16)):
                    curseur_y = (13 * (hauteur // 16))
            if event.key == pygame.K_DOWN:
                if curseur_y != (13 * (hauteur // 16)) + 70:
                    curseur_y = (13 * (hauteur // 16)) + 70
            if event.key == pygame.K_LEFT:
                if curseur_x != 50:
                    curseur_x = 50
            if event.key == pygame.K_RIGHT:
                if curseur_x != 350:
                    curseur_x = 350
            if event.key == pygame.K_SPACE:
                if curseur_x == 50 and curseur_y == (13 * (hauteur // 16)):
                    pygame.draw.rect(fenetre, noir, (400, 300 , 200, 50), 5)
                    heal = attaque_soin(perso_stat, 1.5)
                    joueur_vie = min(joueur_vie + heal, perso_stat["vie"])  # Ne pas dépasser la vie maximale
                    barre_vie_joueur = pourcentage_vie(joueur_vie, perso_stat["vie"])
                    pygame.display.flip()
                    time.sleep(1)
                    pygame.event.clear()
                    rafraichir_ecran()
                    time.sleep(1)
                    pygame.event.clear()
                elif curseur_x == 350 and curseur_y == (13 * (hauteur // 16)):
                    pygame.draw.rect(fenetre, bleu, (400, 300 , 200, 50), 5)
                    degat_magique = degat_infliger_magique(perso_stat, monstre_stat, att_magique)
                    monstre_vie = max(0, monstre_vie - degat_magique)  # Empêche la vie de passer sous 0
                    barre_vie_adversaire = pourcentage_vie(monstre_vie, monstre_stat["vie"])
                    pygame.display.flip()
                    time.sleep(1)
                    pygame.event.clear()
                    rafraichir_ecran()
                    time.sleep(1)
                    pygame.event.clear()
                elif curseur_x == 50 and curseur_y == (13 * (hauteur // 16)) + 70:
                    pygame.draw.rect(fenetre, vert, (400, 300 , 200, 50), 5)
                    degat = degat_infliger_physique(perso_stat, monstre_stat, charge)
                    monstre_vie = max(0, monstre_vie - degat)  # Empêche la vie de passer sous 0
                    barre_vie_adversaire = pourcentage_vie(monstre_vie, monstre_stat["vie"])
                    pygame.display.flip()
                    time.sleep(1)
                    pygame.event.clear()
                    rafraichir_ecran()
                    time.sleep(1)
                    pygame.event.clear()
                elif curseur_x == 350 and curseur_y == (13 * (hauteur // 16)) + 70:
                    pygame.draw.rect(fenetre, rouge, (400, 300 , 200, 50), 5)
                    pygame.display.flip()
                    time.sleep(1)
                tour_joueur = False


    if monstre_vie <= 0 and nbr_combat > 4:
        fenetre.fill(blanc)
        fenetre.blit(texte_gagner, ((largeur // 2) - 120, hauteur // 2 - 20))
        pygame.display.flip()
        print("Vous avez gagné !")
        time.sleep(2)
        pygame.quit()
        sys.exit()
    elif monstre_vie <= 0:
        nbr_combat += 1
        afficher_nombre_combat(nbr_combat)
        chek_monstre()
        barre_vie_adversaire = pourcentage_vie(monstre_vie, monstre_stat["vie"])
        barre_vie_joueur = pourcentage_vie(joueur_vie, perso_stat["vie"])
        tour_joueur = True

    if not tour_joueur:
        monstre_attaque()
        tour_joueur = True
        if joueur_vie <= 0:
            fenetre.fill(blanc)
            fenetre.blit(texte_perdu, ((largeur // 2) - 120, hauteur // 2 - 20))
            pygame.display.flip()
            print("Vous avez gagné !")
            time.sleep(2)
            pygame.quit()
            sys.exit()

    
    rafraichir_ecran()
    clock.tick(60)  # Limite la boucle à 60 FPS

