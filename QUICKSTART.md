# Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Запуск тестов

```bash
pytest
```

## 3. Анализ примера кода

```bash
python -m src.main data/sample_code.py
```

## 4. Запуск примера скрипта

```bash
python scripts/example_usage.py
```

## 5. Проверка перед сдачей

- [ ] Все тесты проходят: `pytest -v`
- [ ] Код проверен линтером: `flake8 src tests`
- [ ] README обновлен (замените YOUR_USERNAME/YOUR_REPO)
- [ ] Все файлы закоммичены и запушены
- [ ] GitHub Actions workflow успешно выполнен

## Структура проекта

```
.
├── src/              # Исходный код
├── tests/            # Тесты
├── data/             # Примеры кода
├── docs/             # Документация
├── scripts/          # Вспомогательные скрипты
└── .github/workflows/ # CI/CD workflows
```

## Важные замечания

1. **Обновите README.md**: Замените `YOUR_USERNAME/YOUR_REPO` на реальные значения
2. **Проверьте workflows**: Убедитесь, что пути к файлам корректны
3. **Запустите тесты**: `pytest -v` должен пройти успешно
4. **Проверьте линтер**: `flake8 src tests` не должен показывать критических ошибок

