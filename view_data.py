import os
import sqlite3


# database.
data_folder = '/Users/johnmorris/arxiv-gpt/data/'
conn = sqlite3.connect(os.path.join(data_folder, 'database.db'))
cursor = conn.cursor()

def main():
    # Get 5 random authors
    cursor.execute("SELECT * FROM authors ORDER BY RANDOM() LIMIT 5")
    random_authors = cursor.fetchall()

    # Print the random authors
    print("Random Authors:")
    for author in random_authors:
        author_id, author_name = author
        print(f"Author ID: {author_id}")
        print(f"Author Name: {author_name}")

    # Get 5 random documents
    cursor.execute("SELECT * FROM documents ORDER BY RANDOM() LIMIT 5")
    random_documents = cursor.fetchall()

    # Print the random documents
    print("Random Documents:")
    for document in random_documents:
        doc_id, doc_data = document
        print(f"Document ID: {doc_id}")
        print(f"Document Data: {doc_data}")
        print()

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()