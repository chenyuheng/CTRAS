import sqlite3
conn = sqlite3.connect('db.db')

c = conn.cursor()

# drop and Create table
c.execute("drop table if exists diff_txt;")
c.execute("drop table if exists diff_img;")
c.execute("drop table if exists cluster_txt")
c.execute("drop table if exists cluster_img")
c.execute("drop table if exists cluster_combine")
c.execute("drop table if exists top_txt")
c.execute("drop table if exists top_img")
c.execute('''CREATE TABLE diff_txt
             (app text, duplicate_tag text, diff_sentence text, diff_sentence_index text, report_id text)''')

c.execute('''CREATE TABLE diff_img
             (app text, duplicate_tag text, diff_sentence text, diff_sentence_index text, report_id text)''')

c.execute('''CREATE TABLE cluster_txt
             (app text, duplicate_tag text, diff_sentence text, diff_sentence_index text, report_id text,cluster_id text)''')
c.execute('''CREATE TABLE cluster_img
             (app text, duplicate_tag text, diff_sentence text, diff_sentence_index text, report_id text,cluster_id text)''')
c.execute('''CREATE TABLE cluster_combine
             (app text, duplicate_tag text, cluster_tag text, report_id text, cluster_id_txt text, cluster_id_img text)''')

c.execute('''CREATE TABLE top_txt
             (app text, duplicate_tag int, cluster_tag int, txts text)''')
c.execute('''CREATE TABLE top_img
             (app text, duplicate_tag text, cluster_tag text, report_id text, cluster_id_txt text, cluster_id_img text, txts_img)''')


# Save (commit) the changes
conn.commit() 

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
