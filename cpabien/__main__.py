"""Scrap cpabien."""

import sys
import requests
import shutil
from .helper import downloadTorrentForInput, getDlUrl, cleanInputString
from ..utils.yesno import query_oui_non


while True:
    sys.stdout.write("\nSaisir le nom d'un film et appuyer sur Enter.\n " +
    "(Appuyer directement sur Enter pour quitter)\n")
    inputString = raw_input().lower()

    if not(inputString):
        break

    results = downloadTorrentForInput(inputString)
    nbResults = len(results)
    hintStr = '\nVerifier que le titre est correctement orthographie. ' + \
                'Sinon, le film n\'est peut etre pas disponible.'
    if not(nbResults):
        print 'Pas de resultat pour "%s". ' % inputString + hintStr
    else:
        print '%g resultats trouves\n' % nbResults
        for resu in results:
            dlTitle = resu['title']
            ans = query_oui_non('%s - Est-ce le bon film?' % dlTitle)

            if ans:
                dlUrl = getDlUrl(resu['rawUrl'])

                req = requests.get(dlUrl, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
                if req.status_code == 200:
                    with open("%s.torrent" % cleanInputString(inputString), 'wb') as f:
                        req.raw.decode_content = True
                        shutil.copyfileobj(req.raw, f)

                    print 'Telechargement de "%s" lance!' % dlTitle
                    break
                else:
                    print 'Erreur! Le fichier n\'a pas pu etre telecharge.'
        else:
            print '\nFin des resultats pour "%s"! ' % inputString + hintStr
