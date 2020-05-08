#to import the .csv file

import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://ghavkjvddfqrlb:44d807999d59280b8ab0440d66946f69b2c6601b94d1879574f7ace5e4104899@ec2-18-235-97-230.compute-1.amazonaws.com:5432/d9jrtqc0v005hs')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f=open("books.csv","r")
    reader=csv.reader(f)
    next(reader)
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn, :title, :author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
        db.commit()
        print(f"Added book:'{title}' by '{author}' year:'{year}' with isbn:'{isbn}'")

main()