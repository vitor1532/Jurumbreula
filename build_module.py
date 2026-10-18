import json
import os
import re
import uuid

MODULE_ID = "Jurumbreula"
SPELLS_PACK = f"{MODULE_ID}.spells-55e"
SUBCLASSES_PACK = f"{MODULE_ID}.subclasses-55e"
CLASSES_PACK = f"{MODULE_ID}.classes-55e"

# ==============================================================================
# TABELA COMPLETA DE REGRAS D&D 2024 (5.5e): SUBCLASSES -> ITENS/MAGIAS POR NÍVEL
# ==============================================================================
SUBCLASS_GRANTS_2024 = {
    # --------------------------------------------------------------------------
    # BÁRBARO (BARBARIAN)
    # --------------------------------------------------------------------------
    "caminho-do-berserker-2024": {
        3: ["Frenzy", "Mindless Rage"],
        6: ["Retaliation"],
        14: ["Intimidating Presence"]
    },
    "caminho-do-guerreiro-totemico-2024": {
        3: ["Beast Sense", "Speak with Animals", "Totem Spirit"],
        6: ["Aspect of the Beast"],
        14: ["Totemic Attunement"]
    },
    "caminho-da-arvore-do-mundo-2024": {
        3: ["Vitality of the Tree"],
        6: ["Branches of the Tree"],
        10: ["Roots of the Tree"],
        14: ["Travel Along the Tree"]
    },
    "caminho-do-fanatico-2024": {
        3: ["Divine Fury", "Warrior of the Gods"],
        6: ["Fanatical Focus"],
        14: ["Rage Beyond Death"]
    },

    # --------------------------------------------------------------------------
    # GUERREIRO (FIGHTER)
    # --------------------------------------------------------------------------
    "mestre-de-batalha-2024": {
        3: ["Combat Superiority", "Student of War"],
        7: ["Know Your Enemy"],
        15: ["Relentless"]
    },
    "cavaleiro-arcano-2024": {
        3: ["Weapon Bond", "Shield", "Mage Armor"],
        7: ["War Magic"],
        13: ["Arcane Charge"]
    },

    # --------------------------------------------------------------------------
    # LADINO (ROGUE)
    # --------------------------------------------------------------------------
    "assassino-2024": {
        3: ["Assassinate", "Bonus Proficiencies"],
        9: ["Infiltration Expertise"],
        13: ["Impostor"],
        17: ["Death Strike"]
    },
    "ladrão-2024": {
        3: ["Fast Hands", "Second-Story Work"],
        9: ["Supreme Sneak"],
        13: ["Use Magic Device"]
    },

    # --------------------------------------------------------------------------
    # PALADINO (PALADIN)
    # --------------------------------------------------------------------------
    "juramento-da-vinganca-2024": {
        3: ["Bane", "Hunter's Mark", "Vow of Enmity"],
        5: ["Hold Person", "Misty Step"],
        9: ["Haste", "Protection from Energy"],
        13: ["Banishment", "Dimension Door"],
        17: ["Hold Monster", "Scrying"]
    },
    "juramento-de-devoção-2024": {
        3: ["Protection from Evil and Good", "Sanctuary", "Sacred Weapon"],
        5: ["Lesser Restoration", "Zone of Truth"],
        9: ["Beacon of Hope", "Dispel Magic"],
        13: ["Freedom of Movement", "Guardian of Faith"],
        17: ["Commune", "Flame Strike"]
    },
    "juramento-dos-ancioes-2024": {
        3: ["Ensnaring Strike", "Speak with Animals", "Nature's Wrath"],
        5: ["Misty Step", "Moonbeam"],
        9: ["Plant Growth", "Protection from Energy"],
        13: ["Ice Storm", "Stoneskin"],
        17: ["Commune with Nature", "Tree Stride"]
    },

    # --------------------------------------------------------------------------
    # CLÉRIGO (CLERIC)
    # --------------------------------------------------------------------------
    "dominio-da-vida-2024": {
        3: ["Bless", "Cure Wounds", "Lesser Restoration", "Spiritual Weapon", "Disciple of Life"],
        5: ["Beacon of Hope", "Revivify"],
        7: ["Death Ward", "Guardian of Faith"],
        9: ["Mass Cure Wounds", "Raise Dead"]
    },
    "dominio-da-luz-2024": {
        3: ["Burning Hands", "Faerie Fire", "Scorching Ray", "Flaming Sphere", "Warding Flare"],
        5: ["Daylight", "Fireball"],
        7: ["Guardian of Faith", "Wall of Fire"],
        9: ["Flame Strike", "Scrying"]
    },

    # --------------------------------------------------------------------------
    # DRUIDA (DRUID)
    # --------------------------------------------------------------------------
    "circulo-da-terra-2024": {
        3: ["Misty Step", "Entangle", "Natural Recovery"],
        5: ["Lightning Bolt", "Plant Growth"],
        7: ["Control Water", "Freedom of Movement"],
        9: ["Commune with Nature", "Tree Stride"]
    },
    "circulo-da-lua-2024": {
        3: ["Cure Wounds", "Starry Wisp", "Combat Wild Shape"],
        5: ["Dispel Magic", "Revivify"],
        7: ["Fount of Moonlight"],
        9: ["Mass Cure Wounds"]
    },

    # --------------------------------------------------------------------------
    # PATRULHEIRO (RANGER)
    # --------------------------------------------------------------------------
    "mestre-das-feras-2024": {
        3: ["Ranger's Companion", "Hunter's Mark"],
        7: ["Exceptional Training"],
        11: ["Bestial Fury"]
    },
    "caçador-2024": {
        3: ["Hunter's Prey", "Hunter's Mark"],
        7: ["Defensive Tactics"],
        11: ["Multiattack"]
    },

    # --------------------------------------------------------------------------
    # BRUXO (WARLOCK)
    # --------------------------------------------------------------------------
    "pacto-do-corruptor-2024": {
        3: ["Burning Hands", "Command", "Blindness/Deafness", "Scorching Ray", "Dark One's Blessing"],
        5: ["Fireball", "Stinking Cloud"],
        7: ["Fire Shield", "Wall of Fire"],
        9: ["Flame Strike", "Hallow"]
    }
}

