---
title: IIIF Consortium
id: consortium
layout: spec
---

## The IIIF Consortium

The IIIF Consortium (IIIF-C) was formed in [June 2015][news] to provide steering and sustainability to the IIIF community by signing a [Memorandum of Understanding][mou] in Oxford, England.  The Consortium provides ongoing oversight for the development of IIIF technologies and the growth of the community. Letters of support from the IIIF-C for IIIF-related grant applications may be requested according to the [IIIF Support for Grant Proposals policy][support-policy]. Consortium finances are managed through the [Council on Library and Information Resources][clir].



## Staff

Sheila Rabun  
IIIF Community and Communications Officer  
srabun@iiif.io



## Members

<ul>
{% for i in site.data.institutions %}
    {% if i.iiifc %}
  <li>
      {% if i.uri %}<a href="{{ i.uri }}">{% endif %}
        {{ i.name }}
      {% if i.uri %}</a>{% endif %}
  </li>
    {% endif %}
{% endfor %}
</ul>

[mou]: /community/consortium/mou/
[news]: /news/2015/06/17/iiif-consortium/
[clir]: http://clir.org/
[support-policy]: /community/consortium/policy/support
