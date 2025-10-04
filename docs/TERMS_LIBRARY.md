# Библиотека терминов InterView системы

## Обзор

Данный документ содержит полную библиотеку терминов, используемых в системе InterView для сопоставления естественного языка с UI компонентами.

## Структура библиотеки

### 1. Mod2-v1: Словарь терминов (vocab.json)

**Расположение**: `Mod2-v1/config/vocab.json`

```json
{
  "vocab_version": "0.1.1",
  "terms": [
    {
      "lemma": "форма обратный связь",
      "aliases": ["форма обратной связи", "обратная связь", "форма связи", "contact form"],
      "element": "ContactForm"
    },
    {
      "lemma": "каталог услуга", 
      "aliases": ["каталог услуг", "каталог сервисов", "services catalog", "список услуг"],
      "element": "ServicesGrid"
    },
    {
      "lemma": "форма",
      "aliases": ["form"],
      "element": "ContactForm"
    }
  ]
}
```

### 2. Mod3-v1: Правила сопоставления (Simple Version)

**Расположение**: `Mod3-v1/simple_mod3.py`

```python
mapping_rules = {
    "заголовок": "ui.heading",
    "кнопка": "ui.button", 
    "форма": "ui.form",
    "герои": "ui.hero",
    "подвал": "ui.footer",
    "футер": "ui.footer",
    "текст": "ui.text"
}
```

### 2.1. Mod3-v1: Полный каталог терминов (Enhanced Version)

**Расположение**: `Mod3-v1/scripts/init_enhanced_data.py`

#### Hero/Splash термины:
- **герой** → `ui.hero` (синонимы: шапка, баннер)
- **добро пожаловать** → `ui.hero` (синонимы: приветствие)
- **сайт** → `ui.hero` (синонимы: вест, портал)

#### Content термины:
- **заголовок** → `ui.heading` (синонимы: титул, header)
- **текст** → `ui.text` (синонимы: описание, контент)
- **параграф** → `ui.text` (синонимы: абзац)

#### Action термины:
- **кнопка** → `ui.button` (синонимы: баттон, кнопочка)
- **отправить** → `ui.button` (синонимы: послать)

#### Form термины:
- **форма** → `ui.form` (синонимы: анкета)
- **поле ввода** → `ui.form` (синонимы: инпут)

#### Content structure термины:
- **карточка** → `ui.card` (синонимы: card)
- **контейнер** → `ui.container` (синонимы: обертка)

#### Footer термины:
- **подвал** → `ui.footer` (синонимы: футер, footer)
- **ссылки** → `ui.footer` (синонимы: линки)

#### Navigation термины:
- **навигация** → `ui.navbar` (синонимы: меню, navbar, шапка, навигационное меню)
- **поиск** → `ui.search` (синонимы: строка поиска, поиск товаров, search bar)
- **хлебная крошка** → `ui.breadcrumb` (синонимы: хлебные крошки, breadcrumb)

#### Content термины:
- **карточка** → `ui.card` (синонимы: карточка контента, card)
- **карточка товар** → `ui.productCard` (синонимы: карточка товара, product card)
- **сетка товар** → `ui.productGrid` (синонимы: каталог товаров, товарная сетка, витрина)
- **фильтр** → `ui.filters` (синонимы: фильтры, фасеты, по характеристикам)
- **корзина** → `ui.cart` (синонимы: корзина покупок, basket, cart)
- **призыв действие** → `ui.cta` (синонимы: призыв к действию, call to action, cta)
- **раздел** → `ui.section` (синонимы: секция, блок, section)
- **изображение** → `ui.image` (синонимы: картинка, баннер, image)
- **таблица** → `ui.table` (синонимы: табличка, table, листинг)
- **график** → `ui.chart` (синонимы: диаграмма, chart)
- **список** → `ui.list` (синонимы: bullet list, маркированный список)
- **сетка** → `ui.grid` (синонимы: layout grid, колонки)

#### Interactive термины:
- **вкладка** → `ui.tabs` (синонимы: вкладки, tabs)
- **аккордеон** → `ui.accordion` (синонимы: раскрывающийся список)
- **карусель** → `ui.carousel` (синонимы: слайдер, галерея)
- **модальное окно** → `ui.modal` (синонимы: диалог, popup, modal)
- **подсказка** → `ui.tooltip` (синонимы: tooltip, хинт)
- **popover** → `ui.popover` (синонимы: всплывающее окно, popover)

