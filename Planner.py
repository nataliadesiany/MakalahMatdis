import itertools
import random
from datetime import datetime, timedelta
from collections import defaultdict
import re
import time

class ClothingItem:
    def __init__(self, item_id, name, category, color, style, formality_level, weather_suitability, available=True):
        self.id = item_id
        self.name = name
        self.category = category
        self.color = color
        self.style = style
        self.formality_level = formality_level
        self.weather_suitability = weather_suitability
        self.available = available
        self.usage_count = 0
        self.last_used = None
        
    def __str__(self):
        status = "✓" if self.available else "✗"
        return f"{status} {self.color} {self.name} ({self.category})"
    
    def __repr__(self):
        return f"ClothingItem(id={self.id}, name='{self.name}', available={self.available})"

class Wardrobe:
    def __init__(self):
        self.items = {}
        self.categories = {
            'tops': [],
            'bottoms': [], 
            'outerwear': [],
            'shoes': [],
            'accessories': []
        }
    
    def add_item(self, item):
        if not isinstance(item, ClothingItem):
            raise ValueError("Item must be an instance of ClothingItem")
        
        self.items[item.id] = item
        self.categories[item.category].append(item)
        print(f"Added: {item}")
    
    def get_items_by_category(self, category):
        return self.categories.get(category, [])
    
    def get_available_items_by_category(self, category):
        return [item for item in self.categories.get(category, []) if item.available]
    
    def mark_item_unavailable(self, item_id, reason="in laundry"):
        if item_id in self.items:
            self.items[item_id].available = False
            print(f"Item {self.items[item_id].name} marked as unavailable ({reason})")
        else:
            print(f"Item with ID {item_id} not found in wardrobe")
    
    def mark_item_available(self, item_id):
        if item_id in self.items:
            self.items[item_id].available = True
            print(f"Item {self.items[item_id].name} marked as available")
        else:
            print(f"Item with ID {item_id} not found in wardrobe")
    
    def get_statistics(self):
        available_items = [item for item in self.items.values() if item.available]
        unavailable_items = [item for item in self.items.values() if not item.available]
        
        stats = {
            'total_items': len(self.items),
            'available_items': len(available_items),
            'unavailable_items': len(unavailable_items),
            'by_category': {cat: len([item for item in items if item.available]) 
                          for cat, items in self.categories.items()},
            'by_color': defaultdict(int),
            'by_style': defaultdict(int),
            'unavailable_breakdown': defaultdict(int)
        }
        
        for item in available_items:
            stats['by_color'][item.color] += 1
            stats['by_style'][item.style] += 1
            
        return stats

