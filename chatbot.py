from langgraph.graph import MessageGraph
from langchain_ollama import ChatOllama
from datetime import datetime, timezone
from typing import Dict, Any

# 1. Инструмент: возвращает текущее время UTC в формате ISO-8601
def get_current_time() -> Dict[str, str]:
    """Возвращает текущее время UTC в формате ISO-8601."""
    now = datetime.now(timezone.utc)
    return {"utc": now.strftime("%Y-%m-%dT%H:%M:%SZ")}

# 2. Настройка модели Solar через Ollama
model = ChatOllama(
    model="solar",
    temperature=0.5,
    base_url="http://localhost:11434"
)

# 3. Функция роутера: определяет, куда направить сообщение
def initial_router(state: list) -> str:
    last_message = state[-1].content.lower()
    if any(k in last_message for k in {"time", "hour", "clock"}):
        return "get_time"
    else:
        return "model"

# 4. Построение графа обработки сообщений
graph = MessageGraph()

# Добавляем ноды
graph.add_node("model", model)
graph.add_node("get_time", lambda state: get_current_time())
graph.add_node("router", initial_router)

# Устанавливаем начальную точку
graph.set_entry_point("router")

# Определяем ребра
graph.add_conditional_edges(
    "router",
    initial_router,
    {"model": "model", "get_time": "get_time"}
)
graph.add_edge("get_time", "model")
graph.add_edge("model", "__end__")

# 5. Компиляция приложения
app = graph.compile()

# 6. Локальный чат для тестирования (опционально, не для langgraph dev)
if __name__ == "__main__":
    print("Запущен локальный чат. Введите 'exit' для выхода.")
    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            break
        # Для MessageGraph отправляем список сообщений
        response = app.invoke([{"role": "human", "content": user_input}])
        # Ответ от модели находится в последнем элементе списка
        print("Бот:", response[-1].content)