
class BookManage(object):

    def __init__(self, db):
        self.db = db

    def run(self):
        self._window()
        while True:
            try:
                cmd = input("\033[1;34mcmd>A>\033[0m").strip()
                if cmd == "1":
                    self._add_book()
                elif cmd == "2":
                    self._delete_book()
                elif cmd == "3":
                    self._modify_book_information()
                elif cmd == "4":
                    self._search_book()
                elif cmd == "5":
                    self._display_all_books()
                elif cmd == "quit":
                    print("back to main window")
                    break
                else:
                    print("\033[0;31minput not a command.\033[0m")
                print()
            except Exception as e:
                print(e)

    def _window(self):
        print("------\033[0;31mA. 图书管理\033[0m------")
        print("\033[0;35m1\033[0m. 增加新书")
        print("\033[0;35m2\033[0m. 删除书籍")
        print("\033[0;35m3\033[0m. 修改书籍信息")
        print("\033[0;35m4\033[0m. 查找书籍")
        print("\033[0;35m5\033[0m. 显示所有书籍")
        print("-------------------")

    def _add_book(self):
        new_book = input("请输入书的ISBN号，名字，作者和索书号（“;”隔开）>")
        flag = self._get_command_flag(new_book, 4)
        if flag == -1:
            self._add_book()
        elif flag == 1:
            isbn, name, writer, cable_number = new_book.strip().split(";")
            max_number = self.db.search("select max(number) from book where ISBN = '{}'".format(isbn))
            self.db.insert("insert into book(ISBN, name, writer, cable_number, number, status) value("
                           "'{}', '{}', '{}', '{}', {}, '可借')".format(
                isbn, name, writer, cable_number, max_number+1))

    def _delete_book(self):
        delete_book = input("请输入要删除的书的ISBN号和书次号（“;”隔开）>")
        flag = self._get_command_flag(delete_book, 2)
        if flag == -1:
            self._delete_book()
        elif flag == 1:
            isbn, number = delete_book.strip().split(";")
            status = self.db.search("select status from book where ISBN = '{}' and number = {}".format(isbn, number))
            if len(status) == 0:
                print("查无此书")
            elif status[0][0] == '借出':
                print("该书处于借出状态，无法删除")
            elif status[0][0] == '可借':
                self.db.delete("delete from book where ISBN = '{}' and number = {}".format(isbn, number))
            else:
                print("出现未知错误")

    def _modify_book_information(self):
        modify_book = input("请输入要修改的书的ISBN号和书次号（“;”隔开）>")
        modify_flag = self._get_command_flag(modify_book, 2)
        if modify_flag == -1:
            print("\033[0;31minput not an expect command.\033[0m")
            self._modify_book_information()
        elif modify_flag == 1:
            isbn, number = modify_book.strip().split(";")
            if not number.isdigit():
                print("书次号只能由数字组成")
                self._modify_book_information()
            else:
                self._process_modify_book_information(isbn, number)

    def _search_book(self):
        tips = self._get_search_book_tips()
        i_to_item = {0: "ISBN", 1: "name", 2: "cable_number", 3: "status", 4: "number"}
        inf_and_items = []
        for i, tip in enumerate(tips):
            infor = input(tip)
            if infor == "quit":
                return
            elif infor != "n" and infor != "N":
                inf_and_items.append([infor, i_to_item[i]])
        if len(inf_and_items) > 0 and inf_and_items[-1][1] == "number" and not inf_and_items[-1][0].isdigit():
            print("书次号只能是数字")
            print()
            self._search_book()
        else:
            search_sql = "select name, ISBN, cable_number, status, number from book"
            count = 0
            for inf, item in inf_and_items:
                if count == 0:
                    if item == "number":
                        search_sql += " where {} = {}".format(item, inf)
                    else:
                        search_sql += " where {} like '%{}%'".format(item, inf)
                else:
                    if item == "number":
                        search_sql += " and {} = {}".format(item, inf)
                    else:
                        search_sql += " and {} like '%{}%'".format(item, inf)
                count += 1
            self._display_books(search_sql)

    def _display_all_books(self):
        books = self.db.search("select name, ISBN, cable_number, status, number from book")
        print("\033[0;43m{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:{4}^20}\t{5:^20}\033[0m".format(
            "名字", "ISBN", "索书号", "状态", chr(12288), "书次号"))
        for i, book in enumerate(books):
            print("{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:{4}^20}\t{5:^20}".format(
                book[0], book[1], book[2], book[3], chr(12288), book[4]))

    def _display_books(self, sql):
        books = self.db.search(sql)
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

    def _process_modify_book_information(self, isbn, number):
        res = self.db.search(
            "select name from book where ISBN = '{}' and number = {}".format(isbn, number))
        if len(res) == 0:
            self._modify_book_information()
        else:
            tips = self._get_modify_book_tips()
            for i, (tip, item) in enumerate(tips):
                ans = input(tip)
                if ans == "quit":
                    break
                elif ans != "n" and ans != "N":
                    if i == 3 and ans not in ("可借", "借出"):
                        print("书籍状态只能是“可借”或者“借出”")
                        break
                    elif i == 4 and not ans.isdigit():
                        print("书次号只能由数字组成")
                        break
                    else:
                        self.db.update(
                            "update book set {} = '{}' where ISBN = '{}' and number = {}".format(
                                item, ans, isbn, number))

    def _get_modify_book_tips(self):
        tip1 = "请输入新的ISBN号(回复“n”拒绝修改此项)>"
        tip2 = "请输入新的书名(回复“n”拒绝修改此项)>"
        tip3 = "请输入新的索书号(回复“n”拒绝修改此项)>"
        tip4 = "请输入新的书籍状态(回复“n”拒绝修改此项)>"
        tip5 = "请输入新的书次号(回复“n”拒绝修改此项)>"
        tips = [[tip1, "ISBN"], [tip2, "name"], [tip3, "cable_number"], [tip4, "status"], [tip5, "number"]]
        return tips

    def _get_search_book_tips(self):
        tip1 = "请输入ISBN号相关信息(回复“n”表示不限)>"
        tip2 = "请输入书名相关信息(回复“n”表示不限)>"
        tip3 = "请输入索书号相关信息(回复“n”表示不限)>"
        tip4 = "请输入书籍状态相关信息(回复“n”表示不限)>"
        tip5 = "请输入书次号相关信息(回复“n”表示不限)>"
        tips = [tip1, tip2, tip3, tip4, tip5]
        return tips