import datetime

class BorrowManage(object):

    def __init__(self, db):
        self.db = db

    def run(self):
        self._window()
        while True:
            try:
                cmd = input("\033[1;34mcmd>C>\033[0m").strip()
                if cmd == "1":
                    self._borrow()
                elif cmd == "2":
                    self._return()
                elif cmd == "3":
                    self._display_books_not_been_borrow()
                elif cmd == "4":
                    self._display_books_been_borrowed()
                elif cmd == "quit":
                    print("back to main window")
                    break
                else:
                    print("\033[0;31minput not a command.\033[0m")
                print()
            except Exception as e:
                print(e)

    def _window(self):
        print("------\033[0;31mC. 借阅归还管理\033[0m------")
        print("\033[0;35m1\033[0m. 图书借阅")
        print("\033[0;35m2\033[0m. 图书归还")
        print("\033[0;35m3\033[0m. 显示在馆图书")
        print("\033[0;35m4\033[0m. 显示借出图书")
        print("-------------------")

    def _borrow(self):
        id_and_password = input("请输入读者id和密码（“;”隔开）>")
        borrow_flag = self._get_borrow_flag(id_and_password)
        if borrow_flag == -1:
            self._borrow()
        elif borrow_flag == 0:
            return
        elif borrow_flag == 1:
            self._process_borrow(id_and_password)


    def _return(self):
        id_and_password = input("请输入读者id和密码（“;”隔开）>")
        return_flag = self._get_return_flag(id_and_password)
        if return_flag == -1:
            self._return()
        elif return_flag == 0:
            return
        elif return_flag == 1:
            id, _ = id_and_password.strip().split(";")
            self._display_books_reader_borrow(id)
            self._process_return(id)

    def _display_books_been_borrowed(self):
        books =self.db.search(
            "select borrow_id, reader_id, book_name, book_ISBN, book_number, borrow_date, return_date from borrow")
        print("\033[0;43m{0:{7}^11}\t{1:{7}^11}\t{2:{7}^20}\t{3:^20}\t{4:{7}^11}\t{5:^20}\t{6:^20}\033[0m".format(
            "借书号", "读者id", "书名", "ISBN", "书次号", "借阅日期", "应还日期", chr(12288)))
        for book in books:
            print("{0:{7}^11}\t{1:{7}^11}\t{2:{7}^20}\t{3:^20}\t{4:{7}^11}\t{5:^20}\t{6:^20}".format(
                book[0], book[1], book[2], book[3], book[4], book[5], book[6], chr(12288)))

    def _display_books_not_been_borrow(self):
        books = self.db.search("select name, ISBN, cable_number, status, number from book where status = '可借'")
        print("\033[0;43m{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:{4}^20}\t{5:^20}\033[0m".format(
            "名字", "ISBN", "索书号", "状态", chr(12288), "书次号"))
        for i, book in enumerate(books):
            print("{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:{4}^20}\t{5:^20}".format(
                book[0], book[1], book[2], book[3], chr(12288), book[4]))

    def _get_command_flag(self, input, exp_len):
        items = input.strip().split(";")
        flag = -1
        if len(items) == 1 and items[0] == "quit":
            flag = 0
        elif len(items) == exp_len:
            cnt = 0
            for item in items:
                if item != "":
                    cnt += 1
            if cnt == len(items):
                flag = 1
        if flag == -1:
            print("\033[0;31minput not an expect command.\033[0m")
        return flag

    def _get_borrow_flag(self, id_and_password):
        """
        -1: 输入不合要求，id不是数字，账户或密码问题
        0： 超时书籍
        1： 可借
        """
        flag = self._get_command_flag(id_and_password, 2)
        if flag == 1:
            id, password = id_and_password.strip().split(";")
            if not id.isdigit():
                print("读者id必须由数字组成")
                flag = -1
            else:
                reader = self.db.search(
                    "select name from reader where id = {} and password = '{}'".format(id, password))
                if len(reader) == 0:
                    print("账户不存在或者密码错误")
                    flag = -1
                else:
                    return_date = self.db.search("select return_date from borrow where reader_id = '{}'".format(id))
                    today = datetime.datetime.today()
                    for r_d in return_date:
                        d = datetime.datetime.strptime(r_d[0], "%Y-%m-%d")
                        if today > d:
                            print("该读者有超时未还的图书，拒绝借阅")
                            flag = 0
                            break
        return flag

    def _get_return_flag(self, id_and_password):
        flag = self._get_command_flag(id_and_password, 2)
        if flag == 1:
            id, password = id_and_password.strip().split(";")
            if not id.isdigit():
                print("读者id必须由数字组成")
                flag = -1
            else:
                reader = self.db.search(
                    "select name from reader where id = {} and password = '{}'".format(id, password))
                if len(reader) == 0:
                    print("账户不存在或者密码错误")
                    flag = -1
        return flag

    def _process_borrow(self, id_and_password):
        id, _ = id_and_password.strip().split(";")
        isbn_and_number = input("请输入要借阅的图书的ISBN号和书次号（“;”隔开）>")
        flag = self._get_command_flag(isbn_and_number, 2)
        if flag == -1:
            self._process_borrow(id_and_password)
        elif flag == 0:
            return
        else:
            isbn, number = isbn_and_number.strip().split(";")
            if not number.isdigit():
                print("书次号必须是整数")
                self._process_borrow(id_and_password)
            else:
                status_and_name = self.db.search(
                    "select status, name from book where isbn = '{}' and number = {}".format(isbn, number))
                if len(status_and_name) == 0:
                    print("找不到对应的图书")
                    self._process_borrow(id_and_password)
                elif len(status_and_name) == 1:
                    if status_and_name[0][0] == "借出":
                        print("该图书已经被借")
                        return
                    self.db.update("update book set status = '借出' "
                                   "where isbn = '{}' and number = {}".format(isbn, number))
                    borrow_date = datetime.datetime.today()
                    return_date = borrow_date + datetime.timedelta(days=60)
                    self.db.insert("insert into borrow(reader_id, book_name, book_ISBN, book_number, borrow_date, return_date)"
                                   "values({}, '{}', '{}', {}, '{}', '{}')".format(
                                    id, status_and_name[0][1], isbn, number, borrow_date.strftime("%Y-%m-%d"),
                                    return_date.strftime("%Y-%m-%d")))
                else:
                    print("出现未知错误")

    def _process_return(self, id):
        isbn_and_number = input("请输入要归还的图书的ISBN号和书次号（“;”隔开）>")
        flag = self._get_command_flag(isbn_and_number, 2)
        if flag == -1:
            self._process_return(id)
        elif flag == 0:
            return
        else:
            isbn, number = isbn_and_number.strip().split(";")
            if not number.isdigit():
                print("书次号必须是整数")
                self._process_return(id)
            else:
                book_name = self.db.search(
                    "select name from book where isbn = '{}' and number = {}".format(isbn, number))
                if len(book_name) == 0:
                    print("找不到对应的图书")
                    self._process_return(id)
                elif len(book_name) == 1:
                    return_date = self.db.search(
                        "select return_date from borrow where book_ISBN = '{}' and book_number = {}".format(isbn, number))
                    if len(return_date) == 0:
                        print("该读者未借阅该书")
                        return
                    self.db.delete("delete from borrow where book_ISBN = '{}' and book_number = {}".format(isbn, number))
                    self.db.update("update book set status = '可借' where ISBN = '{}' and number = {}".format(isbn, number))
                    r_d = datetime.datetime.strptime(return_date[0][0], "%Y-%m-%d")
                    today = datetime.datetime.today()
                    if today > r_d:
                        print("该读者还书超时{}天".format((today-r_d).days))


    def _display_books_reader_borrow(self, reader_id):
        books =self.db.search(
            "select borrow_id, reader_id, book_name, book_ISBN, book_number, borrow_date, return_date "
            "from borrow where reader_id = '{}'".format(reader_id))
        print("\033[0;43m{0:{7}^11}\t{1:{7}^11}\t{2:{7}^20}\t{3:^20}\t{4:{7}^11}\t{5:^20}\t{6:^20}\033[0m".format(
            "借书号", "读者id", "书名", "ISBN", "书次号", "借阅日期", "应还日期", chr(12288)))
        for book in books:
            print("{0:{7}^11}\t{1:{7}^11}\t{2:{7}^20}\t{3:^20}\t{4:{7}^11}\t{5:^20}\t{6:^20}".format(
                book[0], book[1], book[2], book[3], book[4], book[5], book[6], chr(12288)))