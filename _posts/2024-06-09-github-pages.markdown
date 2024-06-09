---
layout: post
title:  "GitHub pages"
date:   2024-06-09 21:00:00 +0200
categories: code
---

This website existed a long time ago, and was composed by the following elements:

* Twitter bootstrap
* [nanoc](https://nanoc.app/) static website generator
  
Well, at some point you have to keep your components updated and the obvious happened ... I didn't and wasn't able to publish easily contents as I was using the first bootstrap version and updating was something I didn't want to do, for no valid reason.

Also, I would need to have nanoc site content generator installed to publish something new.

I left it rotting for years because of it and at some point my VPS disappeared and so did the code. Well, I searched for a quite convenient solution and doing so, stubled on [GitHub Pages](https://pages.github.com/). Here's what I did to get this site running again, without much hassle.

_This is going to be inspired by documentation pages_

# Basic hosting

1. Head over to GitHub and create a new public repository named username.github.io, where username is your username (or organization name) on GitHub.
2. {% highlight bash %}git clone https://github.com/username/username.github.io{% endhighlight %}
3. Add some content and push it there with the first commit:
{% highlight bash %}git add --all
git commit -m "Initial commit"
git push -u origin main{% endhighlight %}

You'll get your content available directly at _username.github.io_. That's it.

Adding content isn't harder than a commit.

# Using a custom domain

Well, I wouldn't mind using a github.io fqdn, but I own a domain name so, let's use it.

Go to your domain registrar (I use [EuroDNS](https://www.eurodns.com)) and configure the following records:

{% highlight dns %}* in CNAME b3nj.github.io.

@ in CNAME b3nj.github.io.{% endhighlight %}

I would rather recommand this option instead of configuring A and AAAA records, at least the records will be updated.

Then:

* On GitHub, navigate to your site's repository.
* Under your repository name, click  Settings. If you cannot see the "Settings" tab, select the  dropdown menu, then click Settings.
* Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline. In the "Code and automation" section of the sidebar, click  Pages.
* Under "Custom domain", type your custom domain, then click Save.

# Securing pages with HTTPS

That's easy:
* On GitHub, navigate to your site's repository.
* Under your repository name, click  Settings. If you cannot see the "Settings" tab, select the  dropdown menu, then click Settings.
* Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.
* In the "Code and automation" section of the sidebar, click  Pages.
* Under "GitHub Pages," select Enforce HTTPS.

# Jekyll

What's awesome is that you can use [Jekyll](https://jekyllrb.com/) static website generator in your website and GitHub will automatically build it using GitHub actions and represent it ... it's quite [well documented](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll).

In your local repository, launch the Jekyll init command:

{% highlight bash %}
jekyll new --skip-bundle .
{% endhighlight %}

Then:
* Open the Gemfile that Jekyll created.
* Add "#" to the beginning of the line that starts with gem "jekyll" to comment out this line.
* Add the github-pages gem by editing the line starting with # gem "github-pages". Change this line to:
{% highlight bash %}gem "github-pages", "~> GITHUB-PAGES-VERSION", group: :jekyll_plugins{% endhighlight %}
* Replace GITHUB-PAGES-VERSION with the latest supported version of the github-pages gem. You can find this version here: "Dependency versions."
The correct version Jekyll will be installed as a dependency of the github-pages gem.
* Save and close the Gemfile.
* From the command line, run bundle install.

Then you're good to go ... Have fun learning how to use [Jekyll](https://jekyllrb.com/).