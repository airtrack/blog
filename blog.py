# -*- coding: utf-8 -*-

import user_agents
from post import get_posts_list, get_post_content
from flask import Flask, render_template, request

blog = Flask(__name__)
posts_dir = 'posts'

def is_mobile_request():
    ua = request.user_agent.string
    if ua and user_agents.parse(ua).is_mobile:
        return True
    else:
        return False

def get_mobile_prefix():
    return 'mobile_' if is_mobile_request() else ''

@blog.route('/')
def index():
    return render_template('index.html',
            mobile = get_mobile_prefix(),
            posts = get_posts_list(posts_dir))

@blog.route('/posts/<year>/<month>/<day>/<post_name>/')
def post(year, month, day, post_name):
    post_time = '-'.join((year, month, day))
    content = get_post_content(posts_dir, post_time, post_name)

    if content:
        return render_template('post.html',
                mobile = get_mobile_prefix(), title = post_name,
                time = post_time, content = content)
    else:
        return render_template('404.html'), 404

@blog.route('/about.html')
def about():
    return render_template('about.html', mobile = get_mobile_prefix())

@blog.route('/<css_file>.css')
def css(css_file):
    return blog.send_static_file(css_file + '.css')

@blog.route('/images/<image_file>')
def image(image_file):
    return blog.send_static_file('images/' + image_file)

@blog.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    blog.run(host = '127.0.0.1', port = 8080, debug = True)