#### Form термины:
- **форма вход** → `ui.authForm` (синонимы: форма входа, логин, sign in)
- **форма регистрация** → `ui.registerForm` (синонимы: регистрация, sign up)
- **форма восстановление** → `ui.resetForm` (синонимы: сброс пароля, reset password)

#### Social термины:
- **соцсеть** → `ui.socialLinks` (синонимы: соцсети, socials)

#### Action термины (расширенные):
- **купить** → `ui.button` (синонимы: заказать, подписаться, узнать больше, отправить)
- **заказать** → `ui.button` (синонимы: купить, подписаться, узнать больше, отправить)
- **подписаться** → `ui.button` (синонимы: купить, заказать, узнать больше, отправить)
- **узнать больше** → `ui.button` (синонимы: купить, заказать, подписаться, отправить)

#### Layout термины:
- **сайдбар** → `ui.sidebar` (синонимы: боковая панель, side panel, панель фильтров, categories)
- **меню категорий** → `ui.categoryMenu` (синонимы: список категорий, категории, рубрики)
- **панель управления** → `ui.dashboardSidebar` (синонимы: панель администратора, навигация админки)
- **верхняя панель** → `ui.topbar` (синонимы: верхняя линия, topbar, header bar)
- **пагинация** → `ui.pagination` (синонимы: страницы, навигация по страницам, пагинатор, переход между страницами)
- **вкладка профиля** → `ui.profileMenu` (синонимы: профиль, личный кабинет, user menu)
- **breadcrumb расширенный** → `ui.breadcrumbAdvanced` (синонимы: путь, навигационный след)

#### Content Block термины:
- **описание** → `ui.descriptionBlock` (синонимы: about text, описание компании, описание услуги)
- **статья** → `ui.article` (синонимы: новость, блог, пост, публикация)
- **новость** → `ui.blogPost` (синонимы: статья, блог, пост, публикация)
- **блог** → `ui.blogPost` (синонимы: статья, новость, пост, публикация)
- **список преимуществ** → `ui.featuresList` (синонимы: преимущества, почему мы, достоинства, benefits)
- **вопрос-ответ** → `ui.faq` (синонимы: часто задаваемые вопросы, faq)
- **цены** → `ui.pricingTable` (синонимы: тарифы, стоимость, цены, packages, plans)
- **тарифы** → `ui.pricingTable` (синонимы: цены, стоимость, packages, plans)
- **контакты** → `ui.contactsBlock` (синонимы: контактная информация, телефон, адрес, email)
- **отзывы** → `ui.testimonials` (синонимы: отзывы, мнения клиентов, feedback)
- **партнёры** → `ui.partnersLogos` (синонимы: партнеры, клиенты, brands)
- **этапы** → `ui.steps` (синонимы: шаги работы, этапы, workflow)
- **шаги** → `ui.steps` (синонимы: этапы, workflow)
- **процесс** → `ui.steps` (синонимы: этапы, шаги, workflow)
- **таймлайн** → `ui.timeline` (синонимы: история, chronology, события)
- **история компании** → `ui.timeline` (синонимы: таймлайн, chronology, события)
- **достижения** → `ui.statsBlock` (синонимы: цифры, показатели, факты)
- **метрики** → `ui.statsBlock` (синонимы: цифры, показатели, факты)
- **статистика** → `ui.statsBlock` (синонимы: цифры, показатели, факты)

#### Advanced термины:
- **поиск с автодополнением** → `ui.searchAutocomplete` (синонимы: подсказки поиска, умный поиск)
- **фильтр диапазона** → `ui.rangeFilter` (синонимы: диапазон цен, от и до, slider filter)
- **выпадающее меню** → `ui.dropdown` (синонимы: выпадающий список, select menu)
- **пошаговая форма** → `ui.stepForm` (синонимы: форма с шагами, wizard form)
- **капча** → `ui.captcha` (синонимы: проверка, я не робот, recaptcha)
- **уведомление** → `ui.notification` (синонимы: алерт, уведомление, alert, message)
- **toast** → `ui.toast` (синонимы: всплывающее уведомление, toast message)
- **progress bar** → `ui.progressBar` (синонимы: прогресс, индикатор выполнения)
- **rating** → `ui.rating` (синонимы: звезды, рейтинг, оценка)
- **slider input** → `ui.rangeSlider` (синонимы: ползунок, слайдер, range input)

