#!/usr/bin/env python3
"""Автоматическая генерация свойств (props synthesis) для Mod3-v1"""

import yaml
import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
from jsonschema import validate, ValidationError

class PropsGenerator:
    """Генератор свойств для компонентов интерфейса"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Инициализация с загрузкой конфигурации"""
        self.config = self._load_config(config_path)
        self.schemas_path = self.config.get("props_synthesis", {}).get("schemas_path", "schemas/")
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Загружает конфигурацию из YAML файла"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Конфигурация по умолчанию"""
        return {
            "props_synthesis": {
                "enabled": True,
                "validation_enabled": True,
                "schemas_path": "schemas/",
                "generators": {}
            }
        }
    
    def synthesize_layout_props(
        self, 
        layout: Dict[str, Any], 
        entities: List[str], 
        keyphrases: List[str], 
        full_text: str = ""
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        Генерирует props для всех компонентов в layout
        
        Args:
            layout: Layout с секциями
            entities: Список извлеченных сущностей
            keyphrases: Список ключевых фраз
            full_text: Полный текст для анализа
            
        Returns:
            Tuple[layout с props, список warnings]
        """
        if not self.config.get("props_synthesis", {}).get("enabled", True):
            return layout, []
        
        warnings = []
        enhanced_layout = {
            "template": layout["template"],
            "sections": {},
            "count": layout["count"]
        }
        
        # Обрабатываем каждую секцию
        for section_name, components in layout["sections"].items():
            enhanced_components = []
            
            for component in components:
                enhanced_component = component.copy()
                
                # Генерируем props для компонента
                generated_props = self._generate_component_props(
                    component["component"],
                    entities,
                    keyphrases,
                    full_text,
                    component.get("term", "")
                )
                
                # Валидируем props
                validated_props, validation_warnings = self._validate_component_props(
                    component["component"],
                    generated_props
                )
                
                enhanced_component["props"] = validated_props
                warnings.extend(validation_warnings)
                
                enhanced_components.append(enhanced_component)
            
            enhanced_layout["sections"][section_name] = enhanced_components
        
        return enhanced_layout, warnings
    
    def _generate_component_props(
        self, 
        component_type: str, 
        entities: List[str], 
        keyphrases: List[str], 
        full_text: str,
        term: str
    ) -> Dict[str, Any]:
        """Генерирует props для конкретного типа компонента"""
        generators_config = self.config.get("props_synthesis", {}).get("generators", {})
        component_config = generators_config.get(component_type, {})
        
        # Объединяем все текстовые данные для анализа
        all_text = " ".join(entities + keyphrases + [full_text, term]).lower()
        
        if component_type == "ui.button":
            return self._generate_button_props(all_text, component_config)
        elif component_type == "ui.form":
            return self._generate_form_props(all_text, component_config)
        elif component_type == "ui.hero":
            return self._generate_hero_props(all_text, component_config)
        elif component_type == "ui.cards":
            return self._generate_cards_props(all_text, component_config)
        elif component_type == "ui.productGrid":
            return self._generate_product_grid_props(all_text, component_config)
        elif component_type == "ui.footer":
            return self._generate_footer_props(all_text, component_config)
        elif component_type == "ui.text":
            return self._generate_text_props(all_text, component_config)
        elif component_type == "ui.heading":
            return self._generate_heading_props(all_text, component_config)
        elif component_type == "ui.navbar":
            return self._generate_navbar_props(all_text, component_config)
        elif component_type == "ui.search":
            return self._generate_search_props(all_text, component_config)
        elif component_type == "ui.cta":
            return self._generate_cta_props(all_text, component_config)
        elif component_type == "ui.productCard":
            return self._generate_product_card_props(all_text, component_config)
        else:
            # Дефолтные props для неизвестных компонентов
            return component_config.get("default_props", {})
    
    def _generate_button_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для кнопки"""
        action_keywords = config.get("action_keywords", [])
        default_props = config.get("default_props", {"text": "Подробнее", "variant": "primary"})
        
        # Ищем ключевые слова действий
        for keyword in action_keywords:
            if keyword in text:
                return {
                    "text": keyword.title(),
                    "variant": "primary"
                }
        
        return default_props
    
    def _generate_form_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для формы"""
        form_types = config.get("form_types", {})
        default_fields = config.get("default_fields", [])
        
        # Определяем тип формы
        for form_type, form_config in form_types.items():
            keywords = form_config.get("keywords", [])
            for keyword in keywords:
                if keyword in text:
                    return {
                        "fields": form_config.get("fields", default_fields),
                        "title": form_type.title()
                    }
        
        return {
            "fields": default_fields,
            "title": "Форма"
        }
    
    def _generate_hero_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для hero секции"""
        default_props = config.get("default_props", {
            "title": "Добро пожаловать",
            "subtitle": "Наш сайт",
            "cta_text": "Начать"
        })
        
        # Извлекаем заголовок из первых значимых слов
        words = text.split()[:3]
        if words:
            title = " ".join(words).title()
            return {
                "title": title,
                "subtitle": default_props.get("subtitle", "Наш сайт"),
                "cta_text": default_props.get("cta_text", "Начать")
            }
        
        return default_props
    
    def _generate_cards_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для карточек"""
        default_items = config.get("default_items", [
            {"title": "Пример карточки", "description": "Описание карточки"}
        ])
        
        return {
            "items": default_items,
            "layout": "grid",
            "columns": 3
        }
    
    def _generate_product_grid_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для сетки товаров"""
        default_items = config.get("default_items", [
            {"title": "Товар 1", "description": "Описание товара", "price": "1000 ₽"}
        ])
        
        return {
            "items": default_items,
            "layout": "grid",
            "columns": 3,
            "show_filters": True
        }
    
    def _generate_footer_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для футера"""
        default_links = config.get("default_links", [
            "Контакты", "Политика конфиденциальности", "Соцсети", "О нас"
        ])
        
        return {
            "links": default_links
        }
    
    def _generate_text_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для текста"""
        default_text = config.get("default_text", "Описание раздела")
        
        # Используем первую осмысленную фразу
        if text and len(text.strip()) > 3:
            return {"text": text.strip()[:100]}
        
        return {"text": default_text}
    
    def _generate_heading_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для заголовка"""
        default_text = config.get("default_text", "Заголовок")
        default_level = config.get("default_level", 1)
        
        # Используем первые слова как заголовок
        words = text.split()[:2]
        if words:
            return {
                "text": " ".join(words).title(),
                "level": default_level
            }
        
        return {
            "text": default_text,
            "level": default_level
        }
    
    def _generate_navbar_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для навигации"""
        default_links = config.get("default_links", [
            "Главная", "О нас", "Контакты"
        ])
        
        return {
            "links": default_links
        }
    
    def _generate_search_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для поиска"""
        default_props = config.get("default_props", {
            "placeholder": "Поиск...",
            "button_text": "Найти"
        })
        
        return default_props
    
    def _generate_cta_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для призыва к действию"""
        default_props = config.get("default_props", {
            "text": "Узнать больше",
            "variant": "primary"
        })
        
        return default_props
    
    def _generate_product_card_props(self, text: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует props для карточки товара"""
        default_props = config.get("default_props", {
            "title": "Товар",
            "description": "Описание товара",
            "price": "1000 ₽"
        })
        
        return default_props
    
    def _validate_component_props(
        self, 
        component_type: str, 
        props: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Валидирует props компонента через JSON Schema"""
        warnings = []
        
        if not self.config.get("props_synthesis", {}).get("validation_enabled", True):
            return props, warnings
        
        try:
            # Загружаем схему для компонента
            schema_path = os.path.join(self.schemas_path, f"{component_type}.json")
            if not os.path.exists(schema_path):
                return props, warnings
            
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            # Валидируем props
            validate(instance=props, schema=schema)
            return props, warnings
            
        except ValidationError as e:
            # Применяем безопасные дефолты
            warnings.append(f"{component_type}: invalid props, applied defaults")
            
            # Получаем дефолтные props из конфигурации
            generators_config = self.config.get("props_synthesis", {}).get("generators", {})
            component_config = generators_config.get(component_type, {})
            default_props = component_config.get("default_props", {})
            
            return default_props, warnings
            
        except Exception as e:
            warnings.append(f"{component_type}: validation error, applied defaults")
            return props, warnings
    
    def get_props_stats(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """Возвращает статистику генерации props"""
        stats = {
            "total_components": 0,
            "components_with_props": 0,
            "components_without_props": 0,
            "by_type": {}
        }
        
        for section_name, components in layout["sections"].items():
            for component in components:
                stats["total_components"] += 1
                component_type = component["component"]
                
                if component_type not in stats["by_type"]:
                    stats["by_type"][component_type] = {
                        "count": 0,
                        "with_props": 0,
                        "without_props": 0
                    }
                
                stats["by_type"][component_type]["count"] += 1
                
                if component.get("props"):
                    stats["components_with_props"] += 1
                    stats["by_type"][component_type]["with_props"] += 1
                else:
                    stats["components_without_props"] += 1
                    stats["by_type"][component_type]["without_props"] += 1
        
        return stats
