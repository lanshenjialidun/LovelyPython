from gettext import GNUTranslations
import k_config
import k_utils

class KTranslations(GNUTranslations):

    def ugettext(self, message):
        missing = object()
        tmsg = self._catalog.get(message, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.ugettext(message)
            return unicode(message)
        if not isinstance(tmsg,unicode):
            if k_config.output_encoding:
                tmsg = unicode(tmsg,'utf-8').encode(k_config.output_encoding)
        return tmsg

