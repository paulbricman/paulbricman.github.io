---
layout: page
---

## writing [(rss)](/reflections/feed.xml)

Here's a somewhat representative sample of what I spend my time thinking about. While the timestamp format might come across as pretentious, I found that it constantly reminds me of two things. First, that I should use my time here wisely. Second, that we each have our own unique timeline -- comparing my work to that of seasoned PhDs and industry veterans is counterproductive, if anything. Hope you enjoy these, and feel free to share your comments.

<div class="posts" id="Blog">
    <ul>
        {% assign reflections = site.reflections | sort: 'age' %}
        {% for reflection in reflections reversed %}

        {% assign age_split = reflection.age | round: 2 | split: "." %}
        {% assign integral = age_split[0] %}
        {% assign fractional = age_split[1] | append: "00" | truncate: 2, "" %}

        <li>
            <a href="{{ site.baseurl }}{{ reflection.url }}">{{ reflection.title }}</a>{{integral}}.{{fractional}}&#160;YRS
        </li>
        {% endfor %}
    </ul>

</div>
