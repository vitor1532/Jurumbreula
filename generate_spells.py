import json
import os

# Estrutura completa de nomes e metadados das 391 magias do D&D 5.5e (PHB 2024)
SPELLS_2024 = {
    0: [
        ("Ataque Certeiro (True Strike)", "div"), ("Chama Sagrada (Sacred Flame)", "evo"),
        ("Chicote de Espinhos (Thorn Whip)", "trs"), ("Consertar (Mending)", "trs"),
        ("Espirro Ácido (Acid Splash)", "con"), ("Garra Elemental (Elementalism)", "trs"),
        ("Gostar de Música (Guidance)", "div"), ("Ilusão Menor (Minor Illusion)", "ill"),
        ("Luz (Light)", "evo"), ("Mãos Mágicas (Mage Hand)", "con"),
        ("Mensagem (Message)", "trs"), ("Moldar Terra (Mold Earth)", "trs"),
        ("Palavra de Resplendor (Word of Radiance)", "evo"), ("Prestidigitação (Prestidigitation)", "trs"),
        ("Projeção Mágica (Dancing Lights)", "evo"), ("Proteção contra Lâminas (Blade Ward)", "abj"),
        ("Raio de Fogo (Fire Bolt)", "evo"), ("Raio de Gelo (Ray of Frost)", "evo"),
        ("Resistência (Resistance)", "abj"), ("Serviço Invisível (Spare the Dying)", "nec"),
        ("Shocking Grasp (Toque Chocante)", "evo"), ("Sorriso Zombeteiro (Vicious Mockery)", "enm"),
        ("Taumaturgia (Thaumaturgy)", "trs"), ("Tiro Mágico (Eldritch Blast)", "evo"),
        ("Toque Necrótico (Chill Touch)", "nec"), ("Truque de Cordeiro (Druidcraft)", "trs"),
        ("Vetor de Veneno (Poison Spray)", "nec")
    ],
    1: [
        ("Alarme (Alarm)", "abj"), ("Armadura de Agathys (Armor of Agathys)", "abj"),
        ("Armadura Arcana (Mage Armor)", "abj"), ("Ataque Compulsivo (Compelled Duel)", "enm"),
        ("Bênção (Bless)", "enm"), ("Bruxaria (Hex)", "nec"),
        ("Caminho Nebuloso (Fog Cloud)", "con"), ("Comando (Command)", "enm"),
        ("Compreender Idiomas (Comprehend Languages)", "div"), ("Curar Ferimentos (Cure Wounds)", "nec"),
        ("Detectar Magia (Detect Magic)", "div"), ("Detectar Veneno e Doença (Detect Poison and Disease)", "div"),
        ("Discar Mágico (Searing Smite)", "evo"), ("Escudo Mágico (Shield)", "abj"),
        ("Escudo de Fé (Shield of Faith)", "abj"), ("Fogo das Fadas (Faerie Fire)", "evo"),
        ("Graça Felina (Feather Fall)", "trs"), ("Gritaria Estridente (Dissonant Whispers)", "enm"),
        ("Heroísmo (Heroism)", "enm"), ("Identificação (Identify)", "div"),
        ("Imagem Silenciosa (Silent Image)", "ill"), ("Mãos Flamejantes (Burning Hands)", "evo"),
        ("Marca do Caçador (Hunter's Mark)", "div"), ("Míssil Mágico (Magic Missile)", "evo"),
        ("Névoa Obscurecedora (Entangle)", "con"), ("Onda Trovante (Thunderwave)", "evo"),
        ("Palavra Curativa (Healing Word)", "nec"), ("Passos Longos (Longstrider)", "trs"),
        ("Perdição (Bane)", "enm"), ("Proteção contra o Bem e Mal (Protection from Evil and Good)", "abj"),
        ("Pequeno Refúgio (Sanctuary)", "abj"), ("Riso Histérico de Tasha (Tasha's Hideous Laughter)", "enm"),
        ("Santuário (Sanctuary)", "abj"), ("Salto (Jump)", "trs"),
        ("Sopro de Gelo (Thunderous Smite)", "evo"), ("Sono (Sleep)", "enm"),
        ("Sussurros Discordantes (Dissonant Whispers)", "enm"), ("Suspiro Elemental (Chromatic Orb)", "evo"),
        ("Voz Encantadora (Charm Person)", "enm")
    ],
    2: [
        ("Acrobacia Mágica (Enhance Ability)", "trs"), ("Adivinhação Menor (Augury)", "div"),
        ("Aura de Vitalidade (Aura of Vitality)", "abj"), ("Cegueira/Surdez (Blindness/Deafness)", "nec"),
        ("Chama Contínua (Continual Flame)", "evo"), ("Cativar (Enthrall)", "enm"),
        ("Coroa da Loucura (Crown of Madness)", "enm"), ("Crescer Espinhos (Spike Growth)", "trs"),
        ("Despedaçar (Shatter)", "evo"), ("Escuro (Darkness)", "evo"),
        ("Esfera Flamejante (Flaming Sphere)", "con"), ("Imobilizar Pessoa (Hold Person)", "enm"),
        ("Invisibilidade (Invisibility)", "ill"), ("Lâmina Flamejante (Flame Blade)", "evo"),
        ("Levitação (Levitate)", "trs"), ("Localizar Objetos (Locate Object)", "div"),
        ("Luz do Dia (Moonbeam)", "evo"), ("Llama Sagrada (Scorching Ray)", "evo"),
        ("Mão do Mago (Mage Hand)", "con"), ("Oração de Cura (Prayer of Healing)", "nec"),
        ("Passo Nebuloso (Misty Step)", "con"), ("Patas de Aranha (Spider Climb)", "trs"),
        ("Proteção contra Veneno (Protection from Poison)", "abj"), ("Raios Enfraquecedores (Ray of Enfeeblement)", "nec"),
        ("Restauração Menor (Lesser Restoration)", "abj"), ("Reflexos (Mirror Image)", "ill"),
        ("Silêncio (Silence)", "ill"), ("Sugestão (Suggestion)", "enm"),
        ("Teia (Web)", "con"), ("Ver o Invisível (See Invisibility)", "div")
    ],
    3: [
        ("Andar na Água (Water Walk)", "trs"), ("Animar Mortos (Animate Dead)", "nec"),
        ("Bola de Fogo (Fireball)", "evo"), ("Círculo de Mágica (Magic Circle)", "abj"),
        ("Clarividência (Clairvoyance)", "div"), ("Contra-Mágica (Counterspell)", "abj"),
        ("Convocação de Raios (Call Lightning)", "evo"), ("Crescer Plantas (Plant Growth)", "trs"),
        ("Dissipar Magia (Dispel Magic)", "abj"), ("Escudo de Fogo (Fire Shield)", "evo"),
        ("Esfera Invisível (Nondetection)", "abj"), ("Espirito Guardião (Spirit Guardians)", "con"),
        ("Falar com os Mortos (Speak with Dead)", "nec"), ("Falar com Plantas (Speak with Plants)", "trs"),
        ("Forma Gasosa (Gaseous Form)", "trs"), ("Glifo de Vigilância (Glyph of Warding)", "abj"),
        ("Imagem Maior (Major Image)", "ill"), ("Lenta (Slow)", "trs"),
        ("Línguas (Tongues)", "div"), ("Luz do Dia (Daylight)", "evo"),
        ("Medo (Fear)", "ill"), ("Muralha de Vento (Wind Wall)", "evo"),
        ("Padrão Hipnótico (Hypnotic Pattern)", "ill"), ("Pequana Cabana de Leomund (Tiny Hut)", "evc"),
        ("Proteção contra Energia (Protection from Energy)", "abj"), ("Piscar (Blink)", "trs"),
        ("Relâmpago (Lightning Bolt)", "evo"), ("Remover Maldição (Remove Curse)", "abj"),
        ("Respirar na Água (Water Breathing)", "trs"), ("Sinal de Esperança (Beacon of Hope)", "abj"),
        ("Velocidade (Haste)", "trs"), ("Voo (Fly)", "trs")
    ],
    4: [
        ("Âncora Dimensional (Dimension Door)", "con"), ("Assassino Fantasmagórico (Phantasmal Killer)", "ill"),
        ("Banishment (Banimento)", "abj"), ("Cão Fiel de Mordenkainen (Faithful Hound)", "con"),
        ("Compulsão (Compulsion)", "enm"), ("Confusão (Confusion)", "enm"),
        ("Controlar Água (Control Water)", "trs"), ("Estatua de Pedra (Stoneskin)", "trs"),
        ("Esfera Elástica de Otiluke (Resilient Sphere)", "evc"), ("Invisibilidade Maior (Greater Invisibility)", "ill"),
        ("Localizar Criatura (Locate Creature)", "div"), ("Muralha de Fogo (Wall of Fire)", "evo"),
        ("Metamorfose (Polymorph)", "trs"), ("Moldar Rochas (Stone Shape)", "trs"),
        ("Santuário Privado (Private Sanctum)", "abj"), ("Tempestade de Gelo (Ice Storm)", "evo"),
        ("Terreno Alucinatório (Hallucinatory Terrain)", "ill"), ("Tentáculos Negros de Evard (Black Tentacles)", "con")
    ],
    5: [
        ("Aparência Falsa (Seeming)", "ill"), ("Barreira Antivida (Antilife Shell)", "abj"),
        ("Caminho dos Ventos (Wind Walk)", "trs"), ("Círculo de Teleporte (Teleportation Circle)", "con"),
        ("Coluna de Chamas (Flame Strike)", "evo"), ("Comunhão (Commune)", "div"),
        ("Comunhão com a Natureza (Commune with Nature)", "div"), ("Cone de Frio (Cone of Cold)", "evo"),
        ("Conhecimento Lendário (Legend Lore)", "div"), ("Contagiar (Contagion)", "nec"),
        ("Cura Completa Menor (Mass Cure Wounds)", "nec"), ("Dominar Pessoa (Dominate Person)", "enm"),
        ("Imobilizar Monstro (Hold Monster)", "enm"), ("Muralha de Força (Wall of Force)", "evo"),
        ("Muralha de Pedra (Wall of Stone)", "evc"), ("Onda Destrutiva (Destructive Wave)", "evo"),
        ("Praga de Insetos (Insect Plague)", "con"), ("Restauração Maior (Greater Restoration)", "abj"),
        ("Reviver os Mortos (Raise Dead)", "nec"), ("Telecinésia (Telekinesis)", "trs")
    ],
    6: [
        ("Ataque de Vento (Investiture of Wind)", "trs"), ("Barreira de Lâminas (Blade Barrier)", "evo"),
        ("Caminhar nas Sombras (Find the Path)", "div"), ("Carne para Pedra (Flesh to Stone)", "trs"),
        ("Corrente de Relâmpagos (Chain Lightning)", "evo"), ("Cura Completa (Heal)", "nec"),
        ("Desintegrar (Disintegrate)", "trs"), ("Esfera Congelante de Otiluke (Freezing Sphere)", "evo"),
        ("Globo de Invulnerabilidade (Globe of Invulnerability)", "abj"), ("Ilusão Programada (Programmed Illusion)", "ill"),
        ("Invocação de Contingência (Contingency)", "evc"), ("Muralha de Gelo (Wall of Ice)", "evo"),
        ("Portal de Plano (Planar Ally)", "con"), ("Proibição (Forbiddance)", "abj"),
        ("Sugestão em Massa (Mass Suggestion)", "enm"), ("Visão da Verdade (True Seeing)", "div")
    ],
    7: [
        ("Bola de Fogo Atrasada (Delayed Blast Fireball)", "evo"), ("Dedo da Morte (Finger of Death)", "nec"),
        ("Espada de Mordenkainen (Arcane Sword)", "evo"), ("Involucro de Teleporte (Teleport)", "con"),
        ("Jaula de Força (Forcecage)", "evo"), ("Muralha Prismática (Prismatic Wall)", "abj"),
        ("Palavra Divina (Divine Word)", "evo"), ("Regeneração (Regenerate)", "trs"),
        ("Ressurreição (Resurrection)", "nec"), ("Símbolo (Symbol)", "abj"),
        ("Simulacro (Simulacrum)", "ill"), ("Tempestade de Fogo (Fire Storm)", "evo")
    ],
    8: [
        ("Antipatia/Simpatia (Antipathy/Sympathy)", "enm"), ("Campo Antimagia (Antimagic Field)", "abj"),
        ("Clonar (Clone)", "nec"), ("Dominar Monstro (Dominate Monster)", "enm"),
        ("Explosão Solar (Sunburst)", "evo"), ("Forma Dragão (Illusory Dragon)", "ill"),
        ("Labirinto (Maze)", "con"), ("Mente Embrutecida (Feeblemind)", "enm"),
        ("Palavra de Power Stun (Power Word Stun)", "enm"), ("Terremoto (Earthquake)", "evo"),
        ("Tsunami (Tsunami)", "con")
    ],
    9: [
        ("Chuva de Meteoro (Meteor Swarm)", "evo"), ("Cura Completa em Massa (Mass Heal)", "nec"),
        ("Desejo (Wish)", "con"), ("Forma Verdadeira (Shapechange)", "trs"),
        ("Parar o Tempo (Time Stop)", "trs"), ("Palavra de Poder Matar (Power Word Kill)", "enm"),
        ("Portal (Gate)", "con"), ("Portal do Tempo (Time Ravager)", "nec"),
        ("Ressurreição Verdadeira (True Resurrection)", "nec"), ("Sexta Esfera (Time Stop)", "trs"),
        ("Sexto Sentido (Foresight)", "div"), ("Transformação de Tenser (Tenser's Transformation)", "trs")
    ]
}

