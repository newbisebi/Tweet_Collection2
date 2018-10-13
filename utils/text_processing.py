import treetaggerwrapper
from nltk.tokenize import word_tokenize
from string import punctuation

# On veut garder certains caractères de ponctuation
punctuation = [p for p in punctuation if p not in "!?$#%&+-"] 

par = "text_processing_tools/french-utf8.par"
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGPARFILE=par)
exclude_type = ["ADV", "DET:ART", "DET:POS", "KON", "NUM", "PRO",
                "PRO:DEM", "SENT", "PRO:IND", "PRO:PER", "PRO:POS",
                "PRO:REL", "PRP", "PRP:det", "PUN", "PUN:cit", "SYM"]


def processing(text, return_token=False):
    text = text.replace('#', '# ')
    text_tagged = tagger.tag_text(text)
    text_tagged = treetaggerwrapper.make_tags(
        text_tagged, exclude_nottags=True)
    list_lemm = [
        tag.lemma for tag in text_tagged if tag.pos not in exclude_type
        ]
    # liste = reduc(liste)
    new_text = ' '.join(list_lemm)
    # new_text = new_text.replace(u"url-remplacée",u"")
    # new_text = new_text.replace(u"email-remplacé",u"")
    # new_text = new_text.replace(u"dns-remplacé",u"")
    for p in punctuation:
        new_text = new_text.replace(p, "")
    new_text = new_text.replace("  ", " ").replace("  ", " ").lower()
    if new_text == "" or new_text is None:
        new_text = "empty-tweet"

    if return_token:
        new_text = word_tokenize(new_text)

    return new_text


def format_sentence(sent):
    """Format data for classification"""
    sent = processing(sent)
    return ({word: True for word in word_tokenize(sent)})


if __name__ == '__main__':
    pass
    # Test data:

    # processing(""" @soissonschris Bugatti Chiron #Mondial2018 https://t.co/b0MATr1iJC """)
    # processing(""" "Découvrez des assurances qui s'adaptent à vos nouvelles attentes...
    # https://t.co/O7PlaPzPvP https://t.co/T0U6Y7MLfV" """)
    # processing(""" "Ce qui est atypique chez nous, c'est que l'on a mis les paysans et les commerçants autour de la même table" 🎙 Clau… https://t.co/rKBp9SzQBM """)
    # processing(""" @sophie_merle @m6info La #spiruline est aussi une arme contre la #malnutrition !  Excellent complément alimentaire,… https://t.co/kOQxSh8vBT """)
    # processing(""" L’#éducation participe à l’amélioration du processus démocratique et à l’exercice de ses droits civiques. Nous mili… https://t.co/8E6YHIg01B """)
    # processing(""" Courir dimanche ? Oui au #Trail du four à chaux à #Nandy ! https://t.co/WFOlDph4R3 #scleroseenplaques @LaRep77… https://t.co/8I5yqDk3Tj """)
    # processing(""" [Chiffres-Clé du jour] 2 270 000 m3 de capacité de stockage d'eau recyclée, 12,5 km de canalisations et 4 000 hecta… https://t.co/M2zHNVwpNs """)
    # processing(""" "ACC
    # @assocoeurcouleur    
    # #lavoixdesrares

    # Plateforme d'expertise Maladies Rares Paris-Sud
    # @RaresParisSud

    # #CaféMR… https://t.co/3rEXa1KoRR" """)
    # processing(""" Tarbes : la navette gratuite du centre-ville se renverse, 3 blessés légers https://t.co/XFGVq17XIE """)
    # processing(""" Le Germoir🌱 weekend de #coconstruction pour les #bénévoles dirigeants + salarié.e.s @e_graine venu.e.s de toute la… https://t.co/zf6MJzzt3t """)
    # processing(""" Les #femmes contribuent de manière significative à la mise en œuvre de l’« Agenda 2030 » et à l’atteinte de ses 17… https://t.co/ed8mDxoeFS """)