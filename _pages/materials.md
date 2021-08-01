---
layout: page
---

## materials

I'm learning how to work with different analog materials by creating 100
artifacts using one of them, then moving on to the next. The goal is to go
from absolute beginner to modest amateur, with every creation being a
bite-sized lesson in tactility, patience, and fault tolerance. Currently
exploring paper.

<br/>

<div>
    {% for image in site.static_files reversed %} {% if image.path contains
    'materials' %}
    <img
      src="{{ site.baseurl }}{{ image.path }}"
      width="49.1%"
      style="border-style: solid"
    />&nbsp;
    {% endif %} {% endfor %}
  </div>
