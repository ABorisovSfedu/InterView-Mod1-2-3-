#!/usr/bin/env python3
"""Гибридный скоринг для Mod3-v1"""

import yaml
import os
from typing import Dict, List, Any, Tuple, Optional
from rapidfuzz import fuzz
import re

class HybridScoringEngine:
    """Движок гибридного скоринга для компонентов интерфейса"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Инициализация с загрузкой конфигурации"""
        self.config = self._load_config(config_path)
        self.debug_mode = os.getenv("DEBUG_SCORING", "false").lower() == "true"
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Загружает конфигурацию из YAML файла"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Возвращаем конфигурацию по умолчанию
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Конфигурация по умолчанию"""
        return {
            "scoring": {
                "weights": {
                    "exact": 1.0,
                    "fuzzy": 0.7,
                    "context": 0.5,
                    "position": 0.3
                },
                "threshold": 0.6,
                "debug": False
            },
            "context_triggers": {},
            "position_triggers": {},
            "scoring_rules": {
                "min_confidence": 0.51,
                "max_confidence": 0.95,
                "multiple_match_bonus": 0.1,
                "generic_penalty": {
                    "terms": ["сайт", "страница", "элемент", "компонент", "часть"],
                    "penalty": 0.2
                }
            }
        }
    
    def calculate_hybrid_score(
        self, 
        term: str, 
        component: str, 
        context_text: str = "",
        position_hint: str = ""
    ) -> Dict[str, Any]:
        """
        Вычисляет гибридный score для компонента
        
        Args:
            term: Термин для сопоставления
            component: Компонент интерфейса (например, "ui.button")
            context_text: Контекстный текст вокруг термина
            position_hint: Подсказка о позиции элемента
            
        Returns:
            Словарь с результатами скоринга
        """
        weights = self.config["scoring"]["weights"]
        
        # 1. Exact matching (точное совпадение)
        exact_score = self._calculate_exact_score(term, component)
        
        # 2. Fuzzy matching (приблизительное совпадение)
        fuzzy_score = self._calculate_fuzzy_score(term, component)
        
        # 3. Context scoring (контекстные фразы)
        context_score = self._calculate_context_score(term, component, context_text)
        
        # 4. Position scoring (позиционные подсказки)
        position_score = self._calculate_position_score(component, position_hint)
        
        # Вычисляем итоговый score
        total_score = (
            weights["exact"] * exact_score +
            weights["fuzzy"] * fuzzy_score +
            weights["context"] * context_score +
            weights["position"] * position_score
        )
        
        # Применяем правила скоринга
        total_score = self._apply_scoring_rules(total_score, term, component)
        
        # Формируем результат
        result = {
            "score": total_score,
            "confidence": min(max(total_score, 0.0), 1.0),
            "passed_threshold": total_score >= self.config["scoring"]["threshold"]
        }
        
        # Добавляем детализацию в отладочном режиме
        if self.debug_mode or self.config["scoring"]["debug"]:
            result["breakdown"] = {
                "exact": exact_score,
                "fuzzy": fuzzy_score,
                "context": context_score,
                "position": position_score,
                "weights": weights,
                "total_calculation": f"{weights['exact']}×{exact_score:.2f} + {weights['fuzzy']}×{fuzzy_score:.2f} + {weights['context']}×{context_score:.2f} + {weights['position']}×{position_score:.2f} = {total_score:.2f}"
            }
        
        return result
    
    def _calculate_exact_score(self, term: str, component: str) -> float:
        """Вычисляет score для точного совпадения"""
        # Базовые правила сопоставления
        mapping_rules = {
            "заголовок": "ui.heading",
            "кнопка": "ui.button", 
            "форма": "ui.form",
            "герои": "ui.hero",
            "подвал": "ui.footer",
            "футер": "ui.footer",
            "текст": "ui.text",
            "товар": "ui.productCard",
            "каталог": "ui.productGrid",
            "корзина": "ui.cart",
            "меню": "ui.navbar",
            "навигация": "ui.navbar",
            "шапка": "ui.navbar",
            "лендинг": "ui.section",
            "промо": "ui.section",
            "одностраничный": "ui.section",
            "страница секциями": "ui.section",
            "landing": "ui.section",
            "портфолио": "ui.cards",
            "кейсы": "ui.cards",
            "наши работы": "ui.cards",
            "галерея": "ui.cards",
            "проекты": "ui.cards",
            "работы": "ui.cards",
            "интернет-магазин": "ui.productGrid",
            "ecommerce": "ui.productGrid",
            "сайт": "ui.container",
            "страница": "ui.container"
        }
        
        term_lower = term.lower().strip()
        for mapped_term, mapped_component in mapping_rules.items():
            if mapped_term in term_lower and mapped_component == component:
                return 1.0
        
        return 0.0
    
    def _calculate_fuzzy_score(self, term: str, component: str) -> float:
        """Вычисляет score для приблизительного совпадения"""
        # Получаем список всех возможных терминов для компонента
        component_terms = self._get_component_terms(component)
        
        if not component_terms:
            return 0.0
        
        # Вычисляем максимальное fuzzy совпадение
        max_score = 0.0
        for comp_term in component_terms:
            score = fuzz.token_set_ratio(term.lower(), comp_term.lower()) / 100.0
            max_score = max(max_score, score)
        
        return max_score
    
    def _get_component_terms(self, component: str) -> List[str]:
        """Возвращает список терминов, связанных с компонентом"""
        mapping_rules = {
            "ui.heading": ["заголовок", "title", "heading", "h1", "h2", "h3"],
            "ui.button": ["кнопка", "button", "btn", "ссылка", "link"],
            "ui.form": ["форма", "form", "поля", "fields", "input"],
            "ui.hero": ["герои", "hero", "баннер", "banner", "заголовок"],
            "ui.footer": ["подвал", "футер", "footer", "низ", "bottom"],
            "ui.text": ["текст", "text", "параграф", "paragraph", "описание"],
            "ui.productCard": ["товар", "product", "карточка", "card"],
            "ui.productGrid": ["каталог", "catalog", "сетка", "grid", "товары"],
            "ui.cart": ["корзина", "cart", "basket", "покупки"],
            "ui.navbar": ["меню", "навигация", "navbar", "шапка", "header"],
            "ui.section": ["секция", "section", "блок", "block", "раздел"],
            "ui.cards": ["карточки", "cards", "портфолио", "portfolio"],
            "ui.container": ["контейнер", "container", "обертка", "wrapper"]
        }
        
        return mapping_rules.get(component, [])
    
    def _calculate_context_score(self, term: str, component: str, context_text: str) -> float:
        """Вычисляет score на основе контекстных фраз"""
        if not context_text:
            return 0.0
        
        context_triggers = self.config.get("context_triggers", {})
        component_triggers = context_triggers.get(component, [])
        
        if not component_triggers:
            return 0.0
        
        context_lower = context_text.lower()
        matches = 0
        
        for trigger in component_triggers:
            if trigger.lower() in context_lower:
                matches += 1
        
        # Нормализуем score (максимум 1.0)
        return min(matches * 0.3, 1.0)
    
    def _calculate_position_score(self, component: str, position_hint: str) -> float:
        """Вычисляет score на основе позиционных подсказок"""
        if not position_hint:
            return 0.0
        
        position_triggers = self.config.get("position_triggers", {})
        
        # Определяем секцию компонента
        section_rules = {
            "ui.hero": "hero",
            "ui.navbar": "hero", 
            "ui.search": "hero",
            "ui.footer": "footer",
            "ui.productGrid": "main",
            "ui.filters": "main",
            "ui.cart": "main",
            "ui.cards": "main",
            "ui.section": "main",
            "ui.heading": "main",
            "ui.text": "main",
            "ui.button": "main",
            "ui.form": "main",
            "ui.cta": "main"
        }
        
        component_section = section_rules.get(component, "main")
        section_triggers = position_triggers.get(component_section, [])
        
        if not section_triggers:
            return 0.0
        
        position_lower = position_hint.lower()
        matches = 0
        
        for trigger in section_triggers:
            if trigger.lower() in position_lower:
                matches += 1
        
        # Нормализуем score (максимум 1.0)
        return min(matches * 0.4, 1.0)
    
    def _apply_scoring_rules(self, score: float, term: str, component: str) -> float:
        """Применяет дополнительные правила скоринга"""
        rules = self.config.get("scoring_rules", {})
        
        # Применяем минимальный и максимальный confidence
        min_conf = rules.get("min_confidence", 0.51)
        max_conf = rules.get("max_confidence", 0.95)
        
        score = max(score, min_conf)
        score = min(score, max_conf)
        
        # Применяем штраф за общие термины
        generic_penalty = rules.get("generic_penalty", {})
        generic_terms = generic_penalty.get("terms", [])
        penalty = generic_penalty.get("penalty", 0.2)
        
        term_lower = term.lower()
        for generic_term in generic_terms:
            if generic_term in term_lower:
                score -= penalty
                break
        
        return max(score, 0.0)
    
    def score_components(
        self, 
        entities: List[str], 
        keyphrases: List[str], 
        context_text: str = "",
        position_hints: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Оценивает все возможные компоненты для заданных entities и keyphrases
        
        Args:
            entities: Список извлеченных сущностей
            keyphrases: Список ключевых фраз
            context_text: Контекстный текст
            position_hints: Подсказки о позиции элементов
            
        Returns:
            Список компонентов с оценками, отсортированный по убыванию score
        """
        if position_hints is None:
            position_hints = []
        
        all_terms = entities + keyphrases
        scored_components = []
        
        # Список всех возможных компонентов
        all_components = [
            "ui.hero", "ui.navbar", "ui.search", "ui.footer",
            "ui.productGrid", "ui.filters", "ui.cart", "ui.cards",
            "ui.section", "ui.heading", "ui.text", "ui.button",
            "ui.form", "ui.cta", "ui.productCard", "ui.container"
        ]
        
        for component in all_components:
            max_score = 0.0
            best_term = ""
            best_breakdown = {}
            
            for term in all_terms:
                # Объединяем все подсказки о позиции
                combined_position = " ".join(position_hints)
                
                result = self.calculate_hybrid_score(
                    term, component, context_text, combined_position
                )
                
                if result["score"] > max_score:
                    max_score = result["score"]
                    best_term = term
                    if "breakdown" in result:
                        best_breakdown = result["breakdown"]
            
            if max_score > 0:
                scored_component = {
                    "component": component,
                    "confidence": max_score,
                    "term": best_term,
                    "match_type": "hybrid_scoring",
                    "props": {"text": best_term.title()},
                    "passed_threshold": max_score >= self.config["scoring"]["threshold"]
                }
                
                if self.debug_mode or self.config["scoring"]["debug"]:
                    scored_component["breakdown"] = best_breakdown
                
                scored_components.append(scored_component)
        
        # Сортируем по убыванию confidence
        scored_components.sort(key=lambda x: x["confidence"], reverse=True)
        
        return scored_components
