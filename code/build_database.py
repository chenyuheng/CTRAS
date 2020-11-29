import sqlite3
conn = sqlite3.connect('db.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE diff_txt
#              (app text, duplicate_tag text, diff_sentence text, diff_sentence_index text, report_id text)''')

c.execute('''CREATE TABLE cluster_txt
             (app text, duplicate_tag text, diff_sentence text, diff_sentence_index text, report_id text,cluster_id text)''')


# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()