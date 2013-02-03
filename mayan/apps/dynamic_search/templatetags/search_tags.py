from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.translation import ugettext as _

from ..forms import SearchForm
from ..icons import icon_search, icon_advanced_search
from ..models import RecentSearch
from ..settings import RECENT_COUNT

register = Library()

# TODO: remove
@register.inclusion_tag('search_results_subtemplate.html', takes_context=True)
def search_form(context):
    context.update({
        'form': SearchForm(initial={'q': context.get('query_string', {}).get('q'), 'source': 'sidebar'}),
        'request': context['request'],
        'STATIC_URL': context['STATIC_URL'],
        'form_action': reverse('search'),
        'form_title': _(u'Search'),
        'submit_label': _(u'Search'),
        'submit_icon_famfam': 'zoom',
    })
    return context


@register.inclusion_tag('generic_subtemplate.html', takes_context=True)
def recent_searches_template(context):
    recent_searches = RecentSearch.objects.filter(user=context['user'])
    context.update({
        'request': context['request'],
        'STATIC_URL': context['STATIC_URL'],
        'side_bar': True,
        'title': _(u'recent searches (maximum of %d)') % RECENT_COUNT,
        'paragraphs': [
            u'<a href="%(url)s">%(icon)s%(text)s</a>' % {
                'text': rs,
                'url': rs.url(),
                'icon': icon_advanced_search.display_small() if rs.is_advanced() else icon_search.display_small(),
            } for rs in recent_searches
        ]
    })
    return context