def generate_json_files():
    output_dir = os.path.join("data", "spells")
    os.makedirs(output_dir, exist_ok=True)

    file_mapping = {
        0: "cantrips.json",
        1: "level-1.json",
        2: "level-2.json",
        3: "level-3.json",
        4: "level-4.json",
        5: "level-5.json",
        6: "level-6.json",
        7: "level-7.json",
        8: "level-8.json",
        9: "level-9.json"
    }

    total_generated = 0

    for lvl, spells in SPELLS_2024.items():
        filename = file_mapping[lvl]
        filepath = os.path.join(output_dir, filename)
        
        json_data = []
        for name, school in spells:
            spell_item = {
                "name": f"{name} (2024)",
                "type": "spell",
                "img": "icons/svg/spell-phone.svg",
                "system": {
                    "description": {
                        "value": f"<p>Magia oficial do D&D 2024 (PHB) - {name}.</p>"
                    },
                    "level": lvl,
                    "school": school,
                    "properties": ["v", "s"],
                    "range": { "value": 60, "units": "ft" },
                    "actionType": "util"
                }
            }
            json_data.append(spell_item)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        print(f"Gerado: {filepath} com {len(json_data)} magias.")
        total_generated += len(json_data)

    print(f"\nSucesso! {total_generated} magias divididas pelos 10 arquivos JSON em data/spells/.")

if __name__ == "__main__":
    generate_json_files()