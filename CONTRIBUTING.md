# Guidelines

## Communication

Please use [iiif-discuss@googlegroups.com][mailto:iiif-discuss@googlegroups.com] for general discussion, questions and feedback on the documents.  This is to ensure that the entire community can see what is being, and has been discussed. Searching in github issues for answers to a question that has already been answered is much less convenient than reading through issues in a google group.  It is also to ensure that non-technical contributors have a chance to engage without feeling intimidated by the more code-oriented nature of github.

Please file issues in github for problems with the specifications or website.  One issue should be used per problem, so that we can work on them individually and either mark them as wontfix, defer, or close them when they're solved.  Please tag each specification issue with at least one of: `image`, `presentation`, `search`, `rest` or `auth` so it's easier to track.  If the issue is about the HTML, images, CSS or other part of the site, please tag it as `website`. Editors will assign who is responsible for the issue, and add the issue to the appropriate milestone.  

The editors take responsibility for ensuring that comments and feedback on iiif-discuss are turned into issues.  Please check that your issue discussed on the email list hasn't already been added to avoid `duplicate`s.

Pull requests are welcome.  Please read on for how to contribute directly.

## Making Changes

Please do not work on master. Submit pull requests from branches, and [squash your commits][squash] prior. For example:

```
 $ git checkout master 
 $ git checkout pull # make sure you're up to date
 $ git checkout my_cool_branch
 $ git rebase -i master
```

and follow the prompts. Generally you'll `pick` the first commit and `squash` the rest into it.

## English

Specs are written in American English. Use:

* *color* not ~~*colour*~~
* *gray* not ~~*grey*~~

## Markdown

Use the [Kramdown syntax][kram].

## Images

Images must be PNG.

## Front Matter

 * Specs use `tags`, news and announements (`_posts`) use `categories`.
 * Look at previous posts and specs to determine what tags/categories to use. 
 * Anything in the `api` directory (and subdirectories thereof) must include the `spec-doc` tag.
 * News posts must include:

    * title
    * author
    * tags
    * layout: post

    and may include an excerpt.

[kram]: http://kramdown.gettalong.org/syntax.html
[squash]: http://lmgtfy.com/?q=Squash+git+commits
