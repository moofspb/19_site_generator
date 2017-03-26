import os
import json
import markdown
from jinja2 import Environment, FileSystemLoader


SITE_DIR = 'site/'
ARTICLE_DIR = 'articles/'


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
    return '{}{}.html'.format(SITE_DIR, article_path)


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
    for article in config['articles']:
        article['source'] = get_html_article_path(article['source'])
    return config


def render_main_page(context, template_path='templates/main.html'):
    template = create_template(template_path)
    return template.render(config=context)


def render_article_page(article, template_path='templates/article.html'):
    template = create_template(template_path)
    article_context = {
        'title': article['title'],
        'source': article['source'],
        'content': markdown_to_html(load_markdown(article['source']))
        }
    return template.render(config=article_context)


def write_generated_page(filepath, template):
    with open(filepath, 'w') as f:
        f.write(template)


if __name__ == '__main__':
    config_md_path = load_config('config.json')
    config_html_path = change_articles_paths(config_md_path)
    main_page_path = SITE_DIR + 'index.html'
    for article in config_html_path['articles']:
        create_dir_for_html(article['source'])
    create_dir_for_html(SITE_DIR)
    write_generated_page(main_page_path, render_main_page(config_html_path))
    for article in config_md_path['articles']:
        write_generated_page(article['source'], render_article_page(article))

    """
    TODO:
    1. render_article_page: fix get article content (line 66)
    2. fix site/site in articles links in index.html
    3. create function generate_site



    main_template = 'templates/main.html'
    article_template = 'templates/article.html'
    config = load_config('config.json')
    create_dir_for_html('site')
    context = {
        'topics': [topic for topic in config['topics']],
        'articles': [article for article in config['articles']]
    }
    write_generated_page('site/index.html', (render_template(main_template, context)))
    write_generated_page('site/')
    # print(get_titles(load_config('config.json')))
    topics = get_titles(load_config('config.json'))
    articles = get_articles(load_config('config.json'))
    html_from_md = markdown_to_html(load_markdown('articles/0_tutorial/8_cli.md'))
    context = {
        'topics': topics,
        'articles': articles,
        'article': html_from_md
    }

    create_dir_for_html('site')
    # write_generated_page('site/index.html', (render_template('templates/main.html', context)))
    # print(load_config('config.json'))

    html_template = render_template('templates/article.html', context)

    write_generated_page('site/8_cli.html', html_template)

    # html_article = markdown_to_html(load_markdown('articles/0_tutorial/8_cli.md'))
    # write_generated_page('site/8_cli.html', html_article)
    """

