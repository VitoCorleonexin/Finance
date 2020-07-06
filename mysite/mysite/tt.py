import os
import datetime
def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(__file__)
    print(os.path.abspath(__file__))
    print(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    print(os.path.join(BASE_DIR,'templates'))
    print(datetime.date.today())

if __name__ == "__main__":
    main()


