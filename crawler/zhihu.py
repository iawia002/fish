# coding=utf-8

import requests
from bs4 import BeautifulSoup

import utils.db
from db.sa import Session
from models import Article, UpdateInfo


'''
<div class="zm-editable-content clearfix">
    <img
        src="//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg"
        data-rawwidth="746"
        data-rawheight="823"
        class="origin_image zh-lightbox-thumb lazy"
        width="746"
        data-original="https://pic3.zhimg.com/v2-150ecb41e823c5f650058ab181ce1286_r.png"
        data-actualsrc="https://pic3.zhimg.com/v2-150ecb41e823c5f650058ab181ce1286_b.png"
    >
</div>
'''


def img_with_data_original(tag):
    if tag.name == 'img' and tag.has_attr('data-original') \
            and set(['origin_image', 'lazy']).issubset(set(tag['class'])):
        return tag


def imgs(url):
    ZH_API = 'https://www.zhihu.com/node/QuestionAnswerListV2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8'  # noqa
    }
    post_headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_headers.update(headers)
    url = url.split('?')[0]
    if url[-1] == '/':
        question_id = url.split('/')[-2]
    else:
        question_id = url.split('/')[-1]
    html_text = requests.get(
        url,
        headers=headers,
    ).text
    soup = BeautifulSoup(html_text, 'html.parser')
    answer_num = int(soup.find(id='zh-question-answer-num')['data-num'])
    title = soup.title.string
    page = answer_num / 10
    if answer_num % 10 != 0:
        page += 1
    answers = []
    for item in xrange(page):
        data = (
            'method=next&params='
            '{{"url_token":{question_id},"pagesize":10,"offset":{offset}}}'
        ).format(
            question_id=question_id,
            offset=item*10
        )
        r = requests.post(ZH_API, headers=post_headers, data=data)
        answers.extend(r.json()['msg'])
    img_list = []
    for answer in answers:
        soup = BeautifulSoup(answer, 'html.parser')
        imgs = soup.find_all(img_with_data_original)
        img_list.extend([img['data-original'] for img in imgs])
    return {'title': title, 'images': img_list}


def jike():
    '''
    即刻：知乎热门钓鱼帖
    '''
    JK_API = (
        'https://app.jike.ruguoapp.com/1.0/topics/showDetail?'
        'topicId={topic_id}'
    ).format(topic_id='57281cf75f0ba71200ffde92')
    results = requests.get(
        JK_API,
    )
    if results.status_code != 200:
        return
    results = results.json()
    messages = results['messages']
    messages_url = [message['linkUrl'] for message in messages]
    session = Session()
    update_record = session.query(UpdateInfo).first()
    already_existing = update_record.content
    # 用这次的 URL 列表减去已经存在的 URL 列表，得到这次多出来的 URL
    need_update = list(set(messages_url) - set(already_existing))
    for url in need_update:
        article = utils.db.get_or_create(session, Article, source=url)
        result = imgs(url)
        article.content = result['images']
        article.title = result['title']
        article.image_num = len(result['images'])
        session.add(article)
    total = []
    total.extend(already_existing)
    total.extend(need_update)
    update_record.content = total
    session.add(update_record)
    session.commit()
    session.close()
    return need_update


def update_manually(url):
    session = Session()

    # 更新文章
    article = utils.db.get_or_create(session, Article, source=url)
    result = imgs(url)
    article.content = result['images']
    article.title = result['title']
    article.image_num = len(result['images'])

    # 更新记录
    update_record = session.query(UpdateInfo).first()
    total = []
    total.extend(update_record.content)
    if url not in total:
        total.append(url)
    update_record.content = total

    session.add(article)
    session.add(update_record)
    try:
        session.commit()
    except:
        session.rollback()
        raise
    session.close()


if __name__ == '__main__':
    __import__('ipdb').set_trace()
