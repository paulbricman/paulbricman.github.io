---
layout: page
---

<center>
<br/>
<img width="30%" src="/assets/img/profile.jpeg" style="border-radius: 50%;">
<h2>Paul Bricman</h2>
</center>

I'm a Romanian-born Netherlands-based student on a quest to extend the range of ways in which people can think. On the surface, this happens by designing new primitives, mechanics, and affordances which bring together the computational grandeur of machines and the fragile brilliance of minds in a momentary symbiosis of carbon and silicone. On a deeper level, this happens by deliberately laying the foundation of our cognitive infrastructure: a patchwork of composable building blocks which bring firm principles of engineering to the brittle land of human thought. My work on the thoughtware stack is made possible by a handful of generous [sponsors](/sponsors).

Outside thoughtware engineering, I'm learning how to create things using analog materials (e.g. paper, yarn) and subjecting myself to a prolonged culture shock by learning Mandarin. I love the sublime feeling of peeking into awe-inspiring worlds devised by authors with strong worldbuilding skills, and I'm trying my best to marry the effectiveness of routines, habits, and protocols, with the humane qualities of intention and presence. To share my reflections in a more structured format, I'm writing one short article per week.

### recent reflections [(see all)](/reflections)

<div class="posts" id="Blog">
    <ul>
        {% assign reflections = site.reflections | sort: 'age' | reverse %}
        {% for reflection in reflections limit:10 %}

        {% assign age_split = reflection.age | round: 2 | split: "." %}
        {% assign integral = age_split[0] %}
        {% assign fractional = age_split[1] | append: "00" | truncate: 2, "" %}

        <li>
            <a href="{{ site.baseurl }}{{ reflection.url }}">{{ reflection.title }}</a>{{integral}}.{{fractional}}&#160;YRS
        </li>
        {% endfor %}
    </ul>

</div>

### recent thoughtware [(see all)](/thoughtware)

<div class="posts" id="Blog">
    <ul>
        {% assign tools = site.thoughtware | sort | reverse %}
        {% for tool in tools limit:10 %}

        <li>
            <div style="font-weight: normal"><a href="{{ site.baseurl }}{{ tool.url }}">{{ tool.title | downcase }}</a>: {{ tool.description | downcase }}</div>
        </li>
        {% endfor %}
    </ul>

</div>

### miscellaneous

- [**bookshelf**](/bookshelf): "peeking into awe-inspiring worlds"
- [**infinite skills**](/infinite-skills): "learning how to create things", "learning Mandarin"
- [**blogroll**](/blogroll.opml): feeds I follow
- [**playlist**](/playlist): so you're curious what Romanian music sounds like