#### Media термины:
- **видео** → `ui.video` (синонимы: видеофайл, видео блок, ролик, video player)
- **аудио** → `ui.audio` (синонимы: подкаст, аудиоплеер, audio player)
- **галерея изображений** → `ui.imageGallery` (синонимы: галерея, набор картинок)
- **фон** → `ui.background` (синонимы: обложка, фон страницы)
- **обложка** → `ui.cover` (синонимы: фон, фон страницы)
- **инфографика** → `ui.infographic` (синонимы: схема, диаграмма, визуализация)
- **карта** → `ui.map` (синонимы: карта, местоположение, адрес, Google Map, Yandex Map)

#### Business термины:
- **услуги** → `ui.servicesGrid` (синонимы: сервисы, каталог услуг, направления)
- **сервисы** → `ui.servicesGrid` (синонимы: услуги, каталог услуг, направления)
- **команда** → `ui.team` (синонимы: сотрудники, наша команда, people)
- **вакансии** → `ui.vacancies` (синонимы: работа, карьера)
- **партнёрство** → `ui.franchise` (синонимы: сотрудничество, партнерство, франшиза)
- **франшиза** → `ui.franchise` (синонимы: сотрудничество, партнерство, партнёрство)
- **контактная форма** → `ui.contactForm` (синонимы: обратная связь, форма связи)
- **форма подписки** → `ui.subscribeForm` (синонимы: подписка, рассылка, newsletter)
- **форма заявки** → `ui.requestForm` (синонимы: оставить заявку, запрос, order form)
- **платёж** → `ui.paymentForm` (синонимы: оплата, checkout, billing)
- **расчёт стоимости** → `ui.calculator` (синонимы: калькулятор, рассчитать цену)
- **блог** → `ui.blogGrid` (синонимы: новости, лента новостей, посты)
- **новости** → `ui.blogGrid` (синонимы: блог, лента новостей, посты)

#### Social & Legal термины:
- **иконки соцсетей** → `ui.socialIcons` (синонимы: соцсети, social icons, follow us)
- **share-кнопки** → `ui.shareButtons` (синонимы: поделиться, share)
- **footer menu** → `ui.footerMenu` (синонимы: нижнее меню, подвал сайта)
- **cookies banner** → `ui.cookiesBanner` (синонимы: cookie согласие, политика cookies)
- **legal** → `ui.legalLinks` (синонимы: политика, соглашение, terms)
- **privacy** → `ui.legalLinks` (синонимы: политика, соглашение, terms)

#### Data термины:
- **таблица данных** → `ui.dataTable` (синонимы: таблица, таблица данных)
- **график времени** → `ui.timeChart` (синонимы: time graph, temporal chart)
- **фильтры по датам** → `ui.datePicker` (синонимы: выбор даты, календарь)
- **аватар** → `ui.avatar` (синонимы: фото профиля)
- **badge** → `ui.badge` (синонимы: отметка, бейдж, label)
- **бейджик** → `ui.badge` (синонимы: отметка, badge, label)
- **tag** → `ui.tag` (синонимы: тэг, ярлык, метка)
- **метка** → `ui.tag` (синонимы: тэг, ярлык, tag)

### 2.2. Mod3-v1: Базовые термины (Basic Version)

**Расположение**: `Mod3-v1/scripts/init_data.py`

- **кнопка** → `ui.button` (синонимы: button, кнопочка)
- **форма** → `ui.form` (синонимы: form, формочка)
- **обратная связь** → `ContactForm` (синонимы: contact, связь, контакт, feedback)
- **услуги** → `ServicesGrid` (синонимы: services, каталог, сервисы)

### 3. Mod3-v1: Расширенные правила категоризации

**Расположение**: `Mod3-v1/app/services/enhanced_layout_service.py`

#### Правила размещения по секциям:

**Hero секция (Branding/Splash):**
- `ui.hero` - Герой секция
- `ui.welcome` - Приветствие
- `ui.navbar` - Навигационная панель
- `ui.breadcrumb` - Хлебные крошки

**Main секция (Action/Content):**
- `ui.button` - Кнопка
- `ui.heading` - Заголовок
- `ui.text` - Текст
- `ui.paragraph` - Параграф
- `ui.image` - Изображение
- `ui.form` - Форма
- `ui.input` - Поле ввода
- `ui.textarea` - Текстовая область
- `ui.select` - Выпадающий список
- `ui.checkbox` - Чекбокс
- `ui.radio` - Радиокнопка
- `ui.switch` - Переключатель
- `ui.card` - Карточка
- `ui.table` - Таблица
- `ui.chart` - График
- `ui.list` - Список
- `ui.grid` - Сетка
- `ui.tabs` - Вкладки
- `ui.accordion` - Аккордеон
- `ui.carousel` - Карусель
- `ui.modal` - Модальное окно
- `ui.tooltip` - Подсказка
- `ui.popover` - Всплывающее окно

