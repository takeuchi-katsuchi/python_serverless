__pragma__('alias', 'S', '$')

class View:
    # ToDoリストを描画する
    def render_todo_list(self, data):
        S('#todo-list').empty()
        for todo in data:
            S('#todo-list').append(self._create_todo_row(todo))

    # ToDoの明細行を生成する
    def _create_todo_row(self, todo):
        return f"""
            <tr>
                <td>
                    <input type='checkbox' class="toggle-checkbox" id='check-{todo['id']}' {'checked' if todo['completed'] else ''}>
                </td>
                <td>{todo['title']}</td>
                <td>{todo['memo']}</td>
                <td>{['低', '中', '高'][int(todo['priority']) - 1]}</td>
                <td>
                    <button class='btn btn-outline-primary update-button' id='update-{todo['id']}' data-toggle='modal' data-target='#input-form'>変更</button>
                </td>
                <td>
                    <button class='btn btn-outline-danger delete-button' id='delete-{todo['id']}'>削除</button>
                </td>
            </tr>
        """