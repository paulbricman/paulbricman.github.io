---
layout: page
---

## reflections [(rss)](/reflections/feed.xml)

For a long while now, my main channels for sharing ideas publicly were thoughtware write-ups and working notes. Unfortunately, thoughtware write-ups only contain ideas related to currently feasible tools for thought. "Currently feasible" is a quickly moving target and a function of our technical, social, and cultural context -- it's pretty arbitrary. Working notes, on the other hand, are highly unstructured, which makes them difficult to use as a medium for expressing complex thought. I hope these short semi-structured articles published weekly will help communicate the ideas I value most.

<div class="posts" id="Blog">
    <ul>
        {% assign reflections = site.reflections | sort: 'age' %}
        {% for reflection in reflections reversed %}

        {% assign age_split = reflection.age | round: 2 | split: "." %}
        {% assign integral = age_split[0] %}
        {% assign fractional = age_split[1] | append: "00" | truncate: 2, "" %}

        <li>
            <a href="{{ site.baseurl }}{{ reflection.url }}">{{ reflection.title }}</a>{{integral}}.{{fractional}} YRS
        </li>
        {% endfor %}
    </ul>
</div>
