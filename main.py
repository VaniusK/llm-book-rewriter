from imports import *
from book_processor import BookProcessor




if __name__ == "__main__":

    for filename in os.listdir("."):
        if filename.endswith(".fb2"):
            book_processor = BookProcessor("google", "fb2")
            book_processor.process_fb2_book(filename)