class ConstraintEngine:
    def __init__(self):
        self.weather_rules = self._initialize_weather_rules()
        self.occasion_rules = self._initialize_occasion_rules()
        self.color_compatibility = self._initialize_color_rules()
        
    def _initialize_weather_rules(self):
        return {
            'hot': {
                'suitable_items': ['t-shirt', 'tank top', 'shorts', 'sandals', 'dress', 'skirt', 'flip flops'],
                'unsuitable_items': ['coat', 'boots', 'sweater', 'jacket', 'long pants', 'heavy'],
                'max_layers': 2,
                'preferred_materials': ['cotton', 'linen', 'light']
            },
            'warm': {
                'suitable_items': ['shirt', 'blouse', 'jeans', 'chinos', 'sneakers', 'light jacket', 'cardigan'],
                'unsuitable_items': ['heavy coat', 'winter boots', 'thick sweater', 'puffer'],
                'max_layers': 3,
                'preferred_materials': ['cotton', 'denim', 'light wool']
            },
            'cool': {
                'suitable_items': ['sweater', 'cardigan', 'jeans', 'jacket', 'closed shoes', 'boots', 'long pants'],
                'unsuitable_items': ['sandals', 'shorts', 'tank top', 'flip flops'],
                'min_layers': 2,
                'preferred_materials': ['wool', 'denim', 'leather']
            },
            'cold': {
                'suitable_items': ['coat', 'heavy sweater', 'boots', 'long pants', 'scarf', 'gloves', 'jacket'],
                'unsuitable_items': ['sandals', 'shorts', 't-shirt', 'tank top', 'flip flops'],
                'min_layers': 3,
                'preferred_materials': ['wool', 'fleece', 'down', 'leather', 'heavy']
            }
        }
    
    def _initialize_occasion_rules(self):
        return {
            'formal': {
                'min_formality': 7, 
                'required_categories': ['tops', 'bottoms', 'shoes'],
                'preferred_items': ['dress shirt', 'suit', 'dress shoes', 'tie', 'blazer'],
                'description': 'Business meetings, formal events, important presentations'
            },
            'business': {
                'min_formality': 5, 
                'max_formality': 8,
                'preferred_items': ['blazer', 'dress shirt', 'chinos', 'dress shoes', 'button down'],
                'description': 'Business casual, office environment, client meetings'
            },
            'casual': {
                'max_formality': 6,
                'preferred_items': ['t-shirt', 'jeans', 'sneakers', 'sweater', 'casual shirt'],
                'description': 'Weekend activities, casual social events, relaxed environments'
            },
            'sporty': {
                'max_formality': 4, 
                'required_items': ['sneakers'],
                'preferred_items': ['athletic wear', 'joggers', 'hoodie', 'running shoes'],
                'description': 'Exercise, sports activities, athletic events'
            },
            'party': {
                'min_formality': 6,
                'preferred_items': ['dress', 'heels', 'jewelry', 'blazer', 'stylish top'],
                'description': 'Social parties, evening events, celebrations'
            }
        }
    
    def _initialize_color_rules(self):
        return {
            'black': ['white', 'gray', 'navy', 'red', 'blue', 'silver', 'gold', 'beige', 'cream'],
            'white': ['black', 'navy', 'blue', 'gray', 'brown', 'red', 'green', 'pink', 'purple', 'any'],
            'navy': ['white', 'gray', 'beige', 'light blue', 'cream', 'silver', 'brown'],
            'gray': ['white', 'black', 'navy', 'pink', 'yellow', 'blue', 'purple', 'silver'],
            'brown': ['white', 'beige', 'cream', 'navy', 'tan', 'orange', 'gold', 'green'],
            'beige': ['brown', 'white', 'navy', 'black', 'cream', 'tan', 'gold'],
            'red': ['black', 'white', 'navy', 'gray', 'beige', 'cream'],
            'blue': ['white', 'black', 'gray', 'beige', 'brown', 'navy', 'silver'],
            'green': ['white', 'beige', 'brown', 'navy', 'cream', 'gold'],
            'pink': ['white', 'gray', 'navy', 'black', 'silver'],
            'yellow': ['white', 'gray', 'navy', 'black', 'brown'],
            'purple': ['white', 'gray', 'black', 'silver'],
            'orange': ['brown', 'beige', 'white', 'navy', 'cream'],
            'cream': ['brown', 'beige', 'navy', 'white', 'gold'],
            'tan': ['brown', 'beige', 'white', 'navy', 'cream'],
            'silver': ['black', 'white', 'gray', 'navy', 'blue'],
            'gold': ['black', 'brown', 'beige', 'white', 'cream']
        }
    
    def validate_hard_constraints(self, outfit, weather, occasion):
        if not self._check_availability(outfit):
            return False, "Some items are not available"
            
        if not self._check_weather_compatibility(outfit, weather):
            return False, "Weather compatibility failed"
            
        if not self._check_occasion_compatibility(outfit, occasion):
            return False, "Occasion compatibility failed"
            
        if not self._check_basic_color_compatibility(outfit):
            return False, "Color compatibility failed"
            
        return True, "All hard constraints satisfied"
    
    def _check_availability(self, outfit):
        return all(item.available for item in outfit)
    
    def _check_weather_compatibility(self, outfit, weather):
        if weather not in self.weather_rules:
            return True
            
        rules = self.weather_rules[weather]
        
        for item in outfit:
            item_name_lower = item.name.lower()
            for unsuitable in rules.get('unsuitable_items', []):
                if unsuitable in item_name_lower:
                    return False
        
        layer_count = sum(1 for item in outfit if item.category in ['tops', 'outerwear'])
        
        if 'max_layers' in rules and layer_count > rules['max_layers']:
            return False
        if 'min_layers' in rules and layer_count < rules['min_layers']:
            return False
            
        return True
    
    def _check_occasion_compatibility(self, outfit, occasion):
        if occasion not in self.occasion_rules:
            return True
            
        rules = self.occasion_rules[occasion]
        
        avg_formality = sum(item.formality_level for item in outfit) / len(outfit)
        
        if 'min_formality' in rules and avg_formality < rules['min_formality']:
            return False
        if 'max_formality' in rules and avg_formality > rules['max_formality']:
            return False
            
        return True
    
    def _check_basic_color_compatibility(self, outfit):
        colors = [item.color for item in outfit]
        
        if len(set(colors)) <= 1:
            return True
            
        for i, color1 in enumerate(colors):
            for color2 in colors[i+1:]:
                if color1 != color2:
                    compatible_colors = self.color_compatibility.get(color1, [])
                    if color2 not in compatible_colors and 'any' not in compatible_colors:
                        return False
        
        return True
    
    def calculate_soft_constraint_score(self, outfit, weather, occasion, preferences=None):
        total_score = 0
        
        color_score = self._calculate_color_harmony_score(outfit)
        total_score += color_score * 0.70
        
        preference_score = self._calculate_preference_score(outfit, preferences)
        total_score += preference_score * 0.30
        
        return total_score
    
    def _calculate_color_harmony_score(self, outfit):
        colors = [item.color for item in outfit]
        unique_colors = list(set(colors))
        
        if len(unique_colors) > 4:
            return 0.2
        elif len(unique_colors) > 3:
            return 0.5
        
        harmonic_combinations = [
            ['black', 'white'], ['navy', 'white'], ['brown', 'beige'],
            ['gray', 'white'], ['black', 'gray'], ['navy', 'beige'],
            ['brown', 'cream'], ['black', 'red'], ['navy', 'gray'],
            ['white', 'blue'], ['beige', 'brown'], ['gray', 'black'],
            ['navy', 'cream'], ['white', 'navy'], ['black', 'beige']
        ]
        
        for combo in harmonic_combinations:
            if all(color in unique_colors for color in combo):
                return 1.0
        
        compatibility_score = 0
        total_pairs = 0
        
        for i, color1 in enumerate(unique_colors):
            for color2 in unique_colors[i+1:]:
                total_pairs += 1
                compatible_colors = self.color_compatibility.get(color1, [])
                if color2 in compatible_colors or 'any' in compatible_colors:
                    compatibility_score += 1
        
        if total_pairs == 0:
            return 1.0
        
        return compatibility_score / total_pairs
    
    def _calculate_preference_score(self, outfit, preferences):
        if not preferences:
            return 0.5
        
        score = 0.5
        
        if 'preferred_colors' in preferences and preferences['preferred_colors']:
            outfit_colors = [item.color for item in outfit]
            matching_colors = sum(1 for color in outfit_colors 
                                if color in preferences['preferred_colors'])
            color_match_rate = matching_colors / len(outfit_colors)
            score += color_match_rate * 0.3
        
        if 'preferred_styles' in preferences and preferences['preferred_styles']:
            outfit_styles = [item.style for item in outfit]
            matching_styles = sum(1 for style in outfit_styles 
                                if style in preferences['preferred_styles'])
            style_match_rate = matching_styles / len(outfit_styles)
            score += style_match_rate * 0.2
        
        return min(1.0, score)

