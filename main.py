import feedparser
import pymysql

if __name__ == '__main__':
    con = pymysql.connect(host='localhost', user='root', passwd='punter89', db='spreadthejam')
    cursor = con.cursor()

    try:

        with con.cursor() as cur:

            cur.execute('SELECT * FROM feed_urls')

            rows = cur.fetchall()

            for row in rows:
                link = row[0]
                feed = feedparser.parse(link)
                for entry in feed.entries:
                    if 'title' in entry:
                        title = entry.title
                    else:
                        title = None

                    if 'link' in entry:
                        link = entry.link
                    else:
                        link = None

                    if 'author' in entry:
                        author = entry.author
                    else:
                        author = None

                    if 'published_parsed' in entry:
                        timeStruct = entry.published_parsed
                        published = str(timeStruct[0]) + "-" + str(timeStruct[1]) + "-" + str(timeStruct[2]) + " " + str(timeStruct[3]) + ":" + str(timeStruct[4]) + ":" + str(timeStruct[5])
                        print(published)
                    else:
                        published = None

                    if 'summary' in entry:
                        summary = entry.summary
                    else:
                        summary = None

                    if 'content' in entry:
                        content_value = entry.content[0].value
                    else:
                        content_value = None

                    if 'media_content' in entry:
                        #print(entry.media_content[0]['url'])
                        media_content_url = entry.media_content[0]['url']
                        media_content_type = entry.media_content[0]['type']
                        media_content_width = entry.media_content[0]['width']
                        media_content_height = entry.media_content[0]['height']
                        media_content_copyright = entry.media_copyright
                    else:
                        media_content_url = None
                        media_content_type = None
                        media_content_width = None
                        media_content_height = None
                        media_content_copyright = None

                    insert_query = """
                        INSERT INTO feed_item 
                            (title, link, author, published, summary, content_value, media_content_url, media_content_type, media_content_width, media_content_height, media_content_copyright) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """

                    val_tuple = (
                        title,
                        link,
                        author,
                        published,
                        summary,
                        content_value,
                        media_content_url,
                        media_content_type,
                        media_content_width,
                        media_content_height,
                        media_content_copyright
                    )

                    cursor.execute(insert_query, val_tuple)
                    con.commit()

    finally:
        con.close()