**Footer секция (Meta/Navigation):**
- `ui.footer` - Подвал
- `ui.sidebar` - Боковая панель
- `ui.menu` - Меню

### 4. Каталог компонентов Mod3-v1

**Расположение**: `Mod3-v1/simple_mod3.py`, `Mod3-v1/hybrid_scoring.py` и `Mod3-v1/scripts/init_enhanced_data.py`

#### Полный список компонентов (расширенный каталог):

**Основные компоненты (из hybrid_scoring.py):**
- `ui.hero` - Главный баннер
- `ui.navbar` - Навигационная панель
- `ui.search` - Поиск
- `ui.footer` - Подвал
- `ui.productGrid` - Сетка товаров
- `ui.filters` - Фильтры
- `ui.cart` - Корзина
- `ui.cards` - Сетка карточек
- `ui.section` - Секция контента
- `ui.heading` - Заголовок
- `ui.text` - Текст
- `ui.button` - Кнопка
- `ui.form` - Форма
- `ui.cta` - Призыв к действию
- `ui.productCard` - Карточка товара
- `ui.container` - Контейнер

**Navigation компоненты:**
- `ui.breadcrumb` - Хлебные крошки
- `ui.breadcrumbAdvanced` - Расширенные хлебные крошки
- `ui.sidebar` - Боковая панель
- `ui.categoryMenu` - Меню категорий
- `ui.dashboardSidebar` - Панель управления
- `ui.topbar` - Верхняя панель
- `ui.pagination` - Пагинация
- `ui.profileMenu` - Вкладка профиля

**Content компоненты:**
- `ui.card` - Карточка
- `ui.image` - Изображение
- `ui.table` - Таблица
- `ui.chart` - График
- `ui.list` - Список
- `ui.grid` - Сетка
- `ui.descriptionBlock` - Описание
- `ui.article` - Статья
- `ui.blogPost` - Новость/Блог
- `ui.featuresList` - Список преимуществ
- `ui.faq` - Вопрос-ответ
- `ui.pricingTable` - Цены/Тарифы
- `ui.contactsBlock` - Контакты
- `ui.testimonials` - Отзывы
- `ui.partnersLogos` - Партнёры
- `ui.steps` - Этапы/Шаги
- `ui.timeline` - Таймлайн
- `ui.statsBlock` - Достижения/Статистика

**Interactive компоненты:**
- `ui.tabs` - Вкладки
- `ui.accordion` - Аккордеон
- `ui.carousel` - Карусель
- `ui.modal` - Модальное окно
- `ui.tooltip` - Подсказка
- `ui.popover` - Всплывающее окно
- `ui.dropdown` - Выпадающее меню
- `ui.rangeSlider` - Слайдер

**Form компоненты:**
- `ui.authForm` - Форма входа
- `ui.registerForm` - Форма регистрации
- `ui.resetForm` - Форма восстановления
- `ui.contactForm` - Контактная форма
- `ui.subscribeForm` - Форма подписки
- `ui.requestForm` - Форма заявки
- `ui.paymentForm` - Платёж
- `ui.stepForm` - Пошаговая форма
- `ui.captcha` - Капча

**Advanced компоненты:**
- `ui.searchAutocomplete` - Поиск с автодополнением
- `ui.rangeFilter` - Фильтр диапазона
- `ui.notification` - Уведомление
- `ui.toast` - Toast уведомление
- `ui.progressBar` - Прогресс бар
- `ui.rating` - Рейтинг
- `ui.calculator` - Калькулятор

**Media компоненты:**
- `ui.video` - Видео
- `ui.audio` - Аудио
- `ui.imageGallery` - Галерея изображений
- `ui.background` - Фон
- `ui.cover` - Обложка
- `ui.infographic` - Инфографика
- `ui.map` - Карта

**Business компоненты:**
- `ui.servicesGrid` - Услуги/Сервисы
- `ui.team` - Команда
- `ui.vacancies` - Вакансии
- `ui.franchise` - Партнёрство/Франшиза
- `ui.blogGrid` - Блог/Новости