class CombinorialGenerator:
    def __init__(self, wardrobe, constraint_engine):
        self.wardrobe = wardrobe
        self.constraint_engine = constraint_engine
    
    def generate_all_combinations(self, weather, occasion, preferences=None, max_results=15):
        print(f"🔄 Generating combinations for {weather} weather, {occasion} occasion...")
        
        tops = self.wardrobe.get_available_items_by_category('tops')
        bottoms = self.wardrobe.get_available_items_by_category('bottoms')
        outerwear = self.wardrobe.get_available_items_by_category('outerwear')
        shoes = self.wardrobe.get_available_items_by_category('shoes')
        accessories = self.wardrobe.get_available_items_by_category('accessories')
        
        print(f"📦 Available items: {len(tops)} tops, {len(bottoms)} bottoms, "
              f"{len(outerwear)} outerwear, {len(shoes)} shoes, {len(accessories)} accessories")
        
        if not tops or not bottoms or not shoes:
            print("❌ Insufficient items for basic outfit generation")
            return []
        
        valid_combinations = []
        total_checked = 0
        
        print("🔄 Generating basic combinations (top + bottom + shoes)...")
        for top, bottom, shoe in itertools.product(tops, bottoms, shoes):
            basic_outfit = [top, bottom, shoe]
            total_checked += 1
            
            is_valid, reason = self.constraint_engine.validate_hard_constraints(
                basic_outfit, weather, occasion
            )
            
            if is_valid:
                score = self.constraint_engine.calculate_soft_constraint_score(
                    basic_outfit, weather, occasion, preferences
                )
                
                valid_combinations.append({
                    'outfit': basic_outfit,
                    'score': score,
                    'description': self._generate_description(basic_outfit),
                    'type': 'basic'
                })
        
        if outerwear:
            print("🔄 Generating combinations with outerwear...")
            for top, bottom, outer, shoe in itertools.product(tops, bottoms, outerwear, shoes):
                outfit_with_outer = [top, bottom, outer, shoe]
                total_checked += 1
                
                is_valid, reason = self.constraint_engine.validate_hard_constraints(
                    outfit_with_outer, weather, occasion
                )
                
                if is_valid:
                    score = self.constraint_engine.calculate_soft_constraint_score(
                        outfit_with_outer, weather, occasion, preferences
                    )
                    
                    valid_combinations.append({
                        'outfit': outfit_with_outer,
                        'score': score,
                        'description': self._generate_description(outfit_with_outer),
                        'type': 'with_outerwear'
                    })
        
        if accessories and valid_combinations:
            print("🔄 Adding single accessories to top combinations...")
            top_basic = sorted([c for c in valid_combinations if c['type'] == 'basic'], 
                             key=lambda x: x['score'], reverse=True)[:10]
            
            for combo in top_basic:
                for accessory in accessories:
                    outfit_with_acc = combo['outfit'] + [accessory]
                    total_checked += 1
                    
                    is_valid, reason = self.constraint_engine.validate_hard_constraints(
                        outfit_with_acc, weather, occasion
                    )
                    
                    if is_valid:
                        score = self.constraint_engine.calculate_soft_constraint_score(
                            outfit_with_acc, weather, occasion, preferences
                        )
                        
                        valid_combinations.append({
                            'outfit': outfit_with_acc,
                            'score': score,
                            'description': self._generate_description(outfit_with_acc),
                            'type': 'with_accessory'
                        })
        
        if len(accessories) >= 2 and valid_combinations:
            print("🔄 Adding multiple accessories to select combinations...")
            top_basic = sorted([c for c in valid_combinations if c['type'] == 'basic'], 
                             key=lambda x: x['score'], reverse=True)[:5]
            
            for combo in top_basic:
                for acc1, acc2 in itertools.combinations(accessories, 2):
                    outfit_with_accs = combo['outfit'] + [acc1, acc2]
                    total_checked += 1
                    
                    is_valid, reason = self.constraint_engine.validate_hard_constraints(
                        outfit_with_accs, weather, occasion
                    )
                    
                    if is_valid:
                        score = self.constraint_engine.calculate_soft_constraint_score(
                            outfit_with_accs, weather, occasion, preferences
                        )
                        
                        valid_combinations.append({
                            'outfit': outfit_with_accs,
                            'score': score,
                            'description': self._generate_description(outfit_with_accs),
                            'type': 'with_multiple_accessories'
                        })
        
        print(f"Checked {total_checked} combinations, found {len(valid_combinations)} valid ones")
        
        valid_combinations.sort(key=lambda x: x['score'], reverse=True)
        return valid_combinations[:max_results]
    
    def _generate_description(self, outfit):
        categories = {}
        for item in outfit:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(f"{item.color} {item.name}")
        
        description_parts = []
        category_order = ['tops', 'bottoms', 'outerwear', 'shoes', 'accessories']
        
        for category in category_order:
            if category in categories:
                description_parts.append(f"{category.title()}: {', '.join(categories[category])}")
        
        return " | ".join(description_parts)

