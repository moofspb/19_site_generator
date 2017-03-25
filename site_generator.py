import os
import json
import markdown
from jinja2 import Environment, FileSystemLoader


def load_config(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as handler:
        return json.load(handler)


def get_titles(config):
    return [i for i in config['topics']]


def get_articles(config):
    return [i for i in config['articles']]


def load_markdown(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as handler:
        return handler.read()


def create_dir_for_html(article_path):
    if not os.path.exists(article_path):
        os.makedirs(article_path)


def markdown_to_html(md_data):
    return markdown.markdown(md_data)


def render_template(template_path, context):
    path, filename = os.path.split(template_path)
    env = Environment(
        loader=FileSystemLoader(path or './'),
        auto_reload=True
    )
    template = env.get_template(filename)
    return template.render(context)


def write_generated_page(template):
    with open('site/index.html', 'w') as f:
        f.write(template)


# print(get_titles(load_config('config.json')))
topics = get_titles(load_config('config.json'))
articles = get_articles(load_config('config.json'))
context = {
    'topics': topics,
    'articles': articles
}

create_dir_for_html('site')
write_generated_page(render_template('templates/main.html', context))
# print(load_config('config.json'))
# print(markdown_to_html(load_markdown('articles/0_tutorial/8_cli.md')))
"""
TODO:
make main page template (main.html)
make article page template

In site_generator.py:
function "
"""