#!/usr/bin/env python

"""survivor_flair.py: Ascertain suvivor subreddit flair stats."""

__author__ = "Carolyn Gerakines"
__copyright__ = "Copyright 2014, Carolyn Gerakines"
__credits__ = ["Carolyn Gerakines"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Carolyn Gerakines"

import praw
 
USER_AGENT = 'SurvivorFlair/0.1.0 (+https://github.com/Chouette4u/survivor_flair)'

r = praw.Reddit(USER_AGENT)
r.login('xxxx', 'xxxx')
sr = 'survivor'
subreddit = r.get_subreddit(sr)

individuals = [
    'Carolyn',
    'Dan',
    'Hali',
    'Jenn',
    'Joaquin',
    'Joe',
    'Kelly',
    'Lindsey',
    'Max',
    'Mike',
    'Nina',
    'Rodney',
    'Shirin',
    'Sierra',
    'So',
    'Tyler',
    'Vince',
    'Will'
]

tribes = [
    'White Collar',
    'No Collar',
    'Blue Collar'
]

tribe_membership = {
    'Carolyn': 'White Collar',
    'Dan': 'Blue Collar',
    'Hali': 'No Collar',
    'Jenn': 'No Collar',
    'Joaquin': 'White Collar',
    'Joe': 'No Collar',
    'Kelly': 'Blue Collar',
    'Lindsey': 'Blue Collar',
    'Max': 'White Collar',
    'Mike': 'Blue Collar',
    'Nina': 'No Collar',
    'Rodney': 'White Collar',
    'Shirin': 'White Collar',
    'Sierra': 'Blue Collar',
    'So': 'White Collar',
    'Tyler': 'White Collar',
    'Vince': 'No Collar',
    'Will': 'No Collar'
}

 
def write_out(dataset, filename, deep, filter):
    with open(filename, 'w') as f:
        if deep:
            f.write("Flair,Pregame,Player,Other\n")
            for player, css_classes in dataset.items():
                if filter is not None and player not in filter:
                    continue
                pregame_v = 0
                player_v = 0
                other_v = 0
                if 'pregame' in css_classes:
                    pregame_v = css_classes['pregame']
                if 'player' in css_classes:
                    player_v = css_classes['player']
                if 'UNDEFINED' in css_classes:
                    other_v = css_classes['UNDEFINED']
                f.write("%s,%s,%s,%s\n" % (player, pregame_v, player_v, other_v))
        else:
            for key, count in dataset.items():
                if filter is not None and key not in filter:
                    continue
                f.write("%s,%s\n" % (key, count))

def normalized_css_class(input):
    input = input or 'UNDEFINED'
    if input.lower() == 'pregame':
        return 'pregame'
    if input.lower() == 'player':
        return 'player'
    return 'UNDEFINED'

def normalized_tribe(input):
    if input in tribes:
        return input
    if input in tribe_membership:
        return tribe_membership[input]
    return 'UNDEFINED'

def main():
    users = {}
    css_classes = {}
    texts = {}
    combined = {}
    tribe_agg = {}
    total = 0

    for flair in subreddit.get_flair_list(limit = None):
        user = flair['user'] or 'UNDEFINED'
        css_class = normalized_css_class(flair['flair_css_class'])
        flair_text = flair['flair_text'] or 'UNDEFINED'
        tribe = normalized_tribe(flair_text)

        if user not in users:
            users[user] = 0
        if css_class not in css_classes:
            css_classes[css_class] = 0
        if flair_text not in texts:
            texts[flair_text] = 0
        if tribe not in tribe_agg:
            tribe_agg[tribe] = {}
        if css_class not in tribe_agg[tribe]:
            tribe_agg[tribe][css_class] = 0
        if flair_text not in combined:
            combined[flair_text] = { }
        if css_class not in combined[flair_text]:
            combined[flair_text][css_class] = 0
 
        texts[flair_text] += 1 
        css_classes[css_class] += 1 
        users[user] += 1
        combined[flair_text][css_class] += 1
        tribe_agg[tribe][css_class] += 1
        total += 1

        if total % 1000 == 0:
            print "Processed", total, "records."

    # write_out(users, "users.csv", False, None)
    # write_out(users, "users_filtered.csv", False, current_flair_text)
    # write_out(css_classes, "css_classes.csv", False, None)
    # write_out(css_classes, "css_classes_individual.csv", False, current_flair_text)
    write_out(tribe_agg, "tribes.csv", True, tribes)
    write_out(texts, "texts.csv", False, None)
    write_out(texts, "texts_individuals.csv", False, individuals)
    write_out(texts, "texts_tribes.csv", False, tribes)
    write_out(combined, "combined.csv", True, None)
    write_out(combined, "combined_individuals.csv", True, individuals)
    write_out(combined, "combined_tribes.csv", True, tribes)
    write_out(combined, "combined_season.csv", True, individuals + tribes)
 
if __name__ == "__main__":
    main()
