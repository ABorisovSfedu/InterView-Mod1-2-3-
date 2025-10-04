#!/usr/bin/env python3
"""Скрипт для добавления новых компонентов и терминов для шаблонов"""

import sqlite3
import os

def add_new_template_components():
    """Добавляет новые компоненты для шаблонов"""
    
    # Подключаемся к базе данных
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mod3.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Новые компоненты для шаблонов
        new_components = [
            # Medical clinic компоненты
            ("ui.doctorsList", "ui.doctorsList", "Список врачей", "medical"),
            ("ui.appointmentForm", "ui.appointmentForm", "Форма записи на приём", "medical"),
            
            # Education portal компоненты
            ("ui.courseList", "ui.courseList", "Список курсов", "education"),
            
            # Job board компоненты
            ("ui.jobList", "ui.jobList", "Список вакансий", "job"),
            
            # Event landing компоненты
            ("ui.countdown", "ui.countdown", "Обратный отсчёт", "event"),
            ("ui.schedule", "ui.schedule", "Расписание мероприятий", "event"),
            ("ui.speakers", "ui.speakers", "Список спикеров", "event"),
            ("ui.tickets", "ui.tickets", "Билеты", "event"),
            ("ui.gallery", "ui.gallery", "Галерея", "event"),
            
            # Finance services компоненты (calculator уже есть)
            ("ui.contacts", "ui.contacts", "Контакты", "contact"),
        ]
        
        for name, component_type, description, category in new_components:
            # Проверяем, существует ли компонент
            cursor.execute("SELECT id FROM components WHERE name = ?", (name,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO components (name, component_type, description, category, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, 1, datetime('now'), datetime('now'))
                """, (name, component_type, description, category))
                print(f"✅ Добавлен компонент: {name}")
            else:
                print(f"⚠️ Компонент {name} уже существует")
        
        print("✅ Новые компоненты добавлены")
        
        # Новые термины для шаблонов
        new_terms = [
            # Medical clinic термины
            ("клиника", ["медицинская клиника", "поликлиника", "больница"], "ui.servicesGrid"),
            ("врач", ["доктор", "медик", "специалист"], "ui.doctorsList"),
            ("медицинский центр", ["медцентр", "клиника", "медицинское учреждение"], "ui.servicesGrid"),
            ("запись", ["записаться", "запись на приём", "бронирование"], "ui.appointmentForm"),
            ("приём", ["приём врача", "консультация", "осмотр"], "ui.appointmentForm"),
            ("лечение", ["терапия", "медицинская помощь", "оздоровление"], "ui.servicesGrid"),
            ("анализы", ["лабораторные анализы", "исследования", "диагностика"], "ui.servicesGrid"),
            ("здоровье", ["медицина", "здоровый образ жизни", "профилактика"], "ui.servicesGrid"),
            
            # Education portal термины
            ("обучение", ["образование", "учёба", "развитие"], "ui.courseList"),
            ("курс", ["программа обучения", "учебный курс", "дисциплина"], "ui.courseList"),
            ("программа", ["учебная программа", "курс обучения", "образовательная программа"], "ui.courseList"),
            ("преподаватель", ["учитель", "инструктор", "тренер"], "ui.featuresList"),
            ("урок", ["занятие", "лекция", "семинар"], "ui.courseList"),
            ("школа", ["учебное заведение", "образовательное учреждение"], "ui.featuresList"),
            ("студенты", ["учащиеся", "обучающиеся", "слушатели"], "ui.testimonials"),
            
            # Job board термины
            ("работа", ["трудоустройство", "занятость", "деятельность"], "ui.jobList"),
            ("вакансии", ["открытые позиции", "трудовые места", "должности"], "ui.jobList"),
            ("карьера", ["профессиональный рост", "развитие карьеры"], "ui.jobList"),
            ("резюме", ["CV", "анкета", "профиль"], "ui.form"),
            ("отклик", ["откликнуться", "подать заявку", "отправить резюме"], "ui.button"),
            ("поиск работы", ["поиск вакансий", "трудоустройство"], "ui.search"),
            
            # Event landing термины
            ("мероприятие", ["событие", "акция", "встреча"], "ui.schedule"),
            ("событие", ["мероприятие", "акция", "встреча"], "ui.schedule"),
            ("конференция", ["симпозиум", "форум", "съезд"], "ui.schedule"),
            ("фестиваль", ["праздник", "фест", "празднование"], "ui.schedule"),
            ("регистрация", ["запись", "регистрироваться", "участие"], "ui.form"),
            ("билеты", ["входные билеты", "пропуски", "вход"], "ui.tickets"),
            ("расписание", ["программа", "план", "график"], "ui.schedule"),
            
            # Finance services термины
            ("банк", ["банковское учреждение", "финансовое учреждение"], "ui.servicesGrid"),
            ("кредит", ["займ", "ссуда", "кредитование"], "ui.servicesGrid"),
            ("ипотека", ["ипотечное кредитование", "жилищный кредит"], "ui.servicesGrid"),
            ("инвестиции", ["вложения", "инвестирование", "капиталовложения"], "ui.servicesGrid"),
            ("страховка", ["страхование", "страховой полис"], "ui.servicesGrid"),
            ("финансы", ["денежные средства", "финансовые услуги"], "ui.servicesGrid"),
            ("проценты", ["процентная ставка", "доходность"], "ui.calculator"),
            ("заявка", ["заявление", "подача заявки", "оформление"], "ui.form"),
        ]
        
        for term_name, synonyms, component_name in new_terms:
            # Проверяем, существует ли термин
            cursor.execute("SELECT id FROM terms WHERE term = ?", (term_name,))
            existing_term = cursor.fetchone()
            
            if existing_term:
                print(f"⚠️ Термин '{term_name}' уже существует, пропускаем")
                continue
            
            # Создаем термин
            cursor.execute("""
                INSERT INTO terms (term, description, is_active, created_at, updated_at)
                VALUES (?, ?, 1, datetime('now'), datetime('now'))
            """, (term_name, f"Термин для компонента {component_name}"))
            
            term_id = cursor.lastrowid
            
            # Создаем синонимы
            for synonym_name in synonyms:
                cursor.execute("""
                    INSERT INTO synonyms (term_id, synonym, created_at, updated_at)
                    VALUES (?, ?, datetime('now'), datetime('now'))
                """, (term_id, synonym_name))
            
            # Создаем маппинг с компонентом
            cursor.execute("SELECT id FROM components WHERE name = ?", (component_name,))
            component_result = cursor.fetchone()
            if component_result:
                component_id = component_result[0]
                cursor.execute("""
                    INSERT INTO mappings (term_id, component_id, confidence, created_at, updated_at)
                    VALUES (?, ?, 1.0, datetime('now'), datetime('now'))
                """, (term_id, component_id))
                print(f"✅ Добавлен термин: {term_name} → {component_name}")
            else:
                print(f"⚠️ Компонент {component_name} не найден для термина {term_name}")
        
        conn.commit()
        print("✅ Новые термины добавлены")
        
        # Показываем статистику
        cursor.execute("SELECT COUNT(*) FROM terms")
        terms_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM components")
        components_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM synonyms")
        synonyms_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM mappings")
        mappings_count = cursor.fetchone()[0]
        
        print(f"📊 Обновленная статистика:")
        print(f"  - Терминов: {terms_count}")
        print(f"  - Компонентов: {components_count}")
        print(f"  - Синонимов: {synonyms_count}")
        print(f"  - Маппингов: {mappings_count}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка при добавлении данных: {e}")
        raise
    finally:
        conn.close()

def main():
    """Основная функция"""
    print("🚀 Добавление новых компонентов и терминов для шаблонов")
    print("")
    
    add_new_template_components()
    
    print("")
    print("✅ Новые компоненты и термины успешно добавлены!")

if __name__ == "__main__":
    main()
