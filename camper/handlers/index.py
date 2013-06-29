#encoding=utf8

from camper import BaseHandler
from ..base import BarcampView

class IndexView(BaseHandler):
    """an index handler"""

    template = "index.html"

    def get(self):
        """render the view"""
        barcamps = self.config.dbs.barcamps.find()
        barcamps = [BarcampView(barcamp, self) for barcamp in barcamps]
        return self.render( barcamps = barcamps )
    post = get

class Impressum(BaseHandler):
    """show the impressum"""

    template = "impressum.html"

    def get(self):
        """render the view"""
        return self.render()

class Datenschutzerklaerung(BaseHandler):
    """show the privacy policy"""

    template = "datenschutzerklaerung.html"

    def get(self):
        """render the view"""
        return self.render()

class Wettbewerbsbedingungen(BaseHandler):
    """show the rules"""

    template = "wettbewerbsbedingungen.html"

    def get(self):
        """render the view"""
        return self.render()

class Aufgabe(BaseHandler):
    """show the challenge"""

    template = "aufgabe.html"

    def get(self):
        """render the view"""
        return self.render()
