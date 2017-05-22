"""Scrap cpabien."""

import sys
from .helper import search_torrents, dl_file
from ..utils.yesno import query_oui_non
from ..utils.strings import clean_str


# One iteration = one search
while True:

    # Ask user for input
    sys.stdout.write("\nSaisir le nom d'un film et appuyer sur Enter.\n " +
    "(Appuyer directement sur Enter pour quitter)\n")
    input_str = raw_input().lower()

    # If blank, exit the program
    if not(input_str):
        break

    # Run the search
    results = search_torrents(input_str)
    nb_results = len(results)

    hint_str = '\nVerifier que le titre est correctement orthographie. ' + \
                'Sinon, le film n\'est peut etre pas disponible.'

    # No results
    if not(nb_results):
        print 'Pas de resultat pour "%s". ' % input_str + hint_str

    # Results
    else:
        print '%g resultats trouves\n' % nb_results

        # Loop through the results, ask to pick one
        for resu in results:
            dl_title = resu['title']
            ans = query_oui_non('%s - Est-ce le bon film?' % dl_title)

            # Download the file
            if ans:
                if dl_file(resu['dl_url'], clean_str(input_str)):
                    print 'Telechargement de "%s" lance!' % dl_title
                else:
                    print 'Erreur! Le fichier n\'a pas pu etre telecharge.'
                break

        # End of results, nothing was picked
        else:
            print '\nFin des resultats pour "%s"! ' % input_str + hint_str