**Social & Legal компоненты:**
- `ui.socialLinks` - Соцсети
- `ui.socialIcons` - Иконки соцсетей
- `ui.shareButtons` - Share кнопки
- `ui.footerMenu` - Footer меню
- `ui.cookiesBanner` - Cookies баннер
- `ui.legalLinks` - Legal/Privacy ссылки

**Data компоненты:**
- `ui.dataTable` - Таблица данных
- `ui.timeChart` - График времени
- `ui.datePicker` - Фильтры по датам
- `ui.avatar` - Аватар
- `ui.badge` - Badge/Бейджик
- `ui.tag` - Tag/Метка

#### Основные компоненты с примерами:

**ui.hero** (Branding)
```json
{
  "name": "ui.hero",
  "category": "branding",
  "example_props": {
    "title": "Добро пожаловать",
    "subtitle": "Демо приложение",
    "ctas": [
      {"text": "Начать", "variant": "primary"}
    ]
  }
}
```

**ui.heading** (Content)
```json
{
  "name": "ui.heading",
  "category": "content", 
  "example_props": {
    "text": "Заголовок страницы",
    "level": 1
  }
}
```

**ui.button** (Action)
```json
{
  "name": "ui.button",
  "category": "action",
  "example_props": {
    "text": "Отправить",
    "variant": "primary"
  }
}
```

**ui.form** (Form)
```json
{
  "name": "ui.form",
  "category": "form",
  "example_props": {
    "fields": [
      {
        "name": "email",
        "label": "Email",
        "type": "email",
        "required": true
      }
    ],
    "submitText": "Отправить"
  }
}
```

**ui.container** (Layout)
```json
{
  "name": "ui.container",
  "category": "layout",
  "example_props": {
    "padding": "lg",
    "maxWidth": "xl"
  }
}
```

**ui.footer** (Meta)
```json
{
  "name": "ui.footer",
  "category": "meta",
  "example_props": {
    "links": ["О нас", "Контакты"]
  }
}
```

## Шаблоны интерфейсов (Mod3-v1)

### Доступные шаблоны

Система автоматически выбирает шаблон на основе анализа entities и keyphrases. Доступны следующие шаблоны:

#### 1. **ecommerce-landing** (Приоритет: 1)
**Триггеры**: интернет-магазин, каталог, товары, корзина, товар, продажа, магазин, ecommerce

**Компоненты в шаблоне:**
- Hero: `ui.hero`, `ui.search`
- Main: `ui.productGrid`, `ui.filters`, `ui.cta`
- Footer: `ui.footer`

**Структура секций:**

**Hero секция:**
- `ui.hero` - Главный баннер магазина
- `ui.search` - Поиск товаров

**Main секция:**
- `ui.productGrid` - Сетка товаров
- `ui.filters` - Фильтры товаров
- `ui.cta` - Призыв к действию

**Footer секция:**
- `ui.footer` - Подвал с ссылками

#### 2. **hero-main-footer** (Приоритет: 2)
**Триггеры**: меню, навигация, navbar, шапка, сайт, страница

**Компоненты в шаблоне:**
- Hero: `ui.hero`, `ui.navbar`
- Main: `ui.text`, `ui.button`, `ui.form`
- Footer: `ui.footer`

#### 3. **cards-landing** (Приоритет: 3)
**Триггеры**: портфолио, кейсы, наши работы, галерея, проекты, работы

**Компоненты в шаблоне:**
- Hero: `ui.hero`
- Main: `ui.cards`, `ui.text`
- Footer: `ui.footer`

#### 4. **one-column** (Приоритет: 4)
**Триггеры**: лендинг, промо, одностраничный, страница секциями, landing

**Компоненты в шаблоне:**
- Hero: `ui.hero`
- Main: `ui.section`, `ui.text`, `ui.button`
- Footer: `ui.footer`

### Алгоритм выбора шаблона

1. **Анализ триггеров**: Система анализирует все entities и keyphrases
2. **Подсчет совпадений**: Для каждого шаблона подсчитывается количество совпавших триггеров
3. **Выбор по приоритету**: При равенстве счетов выбирается шаблон с более высоким приоритетом
4. **Fallback**: Если триггеры не найдены, используется `hero-main-footer` по умолчанию

### Компоненты по секциям

