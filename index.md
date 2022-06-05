---
layout: page
---

<center>
<br/>
<img width="30%" src="/assets/img/profile.jpeg" style="border-radius: 50%;">
<h2>Paul Bricman</h2>
</center>

> **Note**: I'm moving my work to a different space. Read more [here](/reflections/near-future-plans).

I'm a Romanian-born Netherlands-based student exploring synergies between the organic and the artificial. At peak idealism, this means bringing together minds and machines into a transhumanist symbiosis. Concretely, however, it currently means putting together proof-of-concept tools based on off-the-shelf ML models or, more recently, tiny experimental investigations into aligning AI to human intentions. My work is made possible by a handful of generous [sponsors](/sponsors).

Outside thoughtware, I'm currently learning Chinese and representational drawing, with varying degrees of success. I love visiting other worlds through fiction, and I'm trying my best to combine the effectiveness of habits with the quality of agency. To share my thoughts in a more structured format, I'm writing one short article per week.

### recent writing [(see all)](/reflections)

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

### recent projects [(see all)](/thoughtware)

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

- [**bookshelf**](/bookshelf): what I've been reading
- [**infinite skills**](/infinite-skills): what I'm pursuing outside thoughtware
- [**blogroll**](/blogroll.opml): feeds I follow
