import requests
from lxml import html


def handle_link(url, headers):
    response = requests.get(url, headers=headers)
    if response.ok:
        dom = html.fromstring(response.text)
        dom.make_links_absolute(url)
        new_title = dom.xpath("//h1[@class='hdr__inner']//text()")[0]
        new_reference = dom.xpath("//a[contains(@class, 'breadcrumbs__link')]//span//text()")[0]
        new_publication_datetime = dom.xpath("//span[contains(@class, 'js-ago')]//@datetime")[0]
        new_publication_datetime = new_publication_datetime.replace("T", " ")
        if new_publication_datetime.find("+") != -1:
            new_publication_datetime = new_publication_datetime[:new_publication_datetime.find("+")]  # удаление
            # информации с разницей во времени
        new_link = url
        new = {
            "new_title": new_title,
            "new_reference": new_reference,
            "new_publication_datetime": new_publication_datetime,
            "new_link": new_link
        }
        return new
