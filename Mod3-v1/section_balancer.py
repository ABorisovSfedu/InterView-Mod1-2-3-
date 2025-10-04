#!/usr/bin/env python3
"""Балансировка секций и ограничение повторов для Mod3-v1"""

import yaml
import os
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter

class SectionBalancer:
    """Движок балансировки секций и ограничения повторов"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Инициализация с загрузкой конфигурации"""
        self.config = self._load_config(config_path)
        
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
            "section_balancing": {
                "max_components_per_section": 12,
                "max_repeats_per_key": 2,
                "min_meaningful_main": 2,
                "meaningful_keys": [
                    "ui.form", "ui.button", "ui.cards", "ui.productGrid", 
                    "ui.text", "ui.heading", "ui.productCard", "ui.cta"
                ],
                "fallback": {
                    "confidence": 0.5,
                    "match_type": "fallback",
                    "safe_text_props": {"value": "Описание раздела"}
                }
            }
        }
    
    def balance_layout_sections(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """
        Балансирует секции layout'а согласно конфигурации
        
        Args:
            layout: Layout с секциями hero, main, footer
            
        Returns:
            Сбалансированный layout с warnings
        """
        balancing_config = self.config.get("section_balancing", {})
        warnings = []
        
        # Копируем layout для модификации
        balanced_layout = {
            "template": layout["template"],
            "sections": {
                "hero": layout["sections"]["hero"].copy(),
                "main": layout["sections"]["main"].copy(),
                "footer": layout["sections"]["footer"].copy()
            },
            "count": layout["count"]
        }
        
        # 1. Ограничиваем размер секций
        balanced_layout, size_warnings = self._limit_section_sizes(balanced_layout, balancing_config)
        warnings.extend(size_warnings)
        
        # 2. Удаляем дубликаты по ключу компонента
        balanced_layout, dedup_warnings = self._deduplicate_components(balanced_layout)
        warnings.extend(dedup_warnings)
        
        # 3. Ограничиваем повторы одного ключа
        balanced_layout, repeat_warnings = self._limit_repeats(balanced_layout, balancing_config)
        warnings.extend(repeat_warnings)
        
        # 4. Проверяем смысловую наполняемость Main
        balanced_layout, meaningful_warnings = self._ensure_meaningful_main(balanced_layout, balancing_config)
        warnings.extend(meaningful_warnings)
        
        # Обновляем общий счетчик компонентов
        balanced_layout["count"] = sum(
            len(components) for components in balanced_layout["sections"].values()
        )
        
        # Добавляем warnings если есть
        if warnings:
            balanced_layout["warnings"] = warnings
        
        return balanced_layout
    
    def _limit_section_sizes(self, layout: Dict[str, Any], config: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Ограничивает размер секций, переполнение складывает в main"""
        max_components = config.get("max_components_per_section", 12)
        warnings = []
        
        for section_name in ["hero", "footer"]:
            section = layout["sections"][section_name]
            if len(section) > max_components:
                # Сортируем по убыванию confidence
                section.sort(key=lambda x: x.get("confidence", 0), reverse=True)
                
                # Перемещаем избыточные компоненты в main
                excess_components = section[max_components:]
                layout["sections"]["main"].extend(excess_components)
                
                # Оставляем только первые max_components
                layout["sections"][section_name] = section[:max_components]
                
                warnings.append(f"size_limit: {section_name} overflow {len(excess_components)} components moved to main")
        
        return layout, warnings
    
    def _deduplicate_components(self, layout: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Удаляет дубликаты по ключу компонента, оставляя с наибольшим confidence"""
        warnings = []
        
        for section_name, section in layout["sections"].items():
            if not section:
                continue
                
            # Группируем по типу компонента
            component_groups = {}
            for component in section:
                comp_type = component["component"]
                if comp_type not in component_groups:
                    component_groups[comp_type] = []
                component_groups[comp_type].append(component)
            
            # Обрабатываем каждую группу
            deduplicated_section = []
            for comp_type, components in component_groups.items():
                if len(components) == 1:
                    deduplicated_section.append(components[0])
                else:
                    # Сортируем по убыванию confidence
                    components.sort(key=lambda x: x.get("confidence", 0), reverse=True)
                    
                    # Пытаемся объединить props
                    merged_component = self._merge_component_props(components)
                    deduplicated_section.append(merged_component)
                    
                    warnings.append(f"dedup: {comp_type} x{len(components)} → x1")
            
            layout["sections"][section_name] = deduplicated_section
        
        return layout, warnings
    
    def _merge_component_props(self, components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Объединяет props компонентов, если они совместимы"""
        if not components:
            return {}
        
        # Берем компонент с наибольшим confidence как основу
        base_component = components[0].copy()
        
        # Пытаемся объединить props
        merged_props = base_component.get("props", {}).copy()
        
        for component in components[1:]:
            component_props = component.get("props", {})
            
            # Простое объединение для совместимых props
            for key, value in component_props.items():
                if key not in merged_props:
                    merged_props[key] = value
                elif isinstance(value, str) and isinstance(merged_props[key], str):
                    # Объединяем строки
                    if value not in merged_props[key]:
                        merged_props[key] = f"{merged_props[key]}, {value}"
        
        base_component["props"] = merged_props
        return base_component
    
    def _limit_repeats(self, layout: Dict[str, Any], config: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Ограничивает повторы одного ключа до max_repeats_per_key"""
        max_repeats = config.get("max_repeats_per_key", 2)
        warnings = []
        
        for section_name, section in layout["sections"].items():
            if not section:
                continue
            
            # Подсчитываем повторы
            component_counts = Counter(comp["component"] for comp in section)
            
            # Фильтруем компоненты
            filtered_section = []
            component_added_counts = Counter()
            
            for component in section:
                comp_type = component["component"]
                if component_added_counts[comp_type] < max_repeats:
                    filtered_section.append(component)
                    component_added_counts[comp_type] += 1
                else:
                    warnings.append(f"repeat_limit: {comp_type} exceeded {max_repeats} in {section_name}")
            
            layout["sections"][section_name] = filtered_section
        
        return layout, warnings
    
    def _ensure_meaningful_main(self, layout: Dict[str, Any], config: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
        """Обеспечивает минимальную смысловую наполняемость main секции"""
        min_meaningful = config.get("min_meaningful_main", 2)
        meaningful_keys = config.get("meaningful_keys", [])
        fallback_config = config.get("fallback", {})
        warnings = []
        
        main_section = layout["sections"]["main"]
        
        # Подсчитываем смысловые компоненты
        meaningful_count = sum(
            1 for comp in main_section 
            if comp["component"] in meaningful_keys
        )
        
        if meaningful_count < min_meaningful:
            # Добавляем заглушку
            fallback_component = self._create_fallback_component(fallback_config)
            main_section.insert(0, fallback_component)  # Добавляем в начало
            
            warnings.append(f"meaningful_main: added fallback (had {meaningful_count}, need {min_meaningful})")
        
        return layout, warnings
    
    def _create_fallback_component(self, fallback_config: Dict[str, Any]) -> Dict[str, Any]:
        """Создает заглушку для main секции"""
        confidence = fallback_config.get("confidence", 0.5)
        match_type = fallback_config.get("match_type", "fallback")
        safe_text_props = fallback_config.get("safe_text_props", {"value": "Описание раздела"})
        
        # Пытаемся создать ui.text заглушку
        try:
            return {
                "component": "ui.text",
                "props": safe_text_props,
                "confidence": confidence,
                "match_type": match_type,
                "term": "fallback-text"
            }
        except:
            # Fallback к ui.container
            return {
                "component": "ui.container",
                "props": {},
                "confidence": confidence,
                "match_type": match_type,
                "term": "fallback-container"
            }
    
    def get_balancing_stats(self, layout: Dict[str, Any]) -> Dict[str, Any]:
        """Возвращает статистику балансировки секций"""
        stats = {}
        
        for section_name, section in layout["sections"].items():
            component_counts = Counter(comp["component"] for comp in section)
            stats[section_name] = {
                "total_components": len(section),
                "unique_components": len(component_counts),
                "component_distribution": dict(component_counts),
                "avg_confidence": sum(comp.get("confidence", 0) for comp in section) / len(section) if section else 0
            }
        
        return stats
