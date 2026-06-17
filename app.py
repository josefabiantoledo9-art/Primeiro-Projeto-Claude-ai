import streamlit as st
from database import init_db, add_task, get_tasks, toggle_task, delete_task

PRIORITY_COLORS = {
    "Alta": "🔴",
    "Média": "🟡",
    "Baixa": "🟢",
}

st.set_page_config(page_title="Gerenciador de Tarefas", page_icon="✅", layout="wide")
init_db()


def render_sidebar():
    st.sidebar.title("➕ Nova Tarefa")
    with st.sidebar.form("add_task_form", clear_on_submit=True):
        title = st.text_input("Título *", placeholder="Ex: Reunião de equipe")
        description = st.text_area("Descrição", placeholder="Detalhes da tarefa...")
        priority = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
        submitted = st.form_submit_button("Adicionar Tarefa", use_container_width=True)

    if submitted:
        if not title.strip():
            st.sidebar.error("O título é obrigatório.")
        else:
            add_task(title.strip(), description.strip(), priority)
            st.sidebar.success("Tarefa adicionada!")
            st.rerun()

    st.sidebar.divider()
    st.sidebar.title("🔍 Filtros")
    priority_filter = st.sidebar.selectbox(
        "Prioridade", ["Todas", "Alta", "Média", "Baixa"], key="filter_priority"
    )
    status_filter = st.sidebar.selectbox(
        "Status", ["Todas", "Pendentes", "Concluídas"], key="filter_status"
    )
    return priority_filter, status_filter


def render_task_card(task: dict):
    is_done = bool(task["completed"])
    priority_icon = PRIORITY_COLORS.get(task["priority"], "⚪")

    with st.container(border=True):
        col_check, col_content, col_delete = st.columns([1, 10, 1])

        with col_check:
            checked = st.checkbox(
                label="concluída",
                value=is_done,
                key=f"check_{task['id']}",
                label_visibility="collapsed",
            )
            if checked != is_done:
                toggle_task(task["id"], checked)
                st.rerun()

        with col_content:
            title_style = "~~" if is_done else "**"
            st.markdown(
                f"{title_style}{priority_icon} {task['title']}{title_style}"
            )
            if task["description"]:
                st.caption(task["description"])
            st.caption(
                f"Prioridade: **{task['priority']}** | Criada em: {task['created_at']}"
            )

        with col_delete:
            if st.button("🗑️", key=f"del_{task['id']}", help="Deletar tarefa"):
                delete_task(task["id"])
                st.rerun()


def main():
    st.title("✅ Gerenciador de Tarefas")

    priority_filter, status_filter = render_sidebar()

    tasks = get_tasks(priority_filter, status_filter)

    total = len(tasks)
    done = sum(1 for t in tasks if t["completed"])
    pending = total - done

    m1, m2, m3 = st.columns(3)
    m1.metric("Total", total)
    m2.metric("Pendentes", pending)
    m3.metric("Concluídas", done)

    st.divider()

    if not tasks:
        st.info("Nenhuma tarefa encontrada. Adicione uma nova tarefa no menu lateral.")
        return

    active = [t for t in tasks if not t["completed"]]
    finished = [t for t in tasks if t["completed"]]

    if active:
        st.subheader(f"Pendentes ({len(active)})")
        for task in active:
            render_task_card(task)

    if finished:
        st.subheader(f"Concluídas ({len(finished)})")
        for task in finished:
            render_task_card(task)


if __name__ == "__main__":
    main()
