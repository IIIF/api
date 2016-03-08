---
title: IIIF Consortium
id: consortium
categories: [pages]
layout: spec
---

## The IIIF Consortium

The IIIF Consortium was formed in [June 2015][news] to provide steering and sustainability to the IIIF community by signing a [Memorandum of Understanding][mou] in Oxford, England.  The Consortium will provide ongoing oversight for the development of IIIF technologies and managing the growth of the community.

## Staff

The Consortium is currently in the process of hiring its first full-time staff member, and manages its finances through the [Council on Library and Information Resources][clir]

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




[mou]: mou/
[news]: /news/2015/06/17/iiif-consortium/
[clir]: http://clir.org/