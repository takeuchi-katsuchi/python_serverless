__pragma__('alias', 'S', '$')

from const import BASE_URL

class Model:
    # コンストラクタ
    def __init__(self):
        self._todos = []

    #  指定されたIDのToDoを取得する
    def get_todo(self, todo_id):
        for todo in self._todos:
            if todo['id'] ==todo_id:
                return todo
        return None

    # すべてのToDoを取得する
    def get_all_todos(self):
        return self._todos

    # 全件取得のAPIを呼び出す
    def load_all_todos(self):
        S.ajax({
            'url': f"{BASE_URL}todos",
            'type': 'GET',
        }).done(
            self._success_load_all_todos
        ).fail(
            lambda d: alert('サーバーとの通信に失敗しました。')
        )

    # load_all_todos()成功時の処理
    def _success_load_all_todos(self, data):
        self._todos = data
        S('body').trigger('todos-updated')