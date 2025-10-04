#!/usr/bin/env python3
"""Упрощенная версия Mod3-v1 для запуска с гибридным скорингом"""

import os
os.environ['DATABASE_URL'] = 'sqlite:///./mod3.db'
os.environ['MOD3_HOST'] = '0.0.0.0'
os.environ['MOD3_PORT'] = '9001'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from hybrid_scoring import HybridScoringEngine
from section_balancer import SectionBalancer
from props_generator import PropsGenerator

app = FastAPI(
    title="Mod3-v1 Simple",
    version="1.0.0",
    description="Visual Elements Mapping Service"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация движка гибридного скоринга
scoring_engine = HybridScoringEngine("config.yaml")
debug_scoring = os.getenv("DEBUG_SCORING", "false").lower() == "true"

# Инициализация балансировщика секций
section_balancer = SectionBalancer("config.yaml")

# Инициализация генератора свойств
props_generator = PropsGenerator("config.yaml")

@app.get("/healthz")
def health_check():
    return {
        "status": "ok",
        "service": "Mod3-v1",
        "version": "1.0.0",
        "database_url": "sqlite:///./mod3.db",
        "hybrid_scoring": {
            "enabled": True,
            "debug_mode": debug_scoring,
            "threshold": scoring_engine.config["scoring"]["threshold"],
            "weights": scoring_engine.config["scoring"]["weights"]
        },
        "section_balancing": {
            "enabled": True,
            "max_components_per_section": section_balancer.config["section_balancing"]["max_components_per_section"],
            "max_repeats_per_key": section_balancer.config["section_balancing"]["max_repeats_per_key"],
            "min_meaningful_main": section_balancer.config["section_balancing"]["min_meaningful_main"]
        },
        "props_synthesis": {
            "enabled": props_generator.config["props_synthesis"]["enabled"],
            "validation_enabled": props_generator.config["props_synthesis"]["validation_enabled"],
            "schemas_path": props_generator.config["props_synthesis"]["schemas_path"]
        },
        "feature_flags": {
            "require_props": True,
            "names_normalize": True,
            "dedup_by_component": True,
            "at_least_one_main": True,
            "fallback_sections": True,
            "max_matches": 6
        }
    }

@app.get("/")
def root():
    return {
        "message": "Mod3-v1 - Visual Elements Mapping Service",
        "version": "1.0.0",
        "docs": "/docs"
    }

class MappingRequest(BaseModel):
    session_id: str
    entities: List[str] = []
    keyphrases: List[str] = []
    template: Optional[str] = None

def _select_template_by_site_type(entities: List[str], keyphrases: List[str]) -> Dict[str, Any]:
    """Выбирает шаблон на основе типа сайта из entities и keyphrases"""
    
    # Объединяем все входные данные для анализа
    all_text = " ".join(entities + keyphrases).lower()
    
    # Определяем триггеры для каждого типа сайта
    template_triggers = {
        "ecommerce-landing": {
            "keywords": ["интернет-магазин", "каталог", "товары", "корзина", "товар", "продажа", "магазин", "ecommerce", "покупка", "заказ", "доставка", "оплата"],
            "priority": 1
        },
        "medical-clinic": {
            "keywords": ["клиника", "врач", "медицинский центр", "запись", "приём", "лечение", "анализы", "здоровье", "медицина", "доктор", "поликлиника"],
            "priority": 1
        },
        "education-portal": {
            "keywords": ["обучение", "курс", "программа", "преподаватель", "урок", "школа", "студенты", "образование", "учебный", "дисциплина"],
            "priority": 1
        },
        "job-board": {
            "keywords": ["работа", "вакансии", "карьера", "резюме", "отклик", "поиск работы", "трудоустройство", "должность"],
            "priority": 1
        },
        "event-landing": {
            "keywords": ["мероприятие", "событие", "конференция", "фестиваль", "регистрация", "билеты", "расписание", "встреча", "акция"],
            "priority": 1
        },
        "finance-services": {
            "keywords": ["банк", "кредит", "ипотека", "инвестиции", "страховка", "финансы", "проценты", "заявка", "финансовые услуги"],
            "priority": 1
        },
        "hero-main-footer": {
            "keywords": ["меню", "навигация", "navbar", "шапка", "сайт", "страница"],
            "priority": 2
        },
        "cards-landing": {
            "keywords": ["портфолио", "кейсы", "наши работы", "галерея", "проекты", "работы"],
            "priority": 3
        },
        "one-column": {
            "keywords": ["лендинг", "промо", "одностраничный", "страница секциями", "landing"],
            "priority": 4
        }
    }
    
    # Подсчитываем совпадения для каждого шаблона
    template_scores = {}
    matched_keywords = {}
    
    for template_name, config in template_triggers.items():
        score = 0
        matched = []
        for keyword in config["keywords"]:
            if keyword in all_text:
                score += 1
                matched.append(keyword)
        template_scores[template_name] = score
        matched_keywords[template_name] = matched
    
    # Выбираем шаблон с максимальным количеством совпадений
    max_score = max(template_scores.values()) if template_scores.values() else 0
    
    if max_score == 0:
        # Нет триггеров - используем hero-main-footer по умолчанию
        selected_template = "hero-main-footer"
        explanations = ["Выбран шаблон по умолчанию: hero-main-footer (триггеры не найдены)"]
    else:
        # Находим шаблоны с максимальным счетом
        max_templates = [name for name, score in template_scores.items() if score == max_score]
        
        if len(max_templates) == 1:
            selected_template = max_templates[0]
        else:
            # При равенстве выбираем по приоритету
            priority_order = ["ecommerce-landing", "medical-clinic", "education-portal", "job-board", "event-landing", "finance-services", "hero-main-footer", "cards-landing", "one-column"]
            for template_name in priority_order:
                if template_name in max_templates:
                    selected_template = template_name
                    break
        
        # Формируем объяснения
        matched = matched_keywords[selected_template]
        explanations = [f"Выбран шаблон {selected_template} по триггерам: {', '.join(matched)}"]
    
    return {
        "template": selected_template,
        "explanations": explanations
    }

def _get_template_skeleton(template_name: str) -> Dict[str, Any]:
    """Возвращает скелет секций для выбранного шаблона"""
    
    skeletons = {
        "ecommerce-landing": {
            "template": "ecommerce-landing",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Интернет-магазин", "subtitle": "Добро пожаловать в наш магазин"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.search",
                        "props": {"placeholder": "Поиск товаров"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-search"
                    }
                ],
                "main": [
                    {
                        "component": "ui.productGrid",
                        "props": {"title": "Каталог товаров"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-products"
                    },
                    {
                        "component": "ui.filters",
                        "props": {"title": "Фильтры"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-filters"
                    },
                    {
                        "component": "ui.cta",
                        "props": {"text": "Оформить заказ", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-cta"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О нас", "Контакты", "Доставка"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    }
                ]
            }
        },
        "hero-main-footer": {
            "template": "hero-main-footer",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Добро пожаловать", "subtitle": "Наш сайт"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.navbar",
                        "props": {"links": ["Главная", "О нас", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-navbar"
                    }
                ],
                "main": [
                    {
                        "component": "ui.text",
                        "props": {"text": "Основной контент"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-text"
                    },
                    {
                        "component": "ui.button",
                        "props": {"text": "Действие", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-button"
                    },
                    {
                        "component": "ui.form",
                        "props": {"fields": [{"name": "contact", "label": "Контакт", "type": "text"}]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-form"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О нас", "Контакты", "Помощь"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    }
                ]
            }
        },
        "cards-landing": {
            "template": "cards-landing",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Наши работы", "subtitle": "Портфолио"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    }
                ],
                "main": [
                    {
                        "component": "ui.cards",
                        "props": {"title": "Проекты", "layout": "grid"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-cards"
                    },
                    {
                        "component": "ui.text",
                        "props": {"text": "Описание работ"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-text"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О нас", "Контакты", "Услуги"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    }
                ]
            }
        },
        "one-column": {
            "template": "one-column",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Лендинг", "subtitle": "Промо страница"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    }
                ],
                "main": [
                    {
                        "component": "ui.section",
                        "props": {"title": "Секция 1"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-section1"
                    },
                    {
                        "component": "ui.text",
                        "props": {"text": "Описание"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-text"
                    },
                    {
                        "component": "ui.button",
                        "props": {"text": "Призыв к действию", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-button"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["Контакты", "Политика"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    }
                ]
            }
        },
        "medical-clinic": {
            "template": "medical-clinic",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Медицинская клиника", "subtitle": "Забота о вашем здоровье"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.navbar",
                        "props": {"links": ["Главная", "Услуги", "Врачи", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-navbar"
                    }
                ],
                "main": [
                    {
                        "component": "ui.servicesGrid",
                        "props": {"title": "Наши услуги"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-services"
                    },
                    {
                        "component": "ui.doctorsList",
                        "props": {"title": "Наши врачи"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-doctors"
                    },
                    {
                        "component": "ui.appointmentForm",
                        "props": {"title": "Запись на приём"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-appointment"
                    },
                    {
                        "component": "ui.testimonials",
                        "props": {"title": "Отзывы пациентов"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-testimonials"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О клинике", "Лицензии", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    },
                    {
                        "component": "ui.contacts",
                        "props": {"title": "Контакты"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-contacts"
                    }
                ]
            }
        },
        "education-portal": {
            "template": "education-portal",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Образовательная платформа", "subtitle": "Обучение нового поколения"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.navbar",
                        "props": {"links": ["Главная", "Курсы", "Преподаватели", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-navbar"
                    }
                ],
                "main": [
                    {
                        "component": "ui.courseList",
                        "props": {"title": "Наши курсы"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-courses"
                    },
                    {
                        "component": "ui.featuresList",
                        "props": {"title": "Преимущества обучения"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-features"
                    },
                    {
                        "component": "ui.testimonials",
                        "props": {"title": "Отзывы студентов"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-testimonials"
                    },
                    {
                        "component": "ui.cta",
                        "props": {"text": "Начать обучение", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-cta"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О платформе", "Помощь", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    },
                    {
                        "component": "ui.socialLinks",
                        "props": {"title": "Социальные сети"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-social"
                    }
                ]
            }
        },
        "job-board": {
            "template": "job-board",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Поиск работы", "subtitle": "Найдите работу своей мечты"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.search",
                        "props": {"placeholder": "Поиск вакансий"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-search"
                    }
                ],
                "main": [
                    {
                        "component": "ui.jobList",
                        "props": {"title": "Актуальные вакансии"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-jobs"
                    },
                    {
                        "component": "ui.filters",
                        "props": {"title": "Фильтры поиска"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-filters"
                    },
                    {
                        "component": "ui.cta",
                        "props": {"text": "Разместить резюме", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-cta"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О компании", "Работодателям", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    },
                    {
                        "component": "ui.contacts",
                        "props": {"title": "Контакты"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-contacts"
                    }
                ]
            }
        },
        "event-landing": {
            "template": "event-landing",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Мероприятие", "subtitle": "Присоединяйтесь к нам"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.cta",
                        "props": {"text": "Зарегистрироваться", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-cta"
                    },
                    {
                        "component": "ui.countdown",
                        "props": {"title": "До начала мероприятия"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-countdown"
                    }
                ],
                "main": [
                    {
                        "component": "ui.schedule",
                        "props": {"title": "Программа мероприятия"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-schedule"
                    },
                    {
                        "component": "ui.speakers",
                        "props": {"title": "Спикеры"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-speakers"
                    },
                    {
                        "component": "ui.tickets",
                        "props": {"title": "Билеты"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-tickets"
                    },
                    {
                        "component": "ui.gallery",
                        "props": {"title": "Галерея"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-gallery"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О мероприятии", "Спонсоры", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    },
                    {
                        "component": "ui.contacts",
                        "props": {"title": "Контакты"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-contacts"
                    }
                ]
            }
        },
        "finance-services": {
            "template": "finance-services",
            "sections": {
                "hero": [
                    {
                        "component": "ui.hero",
                        "props": {"title": "Финансовые услуги", "subtitle": "Надёжные финансовые решения"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-hero"
                    },
                    {
                        "component": "ui.navbar",
                        "props": {"links": ["Главная", "Услуги", "Калькулятор", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-navbar"
                    }
                ],
                "main": [
                    {
                        "component": "ui.servicesGrid",
                        "props": {"title": "Наши услуги"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-services"
                    },
                    {
                        "component": "ui.calculator",
                        "props": {"title": "Калькулятор"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-calculator"
                    },
                    {
                        "component": "ui.cta",
                        "props": {"text": "Подать заявку", "variant": "primary"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-cta"
                    },
                    {
                        "component": "ui.testimonials",
                        "props": {"title": "Отзывы клиентов"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-testimonials"
                    }
                ],
                "footer": [
                    {
                        "component": "ui.footer",
                        "props": {"links": ["О компании", "Лицензии", "Контакты"]},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-footer"
                    },
                    {
                        "component": "ui.contacts",
                        "props": {"title": "Контакты"},
                        "confidence": 0.51,
                        "match_type": "template-skeleton",
                        "term": "template-contacts"
                    }
                ]
            }
        }
    }
    
    return skeletons.get(template_name, skeletons["hero-main-footer"])

def _merge_template_with_mappings(skeleton: Dict[str, Any], mapped_components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Объединяет скелет шаблона с найденными компонентами"""
    
    # Копируем скелет
    final_layout = {
        "template": skeleton["template"],
        "sections": {
            "hero": skeleton["sections"]["hero"].copy(),
            "main": skeleton["sections"]["main"].copy(),
            "footer": skeleton["sections"]["footer"].copy()
        }
    }
    
    # Правила размещения компонентов по секциям
    section_rules = {
        "ui.hero": "hero",
        "ui.navbar": "hero",
        "ui.search": "hero",
        "ui.countdown": "hero",
        "ui.footer": "footer",
        "ui.contacts": "footer",
        "ui.socialLinks": "footer",
        "ui.productGrid": "main",
        "ui.filters": "main",
        "ui.cart": "main",
        "ui.cards": "main",
        "ui.section": "main",
        "ui.heading": "main",
        "ui.text": "main",
        "ui.button": "main",
        "ui.form": "main",
        "ui.cta": "main",
        "ui.servicesGrid": "main",
        "ui.doctorsList": "main",
        "ui.appointmentForm": "main",
        "ui.courseList": "main",
        "ui.featuresList": "main",
        "ui.jobList": "main",
        "ui.schedule": "main",
        "ui.speakers": "main",
        "ui.tickets": "main",
        "ui.gallery": "main",
        "ui.calculator": "main",
        "ui.testimonials": "main"
    }
    
    # Добавляем найденные компоненты в соответствующие секции
    for component in mapped_components:
        component_name = component["component"]
        target_section = section_rules.get(component_name, "main")
        
        # Проверяем на дубликаты по типу компонента
        existing_components = final_layout["sections"][target_section]
        duplicate_found = False
        
        for i, existing in enumerate(existing_components):
            if existing["component"] == component_name:
                # Заменяем на компонент с большим confidence
                if component["confidence"] > existing["confidence"]:
                    existing_components[i] = component
                duplicate_found = True
                break
        
        if not duplicate_found:
            final_layout["sections"][target_section].append(component)
    
    # Подсчитываем общее количество компонентов
    total_count = sum(len(components) for components in final_layout["sections"].values())
    final_layout["count"] = total_count
    
    return final_layout

@app.post("/v1/map")
def map_entities_to_layout(request: MappingRequest):
    """Улучшенное сопоставление entities с компонентами с автоматическим выбором шаблона"""
    
    # 1. Определяем тип сайта и выбираем шаблон
    template_info = _select_template_by_site_type(request.entities, request.keyphrases)
    selected_template = template_info["template"]
    template_explanations = template_info["explanations"]
    
    # 2. Инициализируем layout скелетом выбранного шаблона
    layout_skeleton = _get_template_skeleton(selected_template)
    
    # 3. Гибридный скоринг компонентов
    # Объединяем все текстовые данные для контекста
    context_text = " ".join(request.entities + request.keyphrases)
    
    # Извлекаем позиционные подсказки из entities и keyphrases
    position_hints = []
    position_keywords = ["вверху", "сверху", "внизу", "снизу", "в центре", "посередине", "в начале", "в конце"]
    for entity in request.entities + request.keyphrases:
        for keyword in position_keywords:
            if keyword in entity.lower():
                position_hints.append(entity)
                break
    
    # Применяем гибридный скоринг
    scored_components = scoring_engine.score_components(
        entities=request.entities,
        keyphrases=request.keyphrases,
        context_text=context_text,
        position_hints=position_hints
    )
    
    # Фильтруем компоненты по порогу и ограничиваем количество
    max_matches = int(os.getenv("M3_MAX_MATCHES", "6"))
    filtered_components = [
        comp for comp in scored_components 
        if comp["passed_threshold"]
    ][:max_matches]
    
    # Формируем объяснения для скоринга
    mapping_explanations = []
    for comp in filtered_components:
        explanation = {
            "term": comp["term"],
            "matched_component": comp["component"],
            "match_type": comp["match_type"],
            "score": comp["confidence"]
        }
        
        # Добавляем детализацию в отладочном режиме
        if debug_scoring and "breakdown" in comp:
            explanation["breakdown"] = comp["breakdown"]
        
        mapping_explanations.append(explanation)
    
    # 4. Объединяем скелет шаблона с найденными компонентами
    final_layout = _merge_template_with_mappings(layout_skeleton, filtered_components)
    
    # 5. Балансируем секции и ограничиваем повторы
    balanced_layout = section_balancer.balance_layout_sections(final_layout)
    
    # 6. Генерируем props для всех компонентов
    enhanced_layout, props_warnings = props_generator.synthesize_layout_props(
        balanced_layout,
        request.entities,
        request.keyphrases,
        context_text
    )
    
    # 7. Объединяем объяснения
    all_explanations = template_explanations + mapping_explanations
    
    # Формируем финальный ответ
    response = {
        "status": "ok",
        "session_id": request.session_id,
        "layout": enhanced_layout,
        "matches": filtered_components,
        "explanations": all_explanations
    }
    
    # Добавляем warnings если есть
    all_warnings = []
    if "warnings" in balanced_layout:
        all_warnings.extend(balanced_layout["warnings"])
    all_warnings.extend(props_warnings)
    
    if all_warnings:
        response["warnings"] = all_warnings
    
    return response

@app.get("/v1/components")
def get_components():
    """Возвращает каталог компонентов"""
    
    components = [
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
        },
        {
            "name": "ui.heading",
            "category": "content",
            "example_props": {
                "text": "Заголовок страницы",
                "level": 1
            }
        },
        {
            "name": "ui.button",
            "category": "action",
            "example_props": {
                "text": "Отправить",
                "variant": "primary"
            }
        },
        {
            "name": "ui.form",
            "category": "form", 
            "example_props": {
                "fields": [
                    {
                        "name": "email",
                        "label": "Email",
                        "type": "email",
                        "required": True
                    }
                ],
                "submitText": "Отправить"
            }
        },
        {
            "name": "ui.footer",
            "category": "meta",
            "example_props": {
                "links": ["О нас", "Контакты"]
            }
        }
    ]
    
    return {
        "status": "ok",
        "components": components
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Mod3-v1 Simple запущен на порту 9001")
    uvicorn.run(app, host="0.0.0.0", port=9001, log_level="info")
