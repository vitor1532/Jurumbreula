import json
import os
import re
import uuid

MODULE_ID = "Jurumbreula"
SPELLS_PACK = f"{MODULE_ID}.spells-55e"
SUBCLASSES_PACK = f"{MODULE_ID}.subclasses-55e"
CLASSES_PACK = f"{MODULE_ID}.classes-55e"

def make_id():
    """Gera um ID alfanumérico válido de 16 caracteres para o Foundry VTT."""
    return uuid.uuid4().hex[:16]

def sanitize_id(item_id):
    if not item_id or len(str(item_id)) != 16:
        return make_id()
    return item_id

def process_spells():
    """Lê todas as magias em data/spells/ e gera um mapa de Nome -> UUID."""
    spells_dir = os.path.join("data", "spells")
    spell_map = {}
    
    if not os.path.exists(spells_dir):
        print(f"[AVISO] Pasta {spells_dir} não encontrada.")
        return spell_map

    for file in os.listdir(spells_dir):
        if file.endswith(".json"):
            path = os.path.join(spells_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                spells = json.load(f)
                for spell in spells:
                    item_id = sanitize_id(spell.get("_id"))
                    spell["_id"] = item_id
                    
                    # Nome padronizado sem (2024) para busca
                    clean_name = re.sub(r"\s*\(2024\)", "", spell["name"]).strip().lower()
                    uuid_str = f"Compendium.{SPELLS_PACK}.Item.{item_id}"
                    spell_map[clean_name] = uuid_str

    print(f"[OK] Mapeadas {len(spell_map)} magias para o compêndio.")
    return spell_map

def build_full_module(spell_map):
    """Processa e vincula todas as correlações de Classes e Subclasses."""
    input_file = os.path.join("data", "classes-and-subclasses-2024.json")
    
    if not os.path.exists(input_file):
        print(f"[ERRO] Arquivo {input_file} não encontrado.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    subclasses = [i for i in items if i.get("type") == "subclass"]
    classes = [i for i in items if i.get("type") == "class"]

    # 1. MAPEIA SUBCLASSES POR CLASSE
    subclass_map = {} # classIdentifier -> [subclass_uuids]
    
    for sub in subclasses:
        sub_id = sanitize_id(sub.get("_id"))
        sub["_id"] = sub_id
        sub_uuid = f"Compendium.{SUBCLASSES_PACK}.Item.{sub_id}"
        
        class_target = sub.get("system", {}).get("classIdentifier")
        if class_target:
            if class_target not in subclass_map:
                subclass_map[class_target] = []
            subclass_map[class_target].append(sub_uuid)

        # Trata os Advancements da Subclasse (Magias de Juramento, Features de Subclasse, etc.)
        advancements = sub.get("system", {}).get("advancement", [])
        for adv in advancements:
            adv["_id"] = sanitize_id(adv.get("_id"))
            
            # Se for concessão de itens (Features ou Spells da subclasse)
            if adv.get("type") == "ItemGrant":
                config_items = adv.get("configuration", {}).get("items", [])
                for item_ref in config_items:
                    # Se tiver um nome anotado, resolve para o UUID da magia
                    ref_name = item_ref.get("name", "").strip().lower()
                    if ref_name in spell_map:
                        item_ref["uuid"] = spell_map[ref_name]

    # 2. PROCESSA CLASSES (Features, HitPoints, Traits, Subclasses e Feats)
    for cls in classes:
        cls_id = sanitize_id(cls.get("_id"))
        cls["_id"] = cls_id
        class_identifier = cls.get("system", {}).get("identifier")

        advancements = cls.get("system", {}).get("advancement", [])
        
        # Garante que a escolha de Subclasse no nível 3 receba a pool correta
        has_subclass_choice = False
        for adv in advancements:
            adv["_id"] = sanitize_id(adv.get("_id"))
            
            # Escolha de Subclasse no Nível 3
            if adv.get("type") == "ItemChoice" and adv.get("title", "").lower().startswith("subclass"):
                has_subclass_choice = True
                matching_subs = subclass_map.get(class_identifier, [])
                adv.setdefault("configuration", {})["pool"] = matching_subs

            # Concessão de Feats/Features no nível
            elif adv.get("type") == "ItemGrant":
                config_items = adv.get("configuration", {}).get("items", [])
                for item_ref in config_items:
                    ref_name = item_ref.get("name", "").strip().lower()
                    if ref_name in spell_map:
                        item_ref["uuid"] = spell_map[ref_name]

        # Se não tiver a escolha de subclasse configurada no nível 3, cria uma automaticamente
        if not has_subclass_choice and class_identifier in subclass_map:
            advancements.append({
                "_id": make_id(),
                "type": "ItemChoice",
                "level": 3,
                "title": "Escolha de Subclasse",
                "icon": "icons/skills/social/diplomacy-handshake.webp",
                "configuration": {
                    "pool": subclass_map[class_identifier],
                    "choices": { "3": 1 }
                }
            })

    # Salva o resultado compilado e vinculado de volta no JSON
    output_file = os.path.join("data", "classes-and-subclasses-2024.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(classes + subclasses, f, ensure_ascii=False, indent=2)

    print(f"[SUCESSO] Módulo compilado e totalmente correlacionado!")
    print(f"-> {len(classes)} Classes processadas.")
    print(f"-> {len(subclasses)} Subclasses vinculadas com magias e escolhas de nível.")

if __name__ == "__main__":
    print("--- Executando Compilador de Correlações D&D 2024 (Jurumbleura) ---")
    spells = process_spells()
    build_full_module(spells)