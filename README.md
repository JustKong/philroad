WikiPhil
========

A simple website that clicks on the first link in a Wikipedia article until:
a) it leads to the philosophy article;
b) it reaches a dead-end; or
c) it gets into an infinite loop.

Upon reaching any of these conclusions, it'll print out the path that it followed.

It follows xkcd's methodology, where we ignore all links that appear in parenthesis and in italics.