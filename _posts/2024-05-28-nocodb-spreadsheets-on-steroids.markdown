---
layout: post
title:  "nocodb, spreadsheets on steroids"
date:   2024-05-28 21:00:00 +0200
categories: code
---

Searching to migrate a complex excel workbook with loads of intelligence to something web based, easily developpable ...
Asked a colleague what he thought might be a good candidate to do this and pointed me out to [nocodb](https://nocodb.com/).

Here's how they sell it:
# Build Databases As Spreadsheets : No-Coding Required
NocoDB allows building no-code database solutions with ease of spreadsheets.
Bring your own database or choose ours! Millions of rows? Not a problem.
Your Data. Your rules. You are in control.

Wow.

I did a crash course using their [documentation](https://docs.nocodb.com/getting-started/self-hosted/installation/) for a brainless setup using docker and a SQLite backend.

Basically it's this : 
{% highlight bash %}
docker run -d --name nocodb \
-v "$(pwd)"/nocodb:/usr/app/data/ \
-p 8080:8080 \
nocodb/nocodb:latest
{% endhighlight %}

Then fired my browser to localhost on port 8080.

Created a database, several tables and linked them very easily in a super neat interface.
Then well, realized that I can't do automatic calculation and behavioral as I'd like.
However it has awesome "views" that actually present the spreadsheets in a different way, making them less annoying and probably motivating people to fill them. They can be presented as [Grids](https://docs.nocodb.com/views/view-types/grid), [Forms](https://docs.nocodb.com/views/view-types/form), [Gallery](https://docs.nocodb.com/views/view-types/gallery), [kanban](https://docs.nocodb.com/views/view-types/kanban) and [calendar](https://docs.nocodb.com/views/view-types/calendar). 

It's freaking awesome.