#### Hero секция (Branding/Splash)
- `ui.hero` - Главный баннер
- `ui.navbar` - Навигационная панель
- `ui.search` - Поиск
- `ui.breadcrumb` - Хлебные крошки
- `ui.breadcrumbAdvanced` - Расширенные хлебные крошки
- `ui.topbar` - Верхняя панель
- `ui.profileMenu` - Вкладка профиля

#### Main секция (Action/Content)
**Основные компоненты:**
- `ui.button` - Кнопка
- `ui.heading` - Заголовок
- `ui.text` - Текст
- `ui.form` - Форма
- `ui.cta` - Призыв к действию
- `ui.section` - Секция контента
- `ui.container` - Контейнер

**Content компоненты:**
- `ui.card` - Карточка
- `ui.cards` - Сетка карточек
- `ui.productCard` - Карточка товара
- `ui.productGrid` - Сетка товаров
- `ui.image` - Изображение
- `ui.imageGallery` - Галерея изображений
- `ui.table` - Таблица
- `ui.dataTable` - Таблица данных
- `ui.chart` - График
- `ui.timeChart` - График времени
- `ui.list` - Список
- `ui.grid` - Сетка
- `ui.descriptionBlock` - Описание
- `ui.article` - Статья
- `ui.blogPost` - Новость/Блог
- `ui.blogGrid` - Блог/Новости
- `ui.featuresList` - Список преимуществ
- `ui.faq` - Вопрос-ответ
- `ui.pricingTable` - Цены/Тарифы
- `ui.contactsBlock` - Контакты
- `ui.testimonials` - Отзывы
- `ui.partnersLogos` - Партнёры
- `ui.steps` - Этапы/Шаги
- `ui.timeline` - Таймлайн
- `ui.statsBlock` - Достижения/Статистика

**Interactive компоненты:**
- `ui.tabs` - Вкладки
- `ui.accordion` - Аккордеон
- `ui.carousel` - Карусель
- `ui.modal` - Модальное окно
- `ui.tooltip` - Подсказка
- `ui.popover` - Всплывающее окно
- `ui.dropdown` - Выпадающее меню
- `ui.rangeSlider` - Слайдер

**Form компоненты:**
- `ui.authForm` - Форма входа
- `ui.registerForm` - Форма регистрации
- `ui.resetForm` - Форма восстановления
- `ui.contactForm` - Контактная форма
- `ui.subscribeForm` - Форма подписки
- `ui.requestForm` - Форма заявки
- `ui.paymentForm` - Платёж
- `ui.stepForm` - Пошаговая форма
- `ui.captcha` - Капча

**Advanced компоненты:**
- `ui.searchAutocomplete` - Поиск с автодополнением
- `ui.rangeFilter` - Фильтр диапазона
- `ui.filters` - Фильтры
- `ui.notification` - Уведомление
- `ui.toast` - Toast уведомление
- `ui.progressBar` - Прогресс бар
- `ui.rating` - Рейтинг
- `ui.calculator` - Калькулятор
- `ui.datePicker` - Фильтры по датам

**Media компоненты:**
- `ui.video` - Видео
- `ui.audio` - Аудио
- `ui.background` - Фон
- `ui.cover` - Обложка
- `ui.infographic` - Инфографика
- `ui.map` - Карта

**Business компоненты:**
- `ui.servicesGrid` - Услуги/Сервисы
- `ui.team` - Команда
- `ui.vacancies` - Вакансии
- `ui.franchise` - Партнёрство/Франшиза

**Data компоненты:**
- `ui.avatar` - Аватар
- `ui.badge` - Badge/Бейджик
- `ui.tag` - Tag/Метка

#### Footer секция (Meta/Navigation)
- `ui.footer` - Подвал
- `ui.sidebar` - Боковая панель
- `ui.categoryMenu` - Меню категорий
- `ui.dashboardSidebar` - Панель управления
- `ui.pagination` - Пагинация
- `ui.socialLinks` - Соцсети
- `ui.socialIcons` - Иконки соцсетей
- `ui.shareButtons` - Share кнопки
- `ui.footerMenu` - Footer меню
- `ui.cookiesBanner` - Cookies баннер
- `ui.legalLinks` - Legal/Privacy ссылки

## Алгоритмы сопоставления

### 1. Mod2-v1: Fuzzy Matching
- Использует библиотеку `rapidfuzz`
- Порог совпадения: настраиваемый (по умолчанию 0.8)
- Поддерживает нечеткий поиск по алиасам