class SmartOutfitPlanner:
    def __init__(self):
        self.wardrobe = Wardrobe()
        self.constraint_engine = ConstraintEngine()
        self.generator = CombinorialGenerator(self.wardrobe, self.constraint_engine)
        self.setup_extensive_wardrobe()
        self.simulate_laundry_status()
    
    def setup_extensive_wardrobe(self):
        print("Setting up extensive wardrobe...")
        
        tops_data = [
            (1, "Cotton T-Shirt", "white", "casual", 4, "warm"),
            (2, "Dress Shirt", "blue", "formal", 8, "cool"),
            (3, "Polo Shirt", "navy", "casual", 5, "warm"),
            (4, "Sweater", "gray", "casual", 6, "cold"),
            (5, "Blouse", "pink", "formal", 7, "cool"),
            (6, "Tank Top", "black", "casual", 3, "hot"),
            (7, "Hoodie", "red", "sporty", 4, "cool"),
            (8, "Cardigan", "beige", "casual", 6, "cool"),
            (9, "Blazer", "black", "formal", 9, "cool"),
            (10, "Flannel Shirt", "green", "casual", 5, "cool"),
            (11, "Crop Top", "yellow", "casual", 3, "hot"),
            (12, "Turtle Neck", "brown", "casual", 6, "cold"),
            (13, "V-Neck Sweater", "purple", "casual", 5, "cool"),
            (14, "Button Down Shirt", "white", "formal", 7, "cool"),
            (15, "Long Sleeve Tee", "orange", "casual", 4, "cool"),
            (16, "Halter Top", "cream", "casual", 4, "hot"),
            (17, "Knit Top", "silver", "casual", 5, "cool"),
            (18, "Formal Shirt", "navy", "formal", 8, "cool"),
            (19, "Athletic Tank", "blue", "sporty", 3, "hot"),
            (20, "Peasant Blouse", "tan", "casual", 5, "warm")
        ]
        
        for item_id, name, color, style, formality, weather in tops_data:
            self.wardrobe.add_item(ClothingItem(item_id, name, "tops", color, style, formality, weather))
        
        bottoms_data = [
            (101, "Jeans", "blue", "casual", 4, "cool"),
            (102, "Dress Pants", "black", "formal", 8, "cool"),
            (103, "Chinos", "beige", "casual", 6, "warm"),
            (104, "Shorts", "navy", "casual", 3, "hot"),
            (105, "Skirt", "gray", "formal", 7, "warm"),
            (106, "Leggings", "black", "sporty", 3, "cool"),
            (107, "Cargo Pants", "green", "casual", 4, "cool"),
            (108, "Joggers", "red", "sporty", 2, "cool"),
            (109, "Mini Skirt", "pink", "casual", 5, "warm"),
            (110, "Palazzo Pants", "white", "casual", 6, "hot"),
            (111, "Formal Trousers", "navy", "formal", 8, "cool"),
            (112, "Denim Skirt", "blue", "casual", 5, "warm"),
            (113, "Sweatpants", "gray", "sporty", 2, "cool"),
            (114, "Capri Pants", "brown", "casual", 4, "warm"),
            (115, "Pencil Skirt", "black", "formal", 8, "cool")
        ]
        
        for item_id, name, color, style, formality, weather in bottoms_data:
            self.wardrobe.add_item(ClothingItem(item_id, name, "bottoms", color, style, formality, weather))
        
        outerwear_data = [
            (201, "Blazer", "navy", "formal", 8, "cool"),
            (202, "Leather Jacket", "black", "casual", 6, "cool"),
            (203, "Wool Coat", "brown", "formal", 7, "cold"),
            (204, "Denim Jacket", "blue", "casual", 5, "cool"),
            (205, "Cardigan", "gray", "casual", 5, "cool"),
            (206, "Bomber Jacket", "green", "casual", 5, "cool"),
            (207, "Peacoat", "black", "formal", 8, "cold"),
            (208, "Windbreaker", "red", "sporty", 4, "cool"),
            (209, "Trench Coat", "beige", "formal", 8, "cool"),
            (210, "Puffer Jacket", "navy", "casual", 4, "cold"),
            (211, "Kimono", "pink", "casual", 6, "warm"),
            (212, "Track Jacket", "white", "sporty", 3, "cool")
        ]
        
        for item_id, name, color, style, formality, weather in outerwear_data:
            self.wardrobe.add_item(ClothingItem(item_id, name, "outerwear", color, style, formality, weather))
        
        shoes_data = [
            (301, "Sneakers", "white", "casual", 3, "warm"),
            (302, "Dress Shoes", "black", "formal", 9, "cool"),
            (303, "Boots", "brown", "casual", 5, "cold"),
            (304, "Sandals", "beige", "casual", 2, "hot"),
            (305, "High Heels", "red", "formal", 8, "cool"),
            (306, "Loafers", "navy", "formal", 7, "cool"),
            (307, "Flip Flops", "blue", "casual", 1, "hot"),
            (308, "Athletic Shoes", "gray", "sporty", 3, "cool"),
            (309, "Ankle Boots", "black", "casual", 6, "cool"),
            (310, "Ballet Flats", "pink", "casual", 4, "warm"),
            (311, "Oxford Shoes", "brown", "formal", 8, "cool"),
            (312, "Wedges", "tan", "casual", 5, "warm"),
            (313, "Combat Boots", "black", "casual", 5, "cold"),
            (314, "Espadrilles", "cream", "casual", 4, "hot"),
            (315, "Running Shoes", "green", "sporty", 2, "cool")
        ]
        
        for item_id, name, color, style, formality, weather in shoes_data:
            self.wardrobe.add_item(ClothingItem(item_id, name, "shoes", color, style, formality, weather))
        
        accessories_data = [
            (401, "Watch", "silver", "formal", 7, "any"),
            (402, "Belt", "black", "formal", 6, "any"),
            (403, "Necklace", "gold", "formal", 6, "any"),
            (404, "Scarf", "red", "casual", 5, "cold"),
            (405, "Hat", "navy", "casual", 4, "any"),
            (406, "Sunglasses", "black", "casual", 5, "hot"),
            (407, "Bracelet", "silver", "casual", 4, "any"),
            (408, "Earrings", "gold", "formal", 6, "any"),
            (409, "Tie", "blue", "formal", 8, "any"),
            (410, "Handbag", "brown", "formal", 7, "any"),
            (411, "Backpack", "gray", "sporty", 3, "any"),
            (412, "Gloves", "black", "formal", 6, "cold"),
            (413, "Hair Band", "pink", "casual", 3, "any"),
            (414, "Bow Tie", "white", "formal", 9, "any"),
            (415, "Wallet Chain", "silver", "casual", 4, "any"),
            (416, "Brooch", "gold", "formal", 8, "any"),
            (417, "Ring", "silver", "formal", 5, "any"),
            (418, "Anklet", "gold", "casual", 3, "hot")
        ]
        
        for item_id, name, color, style, formality, weather in accessories_data:
            self.wardrobe.add_item(ClothingItem(item_id, name, "accessories", color, style, formality, weather))
        
        print(f"✅ Wardrobe setup complete! Total items: {len(self.wardrobe.items)}")
    
    def simulate_laundry_status(self):
        print("\n🧺 Simulating laundry status...")
        
        unavailable_items = [
            (2, "in laundry"),
            (104, "in laundry"),
            (203, "at dry cleaner"),
            (305, "broken heel"),
            (410, "left at office"),
            (8, "stained"),
            (108, "in laundry"),
            (302, "being repaired")
        ]
        
        for item_id, reason in unavailable_items:
            self.wardrobe.mark_item_unavailable(item_id, reason)
        
        print(f"❌ {len(unavailable_items)} items marked as unavailable")
    
    def get_recommendations(self, weather, occasion, preferences=None, max_results=10):
        print(f"\n🌟 === SMART OUTFIT RECOMMENDATIONS ===")
        print(f"🌤️  Weather: {weather}")
        print(f"🎯 Occasion: {occasion}")
        if preferences:
            print(f"💭 Preferences: {preferences}")
        print("=" * 50)
        
        start_time = time.time()
        recommendations = self.generator.generate_all_combinations(
            weather, occasion, preferences, max_results
        )
        processing_time = time.time() - start_time
        
        print(f"⏱️  Processing time: {processing_time:.3f} seconds")
        
        return recommendations
    
    def display_recommendations(self, recommendations):
        if not recommendations:
            print("❌ No suitable outfit combinations found!")
            print("💡 Try relaxing your preferences or check item availability")
            return
        
        print(f"\n🎉 Found {len(recommendations)} outfit recommendations:\n")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"🏆 RECOMMENDATION #{i}")
            print(f"⭐ Score: {rec['score']:.3f}/1.000")
            print(f"🏷️  Type: {rec['type'].replace('_', ' ').title()}")
            print(f"📝 Description: {rec['description']}")
            
            print("👔 Items:")
            for item in rec['outfit']:
                status_icon = "✅" if item.available else "❌"
                print(f"   {status_icon} {item.color} {item.name} ({item.category}) - "
                      f"Formality: {item.formality_level}, Style: {item.style}")
            
            colors = list(set([item.color for item in rec['outfit']]))
            styles = list(set([item.style for item in rec['outfit']]))
            print(f"🎨 Colors: {', '.join(colors)} ({len(colors)} unique)")
            print(f"🎭 Styles: {', '.join(styles)} ({len(styles)} unique)")
            
            print("-" * 60)
    
    def display_wardrobe_status(self):
        stats = self.wardrobe.get_statistics()
        
        print("\n📊 === WARDROBE STATUS ===")
        print(f"📦 Total items: {stats['total_items']}")
        print(f"✅ Available items: {stats['available_items']}")
        print(f"❌ Unavailable items: {stats['unavailable_items']}")
        
        print("\n📂 Available items by category:")
        for category, count in stats['by_category'].items():
            total_in_category = len(self.wardrobe.get_items_by_category(category))
            print(f"   {category.title()}: {count}/{total_in_category} available")
        
        print("\n🎨 Available items by color:")
        sorted_colors = sorted(stats['by_color'].items(), key=lambda x: x[1], reverse=True)
        for color, count in sorted_colors[:10]:
            print(f"   {color.title()}: {count} items")
        
        print("\n👔 Available items by style:")
        sorted_styles = sorted(stats['by_style'].items(), key=lambda x: x[1], reverse=True)
        for style, count in sorted_styles:
            print(f"   {style.title()}: {count} items")
    
    def show_unavailable_items(self):
        unavailable = [item for item in self.wardrobe.items.values() if not item.available]
        
        if not unavailable:
            print("\n✅ All items are currently available!")
            return
        
        print(f"\n🧺 === UNAVAILABLE ITEMS ({len(unavailable)}) ===")
        by_category = defaultdict(list)
        
        for item in unavailable:
            by_category[item.category].append(item)
        
        for category, items in by_category.items():
            print(f"\n{category.title()}:")
            for item in items:
                print(f"   ❌ {item.color} {item.name}")
    
    def interactive_mode(self):
        print("\n🎮 === INTERACTIVE MODE ===")
        print("Available weather options: hot, warm, cool, cold")
        print("Available occasion options: formal, business, casual, sporty, party")
        print("Type 'quit' to exit, 'status' to see wardrobe status")
        print("Type 'help' for detailed usage instructions\n")
        
        while True:
            try:
                command = input("🎯 Enter command (recommend/status/help/quit): ").strip().lower()
                
                if command == 'quit':
                    print("👋 Thank you for using Smart Outfit Planner!")
                    break
                
                elif command == 'status':
                    self.display_wardrobe_status()
                    self.show_unavailable_items()
                    continue
                
                elif command == 'help':
                    self._show_help()
                    continue
                
                elif command == 'recommend':
                    weather = input("🌤️  Enter weather (hot/warm/cool/cold): ").strip().lower()
                    if weather == 'quit':
                        break
                    
                    if weather not in ['hot', 'warm', 'cool', 'cold']:
                        print("❌ Invalid weather. Please choose: hot, warm, cool, cold")
                        continue
                    
                    occasion = input("🎯 Enter occasion (formal/business/casual/sporty/party): ").strip().lower()
                    if occasion == 'quit':
                        break
                    
                    if occasion not in ['formal', 'business', 'casual', 'sporty', 'party']:
                        print("❌ Invalid occasion. Please choose: formal, business, casual, sporty, party")
                        continue
                    
                    pref_input = input("💭 Enter preferred colors (comma-separated, or press Enter to skip): ").strip()
                    preferences = None
                    if pref_input:
                        preferred_colors = [color.strip() for color in pref_input.split(',')]
                        preferences = {'preferred_colors': preferred_colors}
                    
                    try:
                        max_results = int(input("📊 Number of recommendations (1-20, default 5): ") or "5")
                        max_results = min(max(max_results, 1), 20)
                    except ValueError:
                        max_results = 5
                    
                    recommendations = self.get_recommendations(weather, occasion, preferences, max_results)
                    self.display_recommendations(recommendations)
                    
                    print("\n" + "-"*50)
                
                else:
                    print("❌ Unknown command. Type 'help' for usage instructions.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try again or type 'help' for assistance.")
    
    def _show_help(self):
        print("\n📚 === SMART OUTFIT PLANNER HELP ===")
        print("\n🎯 COMMANDS:")
        print("  recommend  - Generate outfit recommendations")
        print("  status     - Show wardrobe status and statistics")
        print("  help       - Show this help message")
        print("  quit       - Exit the application")
        
        print("\n🌤️  WEATHER OPTIONS:")
        print("  hot   - Tank tops, shorts, sandals (minimal layers)")
        print("  warm  - T-shirts, light pants, sneakers (2-3 layers)")
        print("  cool  - Sweaters, jeans, boots (2+ layers)")
        print("  cold  - Coats, heavy items, boots (3+ layers)")
        
        print("\n🎯 OCCASION OPTIONS:")
        print("  formal   - Business meetings, formal events (formality 7+)")
        print("  business - Office, business casual (formality 5-8)")
        print("  casual   - Weekend, relaxed settings (formality ≤6)")
        print("  sporty   - Exercise, athletics (formality ≤4)")
        print("  party    - Social events, celebrations (formality 6+)")
        
        print("\n💭 PREFERENCES:")
        print("  Colors: Enter preferred colors separated by commas")
        print("  Example: 'navy, white, black'")
        print("  Leave empty for no color preferences")
        
        print("\n📊 SCORING SYSTEM:")
        print("  • Color Harmony: 70% weight (color theory based)")
        print("  • Personal Preferences: 30% weight (user customization)")
        print("  • Hard Constraints: Must be satisfied (availability, weather, occasion)")
        print("  • Soft Constraints: Influence ranking but don't eliminate options")

def main():
    print("🚀 Initializing Smart Outfit Planner...")
    print("🔬 Constraint-Based Combinatorial Optimization System")
    print("📚 Mathematical Foundation: Combinatorics + Constraint Satisfaction Problems")
    print("🎯 Application: Automated Fashion & Personal Styling")
    
    try:
        planner = SmartOutfitPlanner()
        
        print("\n✅ System initialization complete!")
        print(f"📦 Wardrobe loaded with {len(planner.wardrobe.items)} items")
        print("🧺 Dynamic availability simulation active")
        print("🔧 Constraint engine configured")
        print("🧮 Combinatorial generator ready")
        
        planner.interactive_mode()
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()