import os
from .renderer import md
from .blog import title, date, description
from datetime import datetime


class Post(object):
    def __init__(self, path, name):
        self.name = name

        with open(path) as f:
            self.content = f.read()

    def date(self):
        return datetime.strptime(date(self.content), '%B %d, %Y')

    def render(self):
        return md.render(self.content)

    def title(self):
        return title(self.content)

    def description(self):
        return md.render(description(self.content))


class Posts:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.posts = os.listdir(self.path)

    def __getitem__(self, index):
        if index >= len(self.posts):
            raise IndexError('Index out of range')

        if self.posts[index].endswith('.md'):
            post = Post(self.path + '/' + self.posts[index], self.posts[index][:-3])
            return post

    def sorted(self):
        return sorted(self, key=lambda p: p.date(), reverse=True)

    def get(self, name):
        for post in self:
            if post.name == name:
                return post
