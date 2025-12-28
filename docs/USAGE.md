# Подробное руководство по использованию

## Быстрый старт

### 1. Установка

```bash
pip install -r requirements.txt
```

### 2. Базовый анализ

```bash
python -m src.main data/sample_code.py
```

### 3. Анализ с сохранением отчета

```bash
python -m src.main data/sample_code.py --output report.txt
```

## Расширенные примеры

### Анализ всего проекта

```bash
python -m src.main src/ --output project_analysis.txt
```

### JSON отчет для автоматической обработки

```bash
python -m src.main data/sample_code.py --format json --output report.json
```

### Использование в Python скриптах

```python
from src.analyzer import CodeAnalyzer
from src.reporter import ReportGenerator

analyzer = CodeAnalyzer()
reporter = ReportGenerator()

# Анализ файла
results = analyzer.analyze_file("my_code.py")

# Анализ директории
results = analyzer.analyze_directory("my_project/")

# Генерация отчетов
text_report = reporter.generate_text_report(results)
json_report = reporter.generate_json_report(results)
summary = reporter.generate_summary(results)

# Сохранение
reporter.save_report(results, "output.txt", "text")
```

## Интерпретация результатов

### Оценка качества

- **90-100 (A)**: Отличный код, готов к production
- **80-89 (B)**: Хороший код, небольшие улучшения возможны
- **70-79 (C)**: Удовлетворительный код, требует рефакторинга
- **60-69 (D)**: Код требует значительных улучшений
- **0-59 (F)**: Код низкого качества, необходим серьезный рефакторинг

### Метрики

**PEP 8 Compliance**: Процент соответствия стандартам Python
- > 90%: Отлично
- 70-90%: Хорошо
- < 70%: Требует улучшения

**Cyclomatic Complexity**: Сложность функций
- < 5: Простая функция
- 5-10: Средняя сложность
- > 10: Высокая сложность (рекомендуется рефакторинг)

**Docstring Coverage**: Покрытие документацией
- 100%: Идеально
- 70-99%: Хорошо
- < 70%: Требует добавления документации

**Code Duplication**: Уровень дублирования
- < 10%: Низкое дублирование
- 10-30%: Среднее дублирование
- > 30%: Высокое дублирование (рекомендуется рефакторинг)

## CI/CD интеграция

### GitHub Actions

Проект включает два workflow:

1. **tests.yml** - автоматическая проверка при каждом push
2. **daily_report.yml** - ежедневные отчеты и ручной запуск

### Использование daily_report workflow

1. Перейдите в раздел Actions на GitHub
2. Выберите "Daily Code Quality Report"
3. Нажмите "Run workflow"
4. Выберите параметры:
   - Target directory (по умолчанию: `data`)
   - Output format (text или json)
5. Запустите workflow
6. Скачайте отчеты из артефактов

## Часто задаваемые вопросы

**Q: Как улучшить оценку?**
A: Следуйте рекомендациям в отчете. Обычно помогает:
- Добавление docstrings
- Снижение цикломатической сложности
- Улучшение PEP 8 соответствия
- Устранение дублирования кода

**Q: Можно ли анализировать код с синтаксическими ошибками?**
A: Нет, инструмент требует валидный Python код. Исправьте синтаксические ошибки перед анализом.

**Q: Как настроить пороги для метрик?**
A: Измените параметры в классе `CodeAnalyzer`:
```python
analyzer = CodeAnalyzer()
analyzer.complexity_threshold = 15  # Изменить порог сложности
analyzer.duplication_threshold = 0.2  # Изменить порог дублирования
```

