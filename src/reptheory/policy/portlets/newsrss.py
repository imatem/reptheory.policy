from logging import getLogger
import time

import feedparser
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from zope.interface import implements, Interface
from zope import schema

from DateTime import DateTime
from DateTime.interfaces import DateTimeError
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base


# Accept these bozo_exceptions encountered by feedparser when parsing
# the feed:
ACCEPTED_FEEDPARSER_EXCEPTIONS = (feedparser.CharacterEncodingOverride, )

# store the feeds here (which means in RAM)
FEED_DATA = {}  # url: ({date, title, url, itemlist})

logger = getLogger(__name__)

from plone.app.portlets.portlets.rss import RSSFeed
from plone.app.portlets.portlets.rss import Renderer
from plone.app.portlets.portlets.rss import IRSSPortlet
from plone.app.portlets.portlets.rss import Assignment


class NewsIRSSPortlet(IRSSPortlet):
    pass


class NewsAssignment(Assignment):
    implements(NewsIRSSPortlet)

    # portlet_title = u''

    # @property
    # def title(self):
    #     """return the title with RSS feed title or from URL"""
    #     feed = FEED_DATA.get(self.data.url, None)
    #     if feed is None:
    #         return u'RSS: '+self.url[:20]
    #     else:
    #         return u'RSS: '+feed.title[:20]

    # def __init__(self, portlet_title=u'', count=5, url=u"", timeout=100):
    #     self.portlet_title = portlet_title
    #     self.count = count
    #     self.url = url
    #     self.timeout = timeout


class NewsRSSFeed(RSSFeed):

    def _buildItemDict(self, item):
        link = item.links[0]['href']
        itemdict = {
            'title': item.title,
            'url': link,
            'summary': item.get('description', ''),
            # 'speaker': item.get('dc_speaker', ''),
            # 'institution': item.get('dc_institution', ''),
            # 'seminarytitle': item.get('dc_seminarytitle', ''),
            # 'location': item.get('dc_location', ''),
        }
        if hasattr(item, "updated"):
            try:
                itemdict['updated'] = DateTime(item.updated)
            except DateTimeError:
                # It's okay to drop it because in the
                # template, this is checked with
                # ``exists:``
                pass

        return itemdict


class NewsRenderer(Renderer):

    render_full = ZopeTwoPageTemplateFile('newsrss.pt')

    def _getFeed(self):
        """return a feed object but do not update it"""
        feed = FEED_DATA.get(self.data.url, None)
        if feed is None:
            # create it
            feed = FEED_DATA[self.data.url] = NewsRSSFeed(self.data.url, self.data.timeout)
        return feed

    @property
    def items(self):
        if self.data.count == 0:
            return self._getFeed().items
        return self._getFeed().items[:self.data.count]


class AddForm(base.AddForm):
    form_fields = form.Fields(NewsIRSSPortlet)
    label = _(u"Add News RSS Portlet")
    description = _(u"This portlet displays an News RSS feed.")

    def create(self, data):
        return NewsAssignment(portlet_title=data.get('portlet_title', u''),
                          count=data.get('count', 5),
                          url=data.get('url', ''),
                          timeout=data.get('timeout', 100))


class EditForm(base.EditForm):
    form_fields = form.Fields(NewsIRSSPortlet)
    label = _(u"Edit News RSS Portlet")
    description = _(u"This portlet displays an RSS feed.")
