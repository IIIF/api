---
title: IIIF Consortium
id: consortium
layout: spec
---

## The IIIF Consortium

The IIIF Consortium (IIIF-C) was formed in [June 2015][news] in Oxford, England, to provide steering and sustainability for the IIIF community. The IIIF-C now comprises more than 40 Founding Members across the globe who have signed the IIIF-C [Memorandum of Understanding][mou], committing to support the growth and adoption of IIIF. IIIF-C provides continued support for adoption, experimentation, outreach, and a thriving community of libraries, museums, software firms, scholars, and technologists working with IIIF. For more information on the benefits and process for joining, please visit the [IIIF-C FAQ][iiifc-faq].


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
[iiifc-faq]: /community/consortium/faq
