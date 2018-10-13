from utils.models import session, KEYWORD

def add_keyword(keyword=None):
    if not keyword:
        keyword = input("Veuillez entrer le nouveau mot clé à ajouter. Pour les hashtags, inclure le symbole '#'\n")
        keyword = keyword.replace('#', '%23')

    existing_keyword = session.query(KEYWORD).filter(KEYWORD.valeur==keyword)
    if not existing_keyword.all(): #CASE 1 : keyword doesnt exist ==> new keyword create
        new_entry = KEYWORD(keyword)
        session.add(new_entry)
        session.commit()
    elif existing_keyword.one().active==False: #CASE 2 : keywords already exists but inactive : ask if want to activate it
        reactivate = input("Le mot clé est déjà présent dans la base de données. Souhaitez vous le réactiver ? (o/n)\n")
        if reactivate == "o": 
            activate_keyword(keyword)
        else:
            print("Le mot clé n'a pas été réactivé")
    else : #CASE 3 : keyword already exists and is active : do nothing"
        print("Le mot clé est déjà présent dans la base de données")
    session.close()

def desactivate_keyword(keyword=None):
    if not keyword:
        keyword = input("Veuillez entrer la valeur du mot clé à désactiver. Ce mot clé ne sera pas supprimé de la base de données. Pour les hashtags, inclure le symbole '#'\n")
        keyword = keyword.replace('#', '%23')

    existing_keyword = session.query(KEYWORD).filter(KEYWORD.valeur==keyword)
    if not existing_keyword.all(): #CASE 1 : keyword doesnt exists ==> stop
        print("Le mot clé demandé n'existe pas")
    else:
        existing_keyword.one().active=False
        session.commit()
        print("Le mot clé a été désactivé")
    session.close()


def activate_keyword(keyword=None):
    if not keyword:
        keyword = input("Veuillez entrer la valeur du mot clé à réactiver. Pour les hashtags, inclure le symbole '#'\n")
        keyword = keyword.replace('#', '%23')

    existing_keyword = session.query(KEYWORD).filter(KEYWORD.valeur==keyword)
    if not existing_keyword.all(): #CASE 1 : keyword doesnt exists ==> proposer création
        create = input("Le mot clé n'existe pas. Souhaitez vous le créer ? (o/n)\n")
        if create=="o":
            add_keyword(keyword)
    else:
        existing_keyword.one().active=True
        session.commit()
        print("Le mot clé a été réactivé")
    session.close()

def delete_keyword(keyword=None):
    if not keyword:
        keyword = input("Veuillez entrer la valeur du mot clé à supprimer. Pour les hashtags, inclure le symbole '#'. Attention, cette action est irréversible\n")
        keyword = keyword.replace('#', '%23')

        existing_keyword = session.query(KEYWORD).filter(KEYWORD.valeur==keyword)
        if not existing_keyword.all(): #CASE 1 : keyword doesnt exists ==> stop
            print("Le mot clé demandé n'existe pas")
        else : #CASE 2 : keyword exists ==> delete
            existing_keyword.delete()
            session.commit()
            print("Le mot clé a été supprimé")
        session.close()

def display_keywords():
    keywords = session.query(KEYWORD).all()
    print("LISTE DES MOTS CLES :")
    for keyword in keywords:
        if keyword.active:
            statut = "actif"
        else:
            statut="inactif"
        print(f"     { keyword.valeur.replace('%23', '#') } ({ statut })")

def menu_keyword():
    choix = input("""\n
GESTION DES MOTS CLES DE RECHERCHE
Veuillez choisir un numéro parmi les propositions suivantes :
    1 - Afficher tous les mots clés
    2 - Ajouter un mot clé
    3 - Désactiver un mot clé
    4 - Réactiver un mot clé
    5 - Supprimer définitivement un mot clé
    6 - Quitter le programme
    """)
    return choix
    

def main():
    while 1:
        choix = menu_keyword()
        if choix =="1":
            display_keywords()
        elif choix == "2":
            add_keyword()
        elif choix == "3":
            desactivate_keyword()
        elif choix=="4":
            activate_keyword()
        elif choix=="5":
            delete_keyword()
        elif choix=="6":
            print("Programme terminé !")
            break
        else:
            print("Veuillez entrer un numéro parmi les choix proposés")


if __name__=='__main__':
    main()