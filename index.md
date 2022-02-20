---
layout: page
---

<center>
<br/>
<img width="30%" src="/assets/img/profile.jpeg" style="border-radius: 50%;">
<h2>Paul Bricman</h2>
</center>

I'm a Romanian-born Netherlands-based student exploring ways of augmenting human cognition using AI. On the surface, this happens by designing tiny new primitives, mechanics, and affordances which symbiotically bring together minds and machines. On a deeper level, this happens by putting together a cognitive infrastructure: a patchwork of [building blocks](/thoughtware) which together enable a rich combinatorial space of thought patterns, both organic and artificial, both individual and collective. My work on the thoughtware stack is made possible by a handful of generous [sponsors](/sponsors).

Outside thoughtware engineering, I'm learning how to create things using analog materials (e.g. paper, ink) and subjecting myself to a prolonged culture shock by learning Mandarin. I love the sublime feeling of peeking into awe-inspiring worlds while reading fiction, and I'm trying my best to marry the effectiveness of habits with the qualities of intention and presence. To share my reflections in a more structured format, I'm writing [one short article per week](/reflections).

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
- [**lifelong learning**](/lifelong-learning): planning a gap year curriculum
- [**blogroll**](/blogroll.opml): feeds I follow
- [**playlist**](/playlist): so you're curious what Romanian music sounds like
