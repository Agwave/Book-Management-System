from object.connectMysql import ConnetMysql
from object.book_manage import BookManage
from object.reader_manage import ReaderManage
from object.borrow_manage import BorrowManage

def _main():
    db = ConnetMysql()
    book_window = BookManage(db)
    reader_window = ReaderManage(db)
    borrow_window = BorrowManage(db)
    main_window()
    try:
        while True:
            cmd = input("\033[1;34mcmd>\033[0m").strip()
            if cmd == "A" or cmd == "a":
                book_window.run()
                main_window()
            elif cmd == "B" or cmd == "b":
                reader_window.run()
                main_window()
            elif cmd == "C" or cmd == "c":
                borrow_window.run()
                main_window()
            elif cmd == "quit":
                print("Bye")
                break
            else:
                print("\033[0;31minput not a command\033[0m")
    except Exception as e:
        print(e)

def main_window():
    print("------\033[0;31m欢迎使用图书管理系统\033[0m------")
    print("\033[0;35mA\033[0m. 图书管理")
    print("\033[0;35mB\033[0m. 读者管理")
    print("\033[0;35mC\033[0m. 借阅归还管理")
    print("--------------------------")


if __name__ == '__main__':
    _main()