### 2. Mod3-v1: Гибридный скоринг
1. **Точное совпадение** - поиск точных терминов (вес: 1.0)
2. **Нечеткий поиск** - fuzzy matching с rapidfuzz (вес: 0.7)
3. **Контекстный анализ** - анализ окружающего текста (вес: 0.5)
4. **Позиционные подсказки** - анализ позиции в тексте (вес: 0.3)
5. **Порог confidence**: 0.6 (настраивается)

### 3. Mod3-v1: Балансировка секций
После гибридного скоринга применяется балансировка секций:

1. **Ограничение размера секций**: Максимум 12 компонентов на секцию
2. **Дедупликация**: Удаление дубликатов по типу компонента (оставляется с наибольшим confidence)
3. **Ограничение повторов**: Максимум 2 повтора одного типа компонента
4. **Смысловая наполняемость**: Минимум 2 смысловых компонента в main секции
5. **Fallback компоненты**: Добавление заглушек при недостатке контента

### 4. Mod3-v1: Автоматическая генерация свойств (Props Synthesis)
После балансировки секций генерируются props для всех компонентов:

#### Генерация по типам компонентов:

**ui.button:**
- Анализ ключевых слов действий: "отправить", "связаться", "купить", "заказать"
- Генерация label из найденных глаголов
- Дефолт: "Подробнее"

**ui.form:**
- Определение типа формы по ключевым словам:
  - Регистрация: поля "Имя", "Email", "Пароль"
  - Вход: поля "Email", "Пароль"
  - Обратная связь: поля "Имя", "Email", "Сообщение"
- Дефолт: форма обратной связи

**ui.hero:**
- Извлечение title и subtitle из первых слов текста
- Дефолт: "Добро пожаловать", "Наш сайт"

**ui.cards/ui.productGrid:**
- Генерация примеров карточек/товаров
- Настройка layout и columns

**ui.footer:**
- Стандартные ссылки: "Контакты", "Политика конфиденциальности", "Соцсети"

**ui.text:**
- Первая осмысленная фраза из keyphrases
- Дефолт: "Описание раздела"

#### Валидация props:
- Проверка через JSON Schema для каждого типа компонента
- При ошибке валидации применяются безопасные дефолты
- Предупреждения добавляются в warnings[]

## База данных терминов (Mod3-v1)

### Таблицы:

**Components (Компоненты)**
```sql
CREATE TABLE components (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    component_type VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Terms (Термины)**
```sql
CREATE TABLE terms (
    id INTEGER PRIMARY KEY,
    term VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Synonyms (Синонимы)**
```sql
CREATE TABLE synonyms (
    id INTEGER PRIMARY KEY,
    term_id INTEGER REFERENCES terms(id),
    synonym VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Mappings (Сопоставления)**
```sql
CREATE TABLE mappings (
    id INTEGER PRIMARY KEY,
    term_id INTEGER REFERENCES terms(id),
    component_id INTEGER REFERENCES components(id),
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Feature Flags

### Mod3-v1 Feature Flags:
- `M3_REQUIRE_PROPS` - Обязательные свойства компонентов
- `M3_NAMES_NORMALIZE` - Нормализация имен компонентов
- `M3_DEDUP_BY_COMPONENT` - Дедупликация по компонентам
- `M3_AT_LEAST_ONE_MAIN` - Минимум один компонент в main
- `M3_FALLBACK_SECTIONS` - Fallback секции при пустом layout
- `M3_MAX_MATCHES` - Максимальное количество совпадений

## Примеры использования

### Полный workflow системы

#### 1. Входные данные:
```json
{
  "session_id": "test-ecommerce",
  "entities": ["интернет-магазин", "каталог", "товары", "корзина", "кнопка", "форма"],
  "keyphrases": ["магазин товаров", "купить сейчас", "оставьте заявку", "регистрация"]
}
```

#### 2. Результат полного пайплайна:
```json
{
  "status": "ok",
  "session_id": "test-ecommerce",
  "layout": {
    "template": "ecommerce-landing",
    "sections": {
      "hero": [
        {
          "component": "ui.hero",
          "props": {
            "title": "Интернет-магазин",
            "subtitle": "Добро пожаловать в наш магазин"
          },
          "confidence": 0.9,
          "match_type": "exact",
          "term": "интернет-магазин"
        },
        {
          "component": "ui.search",
          "props": {
            "placeholder": "Поиск товаров"
          },
          "confidence": 0.8,
          "match_type": "context",
          "term": "каталог"
        }
      ],
      "main": [
        {
          "component": "ui.productGrid",
          "props": {
            "items": [
              {"title": "Товар 1", "description": "Описание товара", "price": "1000 ₽"},
              {"title": "Товар 2", "description": "Описание товара", "price": "2000 ₽"},
              {"title": "Товар 3", "description": "Описание товара", "price": "3000 ₽"}
            ],
            "layout": "grid",
            "columns": 3,
            "show_filters": true
          },
          "confidence": 0.9,
          "match_type": "exact",
          "term": "товары"
        },
        {
          "component": "ui.button",
          "props": {
            "text": "Купить",
            "variant": "primary"
          },
          "confidence": 0.8,
          "match_type": "context",
          "term": "купить сейчас"
        },
        {
          "component": "ui.form",
          "props": {
            "fields": [
              {"name": "Имя", "type": "text", "required": true},
              {"name": "Email", "type": "email", "required": true},
              {"name": "Пароль", "type": "password", "required": true}
            ],
            "title": "Registration"
          },
          "confidence": 0.8,
          "match_type": "context",
          "term": "регистрация"
        }
      ],
      "footer": [
        {
          "component": "ui.footer",
          "props": {
            "links": ["О нас", "Контакты", "Доставка"]
          },
          "confidence": 0.7,
          "match_type": "template-skeleton",
          "term": "template-footer"
        }
      ]
    },
    "count": 6
  },
  "matches": [
    {
      "term": "интернет-магазин",
      "matched_component": "ui.hero",
      "match_type": "exact",
      "score": 0.9
    },
    {
      "term": "товары",
      "matched_component": "ui.productGrid",
      "match_type": "exact",
      "score": 0.9
    },
    {
      "term": "купить сейчас",
      "matched_component": "ui.button",
      "match_type": "context",
      "score": 0.8
    }
  ],
  "explanations": [
    "Выбран шаблон ecommerce-landing по триггерам: интернет-магазин, каталог, товары",
    "ui.hero: exact match для 'интернет-магазин' (score: 0.9)",
    "ui.productGrid: exact match для 'товары' (score: 0.9)",
    "ui.button: context match для 'купить сейчас' (score: 0.8)"
  ]
}
```

#### 3. Этапы обработки:

1. **Выбор шаблона**: Анализ триггеров → выбор `ecommerce-landing`
2. **Гибридный скоринг**: Точные совпадения + контекстный анализ
3. **Балансировка секций**: Ограничение размера, дедупликация, fallback
4. **Props synthesis**: Автоматическая генерация свойств для всех компонентов
5. **Валидация**: Проверка props через JSON Schema

## Расширение библиотеки

### Добавление новых терминов:

1. **В Mod2-v1**: Обновить `config/vocab.json`
2. **В Mod3-v1**: 
   - Добавить в `mapping_rules` (simple version)
   - Добавить в базу данных через `init_enhanced_data.py`
   - Обновить правила категоризации в `enhanced_layout_service.py`

### Добавление новых компонентов:

1. Определить категорию (branding/content/action/form/layout/meta)
2. Создать схему свойств (`props_schema`) в `schemas/`
3. Добавить примеры свойств (`example_props`)
4. Определить правила размещения по секциям
5. Обновить каталог компонентов
6. Добавить генератор props в `props_generator.py`

### Добавление новых шаблонов:

1. **Определить триггеры**: Добавить ключевые слова в `template_triggers`
2. **Создать скелет**: Определить структуру секций в `_get_template_skeleton`
3. **Настроить компоненты**: Указать какие компоненты входят в каждую секцию
4. **Обновить приоритеты**: Установить порядок выбора шаблона
5. **Добавить валидацию**: Обновить JSON Schema если необходимо

### Добавление новых генераторов props:

1. **Определить логику**: Создать метод генерации для нового типа компонента
2. **Добавить конфигурацию**: Обновить `config.yaml` с настройками генерации
3. **Создать схему**: Добавить JSON Schema для валидации props
4. **Протестировать**: Проверить работу генератора и валидации

## Версионирование

- **vocab_version**: "0.1.1" (Mod2-v1)
- **APP_VERSION**: "1.0.0" (все модули)
- **feature_flags**: настраиваются через ENV переменные

---

*Последнее обновление: 2025-10-04*
*Версия документа: 3.0.0*
*Добавлено: Шаблоны интерфейсов, балансировка секций, props synthesis, расширенная библиотека терминов (100+ терминов)*