def make_id():
    return uuid.uuid4().hex[:16]

def sanitize_id(item_id):
    if not item_id or len(str(item_id)) != 16:
        return make_id()
    return item_id

def normalize_name(name):
    clean = re.sub(r"\s*\(2024\)", "", name, flags=re.IGNORECASE)
    clean = re.sub(r"\s*\([^)]*\)", "", clean)
    return clean.strip().lower()

def process_spells():
    """Mapeia todas as magias existentes em data/spells/."""
    spells_dir = os.path.join("data", "spells")
    spell_map = {}
    
    if not os.path.exists(spells_dir):
        return spell_map

    for file in os.listdir(spells_dir):
        if file.endswith(".json"):
            path = os.path.join(spells_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                spells = json.load(f)
                for spell in spells:
                    item_id = sanitize_id(spell.get("_id"))
                    spell["_id"] = item_id
                    
                    spell.setdefault("system", {})["source"] = {
                        "custom": "PHB 2024",
                        "rules": "2024"
                    }
                    
                    raw_name = spell["name"]
                    uuid_str = f"Compendium.{SPELLS_PACK}.Item.{item_id}"
                    
                    spell_map[raw_name.lower()] = uuid_str
                    spell_map[normalize_name(raw_name)] = uuid_str

    print(f"[OK] Mapeadas {len(spell_map)} magias.")
    return spell_map

def build_full_module(spell_map):
    input_file = os.path.join("data", "classes-and-subclasses-2024.json")
    
    if not os.path.exists(input_file):
        print(f"[ERRO] Arquivo {input_file} não encontrado.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    subclasses = [i for i in items if i.get("type") == "subclass"]
    classes = [i for i in items if i.get("type") == "class"]

    subclass_map = {}

    for sub in subclasses:
        sub_id = sanitize_id(sub.get("_id"))
        sub["_id"] = sub_id
        
        sub.setdefault("system", {})["source"] = {
            "custom": "PHB 2024",
            "rules": "2024"
        }
        
        sub_uuid = f"Compendium.{SUBCLASSES_PACK}.Item.{sub_id}"
        class_target = sub.get("system", {}).get("classIdentifier")
        
        if class_target:
            if class_target not in subclass_map:
                subclass_map[class_target] = []
            subclass_map[class_target].append(sub_uuid)

        sub_identifier = sub.get("system", {}).get("identifier")
        advancements = sub.get("system", {}).setdefault("advancement", [])

        # Processa concessões automáticas (Magias e Recursos do Bárbaro, Guerreiro, etc.)
        if sub_identifier in SUBCLASS_GRANTS_2024:
            grant_rules = SUBCLASS_GRANTS_2024[sub_identifier]
            
            for lvl, item_names in grant_rules.items():
                items_to_grant = []
                for item_name in item_names:
                    clean = normalize_name(item_name)
                    
                    # 1. Tenta vincular como Magia se existir no banco de magias
                    found_uuid = spell_map.get(item_name.lower()) or spell_map.get(clean)
                    
                    if found_uuid:
                        items_to_grant.append({"uuid": found_uuid})
                    else:
                        # 2. Se for uma Feature / Habilidade (Ex: Frenzy do Bárbaro), guarda o nome para concessão direta
                        items_to_grant.append({"name": item_name})

                if items_to_grant:
                    advancements.append({
                        "_id": make_id(),
                        "type": "ItemGrant",
                        "level": lvl,
                        "title": f"Recursos e Magias da Subclasse (Nível {lvl})",
                        "icon": "icons/skills/melee/weapons-crossed-swords-yellow.webp",
                        "configuration": {
                            "items": items_to_grant
                        }
                    })

    # Vínculo das Subclasses às Classes no nível 3
    for cls in classes:
        cls_id = sanitize_id(cls.get("_id"))
        cls["_id"] = cls_id
        
        cls.setdefault("system", {})["source"] = {
            "custom": "PHB 2024",
            "rules": "2024"
        }
        
        class_identifier = cls.get("system", {}).get("identifier")
        advancements = cls.get("system", {}).setdefault("advancement", [])
        
        has_subclass_choice = False
        for adv in advancements:
            adv["_id"] = sanitize_id(adv.get("_id"))
            if adv.get("type") == "ItemChoice" and "subclass" in adv.get("title", "").lower():
                has_subclass_choice = True
                adv.setdefault("configuration", {})["pool"] = subclass_map.get(class_identifier, [])

        if not has_subclass_choice and class_identifier in subclass_map:
            advancements.append({
                "_id": make_id(),
                "type": "ItemChoice",
                "level": 3,
                "title": "Subclass",
                "icon": "icons/skills/social/diplomacy-handshake.webp",
                "configuration": {
                    "pool": subclass_map[class_identifier],
                    "choices": { "3": 1 }
                }
            })

    output_file = os.path.join("data", "classes-and-subclasses-2024.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(classes + subclasses, f, ensure_ascii=False, indent=2)

    print("[SUCESSO] Build completo! Magias e Habilidades (Bárbaro, Guerreiro, etc.) vinculadas com sucesso.")

if __name__ == "__main__":
    spells = process_spells()
    build_full_module(spells)