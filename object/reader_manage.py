
class ReaderManage(object):

    def __init__(self, db):
        self.db = db

    def run(self):
        self.window()
        while True:
            try:
                cmd = input("\033[1;34mcmd>B>\033[0m").strip()
                if cmd == "1":
                    self._add_reader()
                elif cmd == "2":
                    self._delete_reader()
                elif cmd == "3":
                    self._modify_reader()
                elif cmd == "4":
                    self._search_reader()
                elif cmd == "5":
                    self._display_all_readers()
                elif cmd == "quit":
                    print("back to main window")
                    break
                else:
                    print("\033[0;31minput not a command.\033[0m")
                print()
            except Exception as e:
                print(e)

    def window(self):
        print("------\033[0;31mB. 读者管理\033[0m------")
        print("\033[0;35m1\033[0m. 注册读者")
        print("\033[0;35m2\033[0m. 注销读者")
        print("\033[0;35m3\033[0m. 修改读者信息")
        print("\033[0;35m4\033[0m. 查找读者")
        print("\033[0;35m5\033[0m. 显示所有读者")
        print("-------------------")

    def _add_reader(self):
        new_reader = input("请输入作者的名字，设置的密码和电话（“;”隔开）>").strip().split(";")
        if len(new_reader) == 1 and new_reader == "quit":
            return
        elif len(new_reader) != 3:
            print("\033[0;31minput not an expect command.\033[0m")
        else:
            name, password, tel  = new_reader
            if not tel.isdigit() and len(tel) != 11:
                print("电话号码必须是11位的数字")
                self._add_reader()
            elif not password.isalnum():
                print("密码只能由字母和数字组成")
                self._add_reader()
            else:
                self.db.insert("insert into reader(name, password, tel) value("
                               "'{}', '{}', '{}')".format(name, password, tel))

    def _delete_reader(self):
        delete_reader_id = input("请输入要删除的读者的id号>")
        if delete_reader_id == "quit":
            return
        elif not delete_reader_id.isdigit():
            print("输入的读者的id必须是数字")
            self._delete_reader()
        else:
            borrow_ids = self.db.search(
                "select borrow_id from borrow where reader_id = {}".format(delete_reader_id))
            if len(borrow_ids) == 0:
                self.db.delete("delete from reader where id = {}".format(delete_reader_id))
            else:
                print("该读者有借阅未还的书，无法删除")

    def _modify_reader(self):
        modify_reader_id = input("请输入要修改的作者的id>")
        if modify_reader_id == "quit":
            return
        elif not modify_reader_id.isdigit():
            print("输入的读者的id必须是数字")
            self._modify_reader()
        else:
            id = self.db.search("select name from reader where id = {}".format(modify_reader_id))
            if len(id) == 0:
                print("此id不存在")
                self._modify_reader()
            else:
                tip1 = "请输入新的名字(回复“n”拒绝修改此项)>"
                tip2 = "请输入新的电话号码(回复“n”拒绝修改此项)>"
                tip3 = "请输入新的密码(回复“n”拒绝修改此项)>"
                tips = [[tip1, "name"], [tip2, "tel"], [tip3, "password"]]
                for i, (tip, item) in enumerate(tips):
                    ans = input(tip)
                    if ans == "quit":
                        break
                    elif ans != "n" and ans != "N":
                        if i == 1 and not ans.isdigit() and len(ans) != 11:
                            print("电话号码必须是11位的数字")
                        elif i == 2 and not ans.isalnum():
                            print("密码只能由字母和数字组成")
                        else:
                            self.db.update(
                                "update reader set {} = '{}' where id = '{}'".format(
                                    item, ans, modify_reader_id))

    def _search_reader(self):
        tip1 = "请输入读者名字的相关信息(回复“n”表示不限)>"
        tip2 = "请输入读者id的相关信息(回复“n”表示不限)>"
        tip3 = "请输入读者电话的相关信息(回复“n”表示不限)>"
        tip4 = "请输入读者密码的相关信息(回复“n”表示不限)>"
        tips = [tip1, tip2, tip3, tip4]
        i_to_item = {0: "name", 1: "id", 2: "tel", 3: "password"}
        inf_and_items = []
        for i, tip in enumerate(tips):
            infor = input(tip)
            if infor == "quit":
                return
            elif infor != "n" and infor != "N":
                inf_and_items.append([infor, i_to_item[i]])
        search_sql = "select name, id, tel, password from reader"
        count = 0
        for inf, item in inf_and_items:
            if count == 0:
                if item == "id":
                    search_sql += " where {} = {}".format(item, inf)
                else:
                    search_sql += " where {} like '%{}%'".format(item, inf)
            else:
                if item == "id":
                    search_sql += " and {} = {}".format(item, inf)
                else:
                    search_sql += " and {} like '%{}%'".format(item, inf)
            count += 1
        self._display_readers(search_sql)

    def _display_all_readers(self):
        readers = self.db.search("select name, id, tel, password from reader")
        print("\033[0;43m{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:^20}\033[0m".format(
            "名字", "id", "电话", "密码", chr(12288)))
        for i, reader in enumerate(readers):
            print("{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:^20}".format(
                reader[0], reader[1], reader[2], reader[3], chr(12288)))

    def _display_readers(self, sql):
        readers = self.db.search(sql)
        print("\033[0;43m{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:^20}\033[0m".format(
            "名字", "id", "电话", "密码", chr(12288)))
        for i, reader in enumerate(readers):
            print("{0:{4}^20}\t{1:^20}\t{2:^20}\t{3:^20}".format(
                reader[0], reader[1], reader[2], reader[3], chr(12288)))