---
layout: page
---

## reflections

(work in progress)

<div class="posts" id="Blog">
    <ul>
        {% assign reflections = site.reflections | sort: 'age' %}
        {% for reflection in reflections reversed %}
        <li>
            <a href="{{ site.baseurl }}{{ reflection.url }}">{{ reflection.title }}</a>{{ reflection.age }} YRS
        </li>
        {% endfor %}
    </ul>
</div>
