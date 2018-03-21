import csv
from time import localtime, strftime
import sys

def csv_fusion(pubs, authors):
    timestamp = strftime("%Y_%m_%d", localtime())
    path = 'data_out/' + timestamp + '_combo.csv'

    with open(path, 'a+') as record:
        fieldnames = ['gatorlink', 'author_uri', 'author_name', 'article_uri', 'article_name', 'article_type', 'journal_uri', 'journal_name', 'issn', 'pub_date', 'pmid', 'doi']
        writer = csv.DictWriter(record, fieldnames=fieldnames)
        writer.writeheader()

        for pub in pubs:
            auth_n = pub.get('author_uri')
            if auth_n:
                try:
                    auth_name = authors[auth_n][0]
                    auth_gl = authors[auth_n][1]
                except KeyError as e:
                    auth_name = ''
                    auth_gl = ''
                writer.writerow({'gatorlink': auth_gl,
                                'author_uri': auth_n,
                                'author_name': auth_name,
                                'article_uri': pub['article_uri'],
                                'article_name': pub['article_title'],
                                'article_type': pub['article_type'],
                                'journal_uri': pub['journal_uri'],
                                'journal_name': pub['journal_name'],
                                'issn': pub['issn'],
                                'pub_date': pub['pub_date'],
                                'pmid': pub['pmid'],
                                'doi': pub['doi']})
            else:
                writer.writerow({'gatorlink': '',
                                'author_uri': '',
                                'author_name': '',
                                'article_uri': pub['article_uri'],
                                'article_name': pub['article_title'],
                                'article_type': pub['article_type'],
                                'journal_uri': pub['journal_uri'],
                                'journal_name': pub['journal_name'],
                                'issn': pub['issn'],
                                'pub_date': pub['pub_date'],
                                'pmid': pub['pmid'],
                                'doi': pub['doi']})

    return path

def main(pub_path, auth_path):
    pubs = []
    authors = {}

    with open(pub_path, 'r') as pubfile:
        pubread = csv.DictReader(pubfile, delimiter=',')
        pub_headers = pubread.fieldnames
        print(pub_headers)
        for row in pubread:
            pubs.append({'author_uri': row['author_uri'],
                        'article_uri': row['article_uri'],
                        'article_title': row['article_title'],
                        'article_type': row['article_type'],
                        'journal_uri': row['journal_uri'],
                        'journal_name': row['journal_name'],
                        'issn': row['issn'],
                        'pub_date': row['pub_date'],
                        'pmid': row['pmid'],
                        'doi': row['doi']})  
        print("Pubs read")

    with open(auth_path, 'r') as authfile:
        authread = csv.DictReader(authfile, delimiter=',')
        auth_headers = authread.fieldnames
        print(auth_headers)
        for row in authread:
            authors[row['author_uri']] = (row['author_name'], row['gatorlink'])
        print("Authors read")

    fu_sion_ha = csv_fusion(pubs, authors)
    print("Check " + fu_sion_ha)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])