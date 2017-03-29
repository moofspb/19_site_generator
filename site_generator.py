import os
import json
import copy
import markdown
from jinja2 import Environment, FileSystemLoader


SITE_DIR = 'site/'
ARTICLE_DIR = 'articles/'
MAIN_PAGE = 'index.html'
CONFIG = 'config.json'


def load_config(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as handler:
        return json.load(handler)


def load_markdown(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as handler:
        return handler.read()


def create_dir_for_html(path):
    if not os.path.exists(os.path.split(path)[0]):
        os.makedirs(os.path.split(path)[0])


def markdown_to_html(path_to_md):
    return markdown.markdown(path_to_md)


def get_html_article_path(md_path):
    article_path = os.path.splitext(md_path)[0]
    return '{}.html'.format(article_path)


def create_template(template_path):
    path, filename = os.path.split(template_path)
    env = Environment(
        loader=FileSystemLoader(path or './'),
        auto_reload=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env.get_template(filename)


def change_articles_paths(config):
    html_config = copy.deepcopy(config)
    for article in html_config['articles']:
        article['source'] = get_html_article_path(article['source'])
    return html_config


def render_main_page(context, template_path='templates/main.html'):
    template = create_template(template_path)
    return template.render(config=context)


def render_article_page(article_info, template_path='templates/article.html'):
    template = create_template(template_path)
    article_content = markdown_to_html(load_markdown(ARTICLE_DIR + article_info['source']))
    article_context = {
        'title': article_info['title'],
        'source': article_info['source'],
        'content': article_content
        }
    return template.render(config=article_context)


def write_generated_page(filepath, template):
    with open(filepath, 'w') as f:
        f.write(template)


if __name__ == '__main__':
    config_md_path = load_config(CONFIG)
    config_html_path = change_articles_paths(config_md_path)
    main_page_path = SITE_DIR + MAIN_PAGE
    for article in config_html_path['articles']:
        create_dir_for_html(SITE_DIR + article['source'])
    create_dir_for_html(SITE_DIR)
    write_generated_page(main_page_path, render_main_page(config_html_path))
    for article in config_md_path['articles']:
        article_dir = SITE_DIR + get_html_article_path(article['source'])
        write_generated_page(article_dir, render_article_page(article))
