

Zones

URI pattern:  {scheme}://{host}{/prefix}/{identifier}/zone/{name}.json

{
  "@id": "mandatory-uri",
  "@type": "sc:Zone",
  "label": "optional label",
  "height": 1200,           // mandatory
  "width": 800,             // mandatory

  // other fields for zone manipulation
  "viewingOrientation": 270,
  "viewingHint": "foldout",

  "images": [ ... ],
  "otherContent": [ ... ]
}

Then aggregate them in an AnnotationList referenced from otherContent from the Canvas that it is associated with.

