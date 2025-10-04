#!/usr/bin/env python3
"""Скрипт для добавления расширенной библиотеки терминов в Mod3-v1"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Term, Synonym, Component, Mapping
from app.database import get_database_url

def init_database():
    """Создает таблицы в базе данных"""
    engine = create_engine(get_database_url())
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")

def init_extended_vocab():
    """Инициализирует расширенную библиотеку терминов"""
    engine = create_engine(get_database_url())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Создаем все новые компоненты
        components_data = [
            # Navigation компоненты
            {"name": "ui.breadcrumb", "component_type": "ui.breadcrumb", "description": "Хлебные крошки", "category": "navigation"},
            {"name": "ui.breadcrumbAdvanced", "component_type": "ui.breadcrumbAdvanced", "description": "Расширенные хлебные крошки", "category": "navigation"},
            {"name": "ui.sidebar", "component_type": "ui.sidebar", "description": "Боковая панель", "category": "navigation"},
            {"name": "ui.categoryMenu", "component_type": "ui.categoryMenu", "description": "Меню категорий", "category": "navigation"},
            {"name": "ui.dashboardSidebar", "component_type": "ui.dashboardSidebar", "description": "Панель управления", "category": "navigation"},
            {"name": "ui.topbar", "component_type": "ui.topbar", "description": "Верхняя панель", "category": "navigation"},
            {"name": "ui.pagination", "component_type": "ui.pagination", "description": "Пагинация", "category": "navigation"},
            {"name": "ui.profileMenu", "component_type": "ui.profileMenu", "description": "Вкладка профиля", "category": "navigation"},
            
            # Content компоненты
            {"name": "ui.image", "component_type": "ui.image", "description": "Изображение", "category": "content"},
            {"name": "ui.imageGallery", "component_type": "ui.imageGallery", "description": "Галерея изображений", "category": "content"},
            {"name": "ui.dataTable", "component_type": "ui.dataTable", "description": "Таблица данных", "category": "content"},
            {"name": "ui.timeChart", "component_type": "ui.timeChart", "description": "График времени", "category": "content"},
            {"name": "ui.descriptionBlock", "component_type": "ui.descriptionBlock", "description": "Описание", "category": "content"},
            {"name": "ui.article", "component_type": "ui.article", "description": "Статья", "category": "content"},
            {"name": "ui.blogPost", "component_type": "ui.blogPost", "description": "Новость/Блог", "category": "content"},
            {"name": "ui.blogGrid", "component_type": "ui.blogGrid", "description": "Блог/Новости", "category": "content"},
            {"name": "ui.featuresList", "component_type": "ui.featuresList", "description": "Список преимуществ", "category": "content"},
            {"name": "ui.faq", "component_type": "ui.faq", "description": "Вопрос-ответ", "category": "content"},
            {"name": "ui.pricingTable", "component_type": "ui.pricingTable", "description": "Цены/Тарифы", "category": "content"},
            {"name": "ui.contactsBlock", "component_type": "ui.contactsBlock", "description": "Контакты", "category": "content"},
            {"name": "ui.testimonials", "component_type": "ui.testimonials", "description": "Отзывы", "category": "content"},
            {"name": "ui.partnersLogos", "component_type": "ui.partnersLogos", "description": "Партнёры", "category": "content"},
            {"name": "ui.steps", "component_type": "ui.steps", "description": "Этапы/Шаги", "category": "content"},
            {"name": "ui.timeline", "component_type": "ui.timeline", "description": "Таймлайн", "category": "content"},
            {"name": "ui.statsBlock", "component_type": "ui.statsBlock", "description": "Достижения/Статистика", "category": "content"},
            
            # Interactive компоненты
            {"name": "ui.dropdown", "component_type": "ui.dropdown", "description": "Выпадающее меню", "category": "interactive"},
            {"name": "ui.rangeSlider", "component_type": "ui.rangeSlider", "description": "Слайдер", "category": "interactive"},
            
            # Form компоненты
            {"name": "ui.authForm", "component_type": "ui.authForm", "description": "Форма входа", "category": "form"},
            {"name": "ui.registerForm", "component_type": "ui.registerForm", "description": "Форма регистрации", "category": "form"},
            {"name": "ui.resetForm", "component_type": "ui.resetForm", "description": "Форма восстановления", "category": "form"},
            {"name": "ui.contactForm", "component_type": "ui.contactForm", "description": "Контактная форма", "category": "form"},
            {"name": "ui.subscribeForm", "component_type": "ui.subscribeForm", "description": "Форма подписки", "category": "form"},
            {"name": "ui.requestForm", "component_type": "ui.requestForm", "description": "Форма заявки", "category": "form"},
            {"name": "ui.paymentForm", "component_type": "ui.paymentForm", "description": "Платёж", "category": "form"},
            {"name": "ui.stepForm", "component_type": "ui.stepForm", "description": "Пошаговая форма", "category": "form"},
            {"name": "ui.captcha", "component_type": "ui.captcha", "description": "Капча", "category": "form"},
            
            # Advanced компоненты
            {"name": "ui.searchAutocomplete", "component_type": "ui.searchAutocomplete", "description": "Поиск с автодополнением", "category": "advanced"},
            {"name": "ui.rangeFilter", "component_type": "ui.rangeFilter", "description": "Фильтр диапазона", "category": "advanced"},
            {"name": "ui.notification", "component_type": "ui.notification", "description": "Уведомление", "category": "advanced"},
            {"name": "ui.toast", "component_type": "ui.toast", "description": "Toast уведомление", "category": "advanced"},
            {"name": "ui.progressBar", "component_type": "ui.progressBar", "description": "Прогресс бар", "category": "advanced"},
            {"name": "ui.rating", "component_type": "ui.rating", "description": "Рейтинг", "category": "advanced"},
            {"name": "ui.calculator", "component_type": "ui.calculator", "description": "Калькулятор", "category": "advanced"},
            {"name": "ui.datePicker", "component_type": "ui.datePicker", "description": "Фильтры по датам", "category": "advanced"},
            
            # Media компоненты
            {"name": "ui.video", "component_type": "ui.video", "description": "Видео", "category": "media"},
            {"name": "ui.audio", "component_type": "ui.audio", "description": "Аудио", "category": "media"},
            {"name": "ui.background", "component_type": "ui.background", "description": "Фон", "category": "media"},
            {"name": "ui.cover", "component_type": "ui.cover", "description": "Обложка", "category": "media"},
            {"name": "ui.infographic", "component_type": "ui.infographic", "description": "Инфографика", "category": "media"},
            {"name": "ui.map", "component_type": "ui.map", "description": "Карта", "category": "media"},
            
            # Business компоненты
            {"name": "ui.servicesGrid", "component_type": "ui.servicesGrid", "description": "Услуги/Сервисы", "category": "business"},
            {"name": "ui.team", "component_type": "ui.team", "description": "Команда", "category": "business"},
            {"name": "ui.vacancies", "component_type": "ui.vacancies", "description": "Вакансии", "category": "business"},
            {"name": "ui.franchise", "component_type": "ui.franchise", "description": "Партнёрство/Франшиза", "category": "business"},
            
            # Social & Legal компоненты
            {"name": "ui.socialLinks", "component_type": "ui.socialLinks", "description": "Соцсети", "category": "social"},
            {"name": "ui.socialIcons", "component_type": "ui.socialIcons", "description": "Иконки соцсетей", "category": "social"},
            {"name": "ui.shareButtons", "component_type": "ui.shareButtons", "description": "Share кнопки", "category": "social"},
            {"name": "ui.footerMenu", "component_type": "ui.footerMenu", "description": "Footer меню", "category": "social"},
            {"name": "ui.cookiesBanner", "component_type": "ui.cookiesBanner", "description": "Cookies баннер", "category": "social"},
            {"name": "ui.legalLinks", "component_type": "ui.legalLinks", "description": "Legal/Privacy ссылки", "category": "social"},
            
            # Data компоненты
            {"name": "ui.avatar", "component_type": "ui.avatar", "description": "Аватар", "category": "data"},
            {"name": "ui.badge", "component_type": "ui.badge", "description": "Badge/Бейджик", "category": "data"},
            {"name": "ui.tag", "component_type": "ui.tag", "description": "Tag/Метка", "category": "data"},
        ]
        
        for comp_data in components_data:
            component = db.query(Component).filter(Component.name == comp_data["name"]).first()
            if not component:
                component = Component(**comp_data)
                db.add(component)
        
        db.flush()
        print("✅ Компоненты созданы")
        
        # Создаем расширенные термины
        terms_data = [
            # Navigation термины
            {"term": "навигация", "synonyms": ["меню", "navbar", "шапка", "навигационное меню"], "component": "ui.navbar"},
            {"term": "поиск", "synonyms": ["строка поиска", "поиск товаров", "search bar"], "component": "ui.search"},
            {"term": "хлебная крошка", "synonyms": ["хлебные крошки", "breadcrumb"], "component": "ui.breadcrumb"},
            
            # Content термины
            {"term": "карточка", "synonyms": ["карточка контента", "card"], "component": "ui.card"},
            {"term": "карточка товар", "synonyms": ["карточка товара", "product card"], "component": "ui.productCard"},
            {"term": "сетка товар", "synonyms": ["каталог товаров", "товарная сетка", "витрина"], "component": "ui.productGrid"},
            {"term": "фильтр", "synonyms": ["фильтры", "фасеты", "по характеристикам"], "component": "ui.filters"},
            {"term": "корзина", "synonyms": ["корзина покупок", "basket", "cart"], "component": "ui.cart"},
            {"term": "призыв действие", "synonyms": ["призыв к действию", "call to action", "cta"], "component": "ui.cta"},
            {"term": "раздел", "synonyms": ["секция", "блок", "section"], "component": "ui.section"},
            {"term": "изображение", "synonyms": ["картинка", "баннер", "image"], "component": "ui.image"},
            {"term": "таблица", "synonyms": ["табличка", "table", "листинг"], "component": "ui.table"},
            {"term": "график", "synonyms": ["диаграмма", "chart"], "component": "ui.chart"},
            {"term": "список", "synonyms": ["bullet list", "маркированный список"], "component": "ui.list"},
            {"term": "сетка", "synonyms": ["layout grid", "колонки"], "component": "ui.grid"},
            
            # Interactive термины
            {"term": "вкладка", "synonyms": ["вкладки", "tabs"], "component": "ui.tabs"},
            {"term": "аккордеон", "synonyms": ["раскрывающийся список"], "component": "ui.accordion"},
            {"term": "карусель", "synonyms": ["слайдер", "галерея"], "component": "ui.carousel"},
            {"term": "модальное окно", "synonyms": ["диалог", "popup", "modal"], "component": "ui.modal"},
            {"term": "подсказка", "synonyms": ["tooltip", "хинт"], "component": "ui.tooltip"},
            {"term": "popover", "synonyms": ["всплывающее окно", "popover"], "component": "ui.popover"},
            
            # Form термины
            {"term": "форма вход", "synonyms": ["форма входа", "логин", "sign in"], "component": "ui.authForm"},
            {"term": "форма регистрация", "synonyms": ["регистрация", "sign up"], "component": "ui.registerForm"},
            {"term": "форма восстановление", "synonyms": ["сброс пароля", "reset password"], "component": "ui.resetForm"},
            
            # Social термины
            {"term": "соцсеть", "synonyms": ["соцсети", "socials"], "component": "ui.socialLinks"},
            
            # Action термины (расширенные)
            {"term": "купить", "synonyms": ["заказать", "подписаться", "узнать больше", "отправить"], "component": "ui.button"},
            {"term": "заказать", "synonyms": ["купить", "подписаться", "узнать больше", "отправить"], "component": "ui.button"},
            {"term": "подписаться", "synonyms": ["купить", "заказать", "узнать больше", "отправить"], "component": "ui.button"},
            {"term": "узнать больше", "synonyms": ["купить", "заказать", "подписаться", "отправить"], "component": "ui.button"},
            
            # Layout термины
            {"term": "сайдбар", "synonyms": ["боковая панель", "side panel", "панель фильтров", "categories"], "component": "ui.sidebar"},
            {"term": "меню категорий", "synonyms": ["список категорий", "категории", "рубрики"], "component": "ui.categoryMenu"},
            {"term": "панель управления", "synonyms": ["панель администратора", "навигация админки"], "component": "ui.dashboardSidebar"},
            {"term": "верхняя панель", "synonyms": ["верхняя линия", "topbar", "header bar"], "component": "ui.topbar"},
            {"term": "пагинация", "synonyms": ["страницы", "навигация по страницам", "пагинатор", "переход между страницами"], "component": "ui.pagination"},
            {"term": "вкладка профиля", "synonyms": ["профиль", "личный кабинет", "user menu"], "component": "ui.profileMenu"},
            {"term": "breadcrumb расширенный", "synonyms": ["путь", "навигационный след"], "component": "ui.breadcrumbAdvanced"},
            
            # Content Block термины
            {"term": "описание", "synonyms": ["about text", "описание компании", "описание услуги"], "component": "ui.descriptionBlock"},
            {"term": "статья", "synonyms": ["новость", "блог", "пост", "публикация"], "component": "ui.article"},
            {"term": "новость", "synonyms": ["статья", "блог", "пост", "публикация"], "component": "ui.blogPost"},
            {"term": "блог", "synonyms": ["статья", "новость", "пост", "публикация"], "component": "ui.blogPost"},
            {"term": "список преимуществ", "synonyms": ["преимущества", "почему мы", "достоинства", "benefits"], "component": "ui.featuresList"},
            {"term": "вопрос-ответ", "synonyms": ["часто задаваемые вопросы", "faq"], "component": "ui.faq"},
            {"term": "цены", "synonyms": ["тарифы", "стоимость", "цены", "packages", "plans"], "component": "ui.pricingTable"},
            {"term": "тарифы", "synonyms": ["цены", "стоимость", "packages", "plans"], "component": "ui.pricingTable"},
            {"term": "контакты", "synonyms": ["контактная информация", "телефон", "адрес", "email"], "component": "ui.contactsBlock"},
            {"term": "отзывы", "synonyms": ["отзывы", "мнения клиентов", "feedback"], "component": "ui.testimonials"},
            {"term": "партнёры", "synonyms": ["партнеры", "клиенты", "brands"], "component": "ui.partnersLogos"},
            {"term": "этапы", "synonyms": ["шаги работы", "этапы", "workflow"], "component": "ui.steps"},
            {"term": "шаги", "synonyms": ["этапы", "workflow"], "component": "ui.steps"},
            {"term": "процесс", "synonyms": ["этапы", "шаги", "workflow"], "component": "ui.steps"},
            {"term": "таймлайн", "synonyms": ["история", "chronology", "события"], "component": "ui.timeline"},
            {"term": "история компании", "synonyms": ["таймлайн", "chronology", "события"], "component": "ui.timeline"},
            {"term": "достижения", "synonyms": ["цифры", "показатели", "факты"], "component": "ui.statsBlock"},
            {"term": "метрики", "synonyms": ["цифры", "показатели", "факты"], "component": "ui.statsBlock"},
            {"term": "статистика", "synonyms": ["цифры", "показатели", "факты"], "component": "ui.statsBlock"},
            
            # Advanced термины
            {"term": "поиск с автодополнением", "synonyms": ["подсказки поиска", "умный поиск"], "component": "ui.searchAutocomplete"},
            {"term": "фильтр диапазона", "synonyms": ["диапазон цен", "от и до", "slider filter"], "component": "ui.rangeFilter"},
            {"term": "выпадающее меню", "synonyms": ["выпадающий список", "select menu"], "component": "ui.dropdown"},
            {"term": "пошаговая форма", "synonyms": ["форма с шагами", "wizard form"], "component": "ui.stepForm"},
            {"term": "капча", "synonyms": ["проверка", "я не робот", "recaptcha"], "component": "ui.captcha"},
            {"term": "уведомление", "synonyms": ["алерт", "уведомление", "alert", "message"], "component": "ui.notification"},
            {"term": "toast", "synonyms": ["всплывающее уведомление", "toast message"], "component": "ui.toast"},
            {"term": "progress bar", "synonyms": ["прогресс", "индикатор выполнения"], "component": "ui.progressBar"},
            {"term": "rating", "synonyms": ["звезды", "рейтинг", "оценка"], "component": "ui.rating"},
            {"term": "slider input", "synonyms": ["ползунок", "слайдер", "range input"], "component": "ui.rangeSlider"},
            
            # Media термины
            {"term": "видео", "synonyms": ["видеофайл", "видео блок", "ролик", "video player"], "component": "ui.video"},
            {"term": "аудио", "synonyms": ["подкаст", "аудиоплеер", "audio player"], "component": "ui.audio"},
            {"term": "галерея изображений", "synonyms": ["галерея", "набор картинок"], "component": "ui.imageGallery"},
            {"term": "фон", "synonyms": ["обложка", "фон страницы"], "component": "ui.background"},
            {"term": "обложка", "synonyms": ["фон", "фон страницы"], "component": "ui.cover"},
            {"term": "инфографика", "synonyms": ["схема", "диаграмма", "визуализация"], "component": "ui.infographic"},
            {"term": "карта", "synonyms": ["карта", "местоположение", "адрес", "Google Map", "Yandex Map"], "component": "ui.map"},
            
            # Business термины
            {"term": "услуги", "synonyms": ["сервисы", "каталог услуг", "направления"], "component": "ui.servicesGrid"},
            {"term": "сервисы", "synonyms": ["услуги", "каталог услуг", "направления"], "component": "ui.servicesGrid"},
            {"term": "команда", "synonyms": ["сотрудники", "наша команда", "people"], "component": "ui.team"},
            {"term": "вакансии", "synonyms": ["работа", "карьера"], "component": "ui.vacancies"},
            {"term": "партнёрство", "synonyms": ["сотрудничество", "партнерство", "франшиза"], "component": "ui.franchise"},
            {"term": "франшиза", "synonyms": ["сотрудничество", "партнерство", "партнёрство"], "component": "ui.franchise"},
            {"term": "контактная форма", "synonyms": ["обратная связь", "форма связи"], "component": "ui.contactForm"},
            {"term": "форма подписки", "synonyms": ["подписка", "рассылка", "newsletter"], "component": "ui.subscribeForm"},
            {"term": "форма заявки", "synonyms": ["оставить заявку", "запрос", "order form"], "component": "ui.requestForm"},
            {"term": "платёж", "synonyms": ["оплата", "checkout", "billing"], "component": "ui.paymentForm"},
            {"term": "расчёт стоимости", "synonyms": ["калькулятор", "рассчитать цену"], "component": "ui.calculator"},
            {"term": "блог", "synonyms": ["новости", "лента новостей", "посты"], "component": "ui.blogGrid"},
            {"term": "новости", "synonyms": ["блог", "лента новостей", "посты"], "component": "ui.blogGrid"},
            
            # Social & Legal термины
            {"term": "иконки соцсетей", "synonyms": ["соцсети", "social icons", "follow us"], "component": "ui.socialIcons"},
            {"term": "share-кнопки", "synonyms": ["поделиться", "share"], "component": "ui.shareButtons"},
            {"term": "footer menu", "synonyms": ["нижнее меню", "подвал сайта"], "component": "ui.footerMenu"},
            {"term": "cookies banner", "synonyms": ["cookie согласие", "политика cookies"], "component": "ui.cookiesBanner"},
            {"term": "legal", "synonyms": ["политика", "соглашение", "terms"], "component": "ui.legalLinks"},
            {"term": "privacy", "synonyms": ["политика", "соглашение", "terms"], "component": "ui.legalLinks"},
            
            # Data термины
            {"term": "таблица данных", "synonyms": ["таблица", "таблица данных"], "component": "ui.dataTable"},
            {"term": "график времени", "synonyms": ["time graph", "temporal chart"], "component": "ui.timeChart"},
            {"term": "фильтры по датам", "synonyms": ["выбор даты", "календарь"], "component": "ui.datePicker"},
            {"term": "аватар", "synonyms": ["фото профиля"], "component": "ui.avatar"},
            {"term": "badge", "synonyms": ["отметка", "бейдж", "label"], "component": "ui.badge"},
            {"term": "бейджик", "synonyms": ["отметка", "badge", "label"], "component": "ui.badge"},
            {"term": "tag", "synonyms": ["тэг", "ярлык", "метка"], "component": "ui.tag"},
            {"term": "метка", "synonyms": ["тэг", "ярлык", "tag"], "component": "ui.tag"},
        ]
        
        # Очищаем существующие термины и создаем новые
        db.query(Mapping).delete()
        db.query(Synonym).delete()
        db.query(Term).delete()
        
        for term_data in terms_data:
            # Создаем термин
            term = Term(
                term=term_data["term"],
                description=f"Термин для компонента {term_data['component']}"
            )
            db.add(term)
            db.flush()
            
            # Создаем синонимы
            for synonym_name in term_data["synonyms"]:
                synonym = Synonym(
                    term_id=term.id,
                    synonym=synonym_name
                )
                db.add(synonym)
            
            # Создаем маппинг с компонентом
            component = db.query(Component).filter(Component.name == term_data["component"]).first()
            if component:
                mapping = Mapping(
                    term_id=term.id,
                    component_id=component.id,
                    confidence=1.0
                )
                db.add(mapping)
        
        db.commit()
        print("✅ Расширенные термины созданы")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при инициализации данных: {e}")
        raise
    finally:
        db.close()

def main():
    """Основная функция"""
    print("🚀 Инициализация расширенной библиотеки терминов Mod3-v1")
    print("")
    
    init_database()
    init_extended_vocab()
    
    print("")
    print("✅ Расширенная библиотека терминов успешно инициализирована!")
    print("📊 Добавлено 100+ терминов с синонимами и компонентами")

if __name__ == "__main__":
    main()
