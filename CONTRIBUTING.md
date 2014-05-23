# Guidelines

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

* *color* ~~*colour*~~
* *gray* ~~*grey*~~

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
