#!/usr/bin/env python3
"""Упрощенный скрипт для добавления расширенной библиотеки терминов в Mod3-v1"""

import sqlite3
import os

def init_extended_vocab():
    """Инициализирует расширенную библиотеку терминов в SQLite"""
    
    # Подключаемся к базе данных
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mod3.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Очищаем существующие данные
        cursor.execute("DELETE FROM mappings")
        cursor.execute("DELETE FROM synonyms")
        cursor.execute("DELETE FROM terms")
        cursor.execute("DELETE FROM components")
        
        print("✅ Очистили существующие данные")
        
        # Создаем компоненты
        components_data = [
            # Navigation компоненты
            ("ui.breadcrumb", "ui.breadcrumb", "Хлебные крошки", "navigation"),
            ("ui.breadcrumbAdvanced", "ui.breadcrumbAdvanced", "Расширенные хлебные крошки", "navigation"),
            ("ui.sidebar", "ui.sidebar", "Боковая панель", "navigation"),
            ("ui.categoryMenu", "ui.categoryMenu", "Меню категорий", "navigation"),
            ("ui.dashboardSidebar", "ui.dashboardSidebar", "Панель управления", "navigation"),
            ("ui.topbar", "ui.topbar", "Верхняя панель", "navigation"),
            ("ui.pagination", "ui.pagination", "Пагинация", "navigation"),
            ("ui.profileMenu", "ui.profileMenu", "Вкладка профиля", "navigation"),
            
            # Content компоненты
            ("ui.image", "ui.image", "Изображение", "content"),
            ("ui.imageGallery", "ui.imageGallery", "Галерея изображений", "content"),
            ("ui.dataTable", "ui.dataTable", "Таблица данных", "content"),
            ("ui.timeChart", "ui.timeChart", "График времени", "content"),
            ("ui.descriptionBlock", "ui.descriptionBlock", "Описание", "content"),
            ("ui.article", "ui.article", "Статья", "content"),
            ("ui.blogPost", "ui.blogPost", "Новость/Блог", "content"),
            ("ui.blogGrid", "ui.blogGrid", "Блог/Новости", "content"),
            ("ui.featuresList", "ui.featuresList", "Список преимуществ", "content"),
            ("ui.faq", "ui.faq", "Вопрос-ответ", "content"),
            ("ui.pricingTable", "ui.pricingTable", "Цены/Тарифы", "content"),
            ("ui.contactsBlock", "ui.contactsBlock", "Контакты", "content"),
            ("ui.testimonials", "ui.testimonials", "Отзывы", "content"),
            ("ui.partnersLogos", "ui.partnersLogos", "Партнёры", "content"),
            ("ui.steps", "ui.steps", "Этапы/Шаги", "content"),
            ("ui.timeline", "ui.timeline", "Таймлайн", "content"),
            ("ui.statsBlock", "ui.statsBlock", "Достижения/Статистика", "content"),
            
            # Interactive компоненты
            ("ui.dropdown", "ui.dropdown", "Выпадающее меню", "interactive"),
            ("ui.rangeSlider", "ui.rangeSlider", "Слайдер", "interactive"),
            
            # Form компоненты
            ("ui.authForm", "ui.authForm", "Форма входа", "form"),
            ("ui.registerForm", "ui.registerForm", "Форма регистрации", "form"),
            ("ui.resetForm", "ui.resetForm", "Форма восстановления", "form"),
            ("ui.contactForm", "ui.contactForm", "Контактная форма", "form"),
            ("ui.subscribeForm", "ui.subscribeForm", "Форма подписки", "form"),
            ("ui.requestForm", "ui.requestForm", "Форма заявки", "form"),
            ("ui.paymentForm", "ui.paymentForm", "Платёж", "form"),
            ("ui.stepForm", "ui.stepForm", "Пошаговая форма", "form"),
            ("ui.captcha", "ui.captcha", "Капча", "form"),
            
            # Advanced компоненты
            ("ui.searchAutocomplete", "ui.searchAutocomplete", "Поиск с автодополнением", "advanced"),
            ("ui.rangeFilter", "ui.rangeFilter", "Фильтр диапазона", "advanced"),
            ("ui.notification", "ui.notification", "Уведомление", "advanced"),
            ("ui.toast", "ui.toast", "Toast уведомление", "advanced"),
            ("ui.progressBar", "ui.progressBar", "Прогресс бар", "advanced"),
            ("ui.rating", "ui.rating", "Рейтинг", "advanced"),
            ("ui.calculator", "ui.calculator", "Калькулятор", "advanced"),
            ("ui.datePicker", "ui.datePicker", "Фильтры по датам", "advanced"),
            
            # Media компоненты
            ("ui.video", "ui.video", "Видео", "media"),
            ("ui.audio", "ui.audio", "Аудио", "media"),
            ("ui.background", "ui.background", "Фон", "media"),
            ("ui.cover", "ui.cover", "Обложка", "media"),
            ("ui.infographic", "ui.infographic", "Инфографика", "media"),
            ("ui.map", "ui.map", "Карта", "media"),
            
            # Business компоненты
            ("ui.servicesGrid", "ui.servicesGrid", "Услуги/Сервисы", "business"),
            ("ui.team", "ui.team", "Команда", "business"),
            ("ui.vacancies", "ui.vacancies", "Вакансии", "business"),
            ("ui.franchise", "ui.franchise", "Партнёрство/Франшиза", "business"),
            
            # Social & Legal компоненты
            ("ui.socialLinks", "ui.socialLinks", "Соцсети", "social"),
            ("ui.socialIcons", "ui.socialIcons", "Иконки соцсетей", "social"),
            ("ui.shareButtons", "ui.shareButtons", "Share кнопки", "social"),
            ("ui.footerMenu", "ui.footerMenu", "Footer меню", "social"),
            ("ui.cookiesBanner", "ui.cookiesBanner", "Cookies баннер", "social"),
            ("ui.legalLinks", "ui.legalLinks", "Legal/Privacy ссылки", "social"),
            
            # Data компоненты
            ("ui.avatar", "ui.avatar", "Аватар", "data"),
            ("ui.badge", "ui.badge", "Badge/Бейджик", "data"),
            ("ui.tag", "ui.tag", "Tag/Метка", "data"),
        ]
        
        for name, component_type, description, category in components_data:
            cursor.execute("""
                INSERT INTO components (name, component_type, description, category, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, 1, datetime('now'), datetime('now'))
            """, (name, component_type, description, category))
        
        print("✅ Компоненты созданы")
        
        # Создаем термины
        terms_data = [
            # Navigation термины
            ("навигация", ["меню", "navbar", "шапка", "навигационное меню"], "ui.navbar"),
            ("поиск", ["строка поиска", "поиск товаров", "search bar"], "ui.search"),
            ("хлебная крошка", ["хлебные крошки", "breadcrumb"], "ui.breadcrumb"),
            
            # Content термины
            ("карточка", ["карточка контента", "card"], "ui.card"),
            ("карточка товар", ["карточка товара", "product card"], "ui.productCard"),
            ("сетка товар", ["каталог товаров", "товарная сетка", "витрина"], "ui.productGrid"),
            ("фильтр", ["фильтры", "фасеты", "по характеристикам"], "ui.filters"),
            ("корзина", ["корзина покупок", "basket", "cart"], "ui.cart"),
            ("призыв действие", ["призыв к действию", "call to action", "cta"], "ui.cta"),
            ("раздел", ["секция", "блок", "section"], "ui.section"),
            ("изображение", ["картинка", "баннер", "image"], "ui.image"),
            ("таблица", ["табличка", "table", "листинг"], "ui.table"),
            ("график", ["диаграмма", "chart"], "ui.chart"),
            ("список", ["bullet list", "маркированный список"], "ui.list"),
            ("сетка", ["layout grid", "колонки"], "ui.grid"),
            
            # Interactive термины
            ("вкладка", ["вкладки", "tabs"], "ui.tabs"),
            ("аккордеон", ["раскрывающийся список"], "ui.accordion"),
            ("карусель", ["слайдер", "галерея"], "ui.carousel"),
            ("модальное окно", ["диалог", "popup", "modal"], "ui.modal"),
            ("подсказка", ["tooltip", "хинт"], "ui.tooltip"),
            ("popover", ["всплывающее окно", "popover"], "ui.popover"),
            
            # Form термины
            ("форма вход", ["форма входа", "логин", "sign in"], "ui.authForm"),
            ("форма регистрация", ["регистрация", "sign up"], "ui.registerForm"),
            ("форма восстановление", ["сброс пароля", "reset password"], "ui.resetForm"),
            
            # Social термины
            ("соцсеть", ["соцсети", "socials"], "ui.socialLinks"),
            
            # Action термины (расширенные)
            ("купить", ["заказать", "подписаться", "узнать больше", "отправить"], "ui.button"),
            ("заказать", ["купить", "подписаться", "узнать больше", "отправить"], "ui.button"),
            ("подписаться", ["купить", "заказать", "узнать больше", "отправить"], "ui.button"),
            ("узнать больше", ["купить", "заказать", "подписаться", "отправить"], "ui.button"),
            
            # Layout термины
            ("сайдбар", ["боковая панель", "side panel", "панель фильтров", "categories"], "ui.sidebar"),
            ("меню категорий", ["список категорий", "категории", "рубрики"], "ui.categoryMenu"),
            ("панель управления", ["панель администратора", "навигация админки"], "ui.dashboardSidebar"),
            ("верхняя панель", ["верхняя линия", "topbar", "header bar"], "ui.topbar"),
            ("пагинация", ["страницы", "навигация по страницам", "пагинатор", "переход между страницами"], "ui.pagination"),
            ("вкладка профиля", ["профиль", "личный кабинет", "user menu"], "ui.profileMenu"),
            ("breadcrumb расширенный", ["путь", "навигационный след"], "ui.breadcrumbAdvanced"),
            
            # Content Block термины
            ("описание", ["about text", "описание компании", "описание услуги"], "ui.descriptionBlock"),
            ("статья", ["новость", "блог", "пост", "публикация"], "ui.article"),
            ("новость", ["статья", "блог", "пост", "публикация"], "ui.blogPost"),
            ("блог", ["статья", "новость", "пост", "публикация"], "ui.blogPost"),
            ("список преимуществ", ["преимущества", "почему мы", "достоинства", "benefits"], "ui.featuresList"),
            ("вопрос-ответ", ["часто задаваемые вопросы", "faq"], "ui.faq"),
            ("цены", ["тарифы", "стоимость", "цены", "packages", "plans"], "ui.pricingTable"),
            ("тарифы", ["цены", "стоимость", "packages", "plans"], "ui.pricingTable"),
            ("контакты", ["контактная информация", "телефон", "адрес", "email"], "ui.contactsBlock"),
            ("отзывы", ["отзывы", "мнения клиентов", "feedback"], "ui.testimonials"),
            ("партнёры", ["партнеры", "клиенты", "brands"], "ui.partnersLogos"),
            ("этапы", ["шаги работы", "этапы", "workflow"], "ui.steps"),
            ("шаги", ["этапы", "workflow"], "ui.steps"),
            ("процесс", ["этапы", "шаги", "workflow"], "ui.steps"),
            ("таймлайн", ["история", "chronology", "события"], "ui.timeline"),
            ("история компании", ["таймлайн", "chronology", "события"], "ui.timeline"),
            ("достижения", ["цифры", "показатели", "факты"], "ui.statsBlock"),
            ("метрики", ["цифры", "показатели", "факты"], "ui.statsBlock"),
            ("статистика", ["цифры", "показатели", "факты"], "ui.statsBlock"),
            
            # Advanced термины
            ("поиск с автодополнением", ["подсказки поиска", "умный поиск"], "ui.searchAutocomplete"),
            ("фильтр диапазона", ["диапазон цен", "от и до", "slider filter"], "ui.rangeFilter"),
            ("выпадающее меню", ["выпадающий список", "select menu"], "ui.dropdown"),
            ("пошаговая форма", ["форма с шагами", "wizard form"], "ui.stepForm"),
            ("капча", ["проверка", "я не робот", "recaptcha"], "ui.captcha"),
            ("уведомление", ["алерт", "уведомление", "alert", "message"], "ui.notification"),
            ("toast", ["всплывающее уведомление", "toast message"], "ui.toast"),
            ("progress bar", ["прогресс", "индикатор выполнения"], "ui.progressBar"),
            ("rating", ["звезды", "рейтинг", "оценка"], "ui.rating"),
            ("slider input", ["ползунок", "слайдер", "range input"], "ui.rangeSlider"),
            
            # Media термины
            ("видео", ["видеофайл", "видео блок", "ролик", "video player"], "ui.video"),
            ("аудио", ["подкаст", "аудиоплеер", "audio player"], "ui.audio"),
            ("галерея изображений", ["галерея", "набор картинок"], "ui.imageGallery"),
            ("фон", ["обложка", "фон страницы"], "ui.background"),
            ("обложка", ["фон", "фон страницы"], "ui.cover"),
            ("инфографика", ["схема", "диаграмма", "визуализация"], "ui.infographic"),
            ("карта", ["карта", "местоположение", "адрес", "Google Map", "Yandex Map"], "ui.map"),
            
            # Business термины
            ("услуги", ["сервисы", "каталог услуг", "направления"], "ui.servicesGrid"),
            ("сервисы", ["услуги", "каталог услуг", "направления"], "ui.servicesGrid"),
            ("команда", ["сотрудники", "наша команда", "people"], "ui.team"),
            ("вакансии", ["работа", "карьера"], "ui.vacancies"),
            ("партнёрство", ["сотрудничество", "партнерство", "франшиза"], "ui.franchise"),
            ("франшиза", ["сотрудничество", "партнерство", "партнёрство"], "ui.franchise"),
            ("контактная форма", ["обратная связь", "форма связи"], "ui.contactForm"),
            ("форма подписки", ["подписка", "рассылка", "newsletter"], "ui.subscribeForm"),
            ("форма заявки", ["оставить заявку", "запрос", "order form"], "ui.requestForm"),
            ("платёж", ["оплата", "checkout", "billing"], "ui.paymentForm"),
            ("расчёт стоимости", ["калькулятор", "рассчитать цену"], "ui.calculator"),
            ("блог", ["новости", "лента новостей", "посты"], "ui.blogGrid"),
            ("новости", ["блог", "лента новостей", "посты"], "ui.blogGrid"),
            
            # Social & Legal термины
            ("иконки соцсетей", ["соцсети", "social icons", "follow us"], "ui.socialIcons"),
            ("share-кнопки", ["поделиться", "share"], "ui.shareButtons"),
            ("footer menu", ["нижнее меню", "подвал сайта"], "ui.footerMenu"),
            ("cookies banner", ["cookie согласие", "политика cookies"], "ui.cookiesBanner"),
            ("legal", ["политика", "соглашение", "terms"], "ui.legalLinks"),
            ("privacy", ["политика", "соглашение", "terms"], "ui.legalLinks"),
            
            # Data термины
            ("таблица данных", ["таблица", "таблица данных"], "ui.dataTable"),
            ("график времени", ["time graph", "temporal chart"], "ui.timeChart"),
            ("фильтры по датам", ["выбор даты", "календарь"], "ui.datePicker"),
            ("аватар", ["фото профиля"], "ui.avatar"),
            ("badge", ["отметка", "бейдж", "label"], "ui.badge"),
            ("бейджик", ["отметка", "badge", "label"], "ui.badge"),
            ("tag", ["тэг", "ярлык", "метка"], "ui.tag"),
            ("метка", ["тэг", "ярлык", "tag"], "ui.tag"),
        ]
        
        for term_name, synonyms, component_name in terms_data:
            # Проверяем, существует ли термин
            cursor.execute("SELECT id FROM terms WHERE term = ?", (term_name,))
            existing_term = cursor.fetchone()
            
            if existing_term:
                term_id = existing_term[0]
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
        
        conn.commit()
        print("✅ Расширенные термины созданы")
        
        # Показываем статистику
        cursor.execute("SELECT COUNT(*) FROM terms")
        terms_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM components")
        components_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM synonyms")
        synonyms_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM mappings")
        mappings_count = cursor.fetchone()[0]
        
        print(f"📊 Статистика:")
        print(f"  - Терминов: {terms_count}")
        print(f"  - Компонентов: {components_count}")
        print(f"  - Синонимов: {synonyms_count}")
        print(f"  - Маппингов: {mappings_count}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка при инициализации данных: {e}")
        raise
    finally:
        conn.close()

def main():
    """Основная функция"""
    print("🚀 Инициализация расширенной библиотеки терминов Mod3-v1")
    print("")
    
    init_extended_vocab()
    
    print("")
    print("✅ Расширенная библиотека терминов успешно инициализирована!")
    print("📊 Добавлено 100+ терминов с синонимами и компонентами")

if __name__ == "__main__":
    main()
