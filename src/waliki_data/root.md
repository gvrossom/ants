### Development, Yeah

Fonctions utilitaires django.core.urlresolvers¶
reverse()¶

Si vous avez besoin d’utiliser quelque chose de semblable à la balise de gabarit url dans votre code, Django fournit la fonction suivante :

reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)[source]¶

viewname peut être une chaîne contenant le chemin Python vers l’objet de vue, un nom de motif d’URL ou l’objet de vue lui-même. Par exemple, étant donné l’url suivante :

from news import views

url(r'^archive/$', views.archive, name='news-archive')

vous pouvez utiliser indifféremment les appels suivants pour obtenir l’URL :

# using the named URL
reverse('news-archive')

# passing a callable object
# (This is discouraged because you can't reverse namespaced views this way.)
from news import views
reverse(views.archive)

Si l’URL accepte des paramètres, vous pouvez les transmettre dans args. par exemple :

from django.core.urlresolvers import reverse

def myview(request):
    return HttpResponseRedirect(reverse('arch-summary', args=[1945]))

Vous pouvez aussi transmettre kwargs au lieu de args. Par exemple :

>>> reverse('admin:app_list', kwargs={'app_label': 'auth'})
'/admin/auth/'

Il n’est pas possible de passer à la fois args et kwargs à reverse().

Si aucune correspondance n’est trouvée, reverse() génère une exception NoReverseMatch.

La fonction reverse() peut résoudre une large palette de motifs d’expressions régulières correspondant à des URL, mais pas tous. La principale restriction actuellement est que le motif ne peut pas contenir différents choix possibles indiqués par la barre verticale ("|"). De tels motifs peuvent sans problème être utilisés pour résoudre des URL entrantes et faire appel à la vue correspondante, mais il n’est pas possible de les utiliser pour effectuer des résolutions inverses.

Le paramètre current_app vous permet de donner une indication au résolveur pour signaler l’application à laquelle appartient la vue en cours d’exécution. Ce paramètre current_app est employé comme indication pour résoudre des espaces de noms d’application en URL d’instances spécifiques d’application, en accord avec la stratégie de résolution d’URL avec espaces de noms.

The urlconf argument is the URLconf module containing the URL patterns to use for reversing. By default, the root URLconf for the current thread is used.