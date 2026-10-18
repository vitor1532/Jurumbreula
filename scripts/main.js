Hooks.once('ready', async () => {
    // Apenas o GM executa a rotina de criação inicial dos compêndios
    if (!game.user.isGM) return;

    const classPack = game.packs.get("Jurumbleura.classes-55e");
    const subclassPack = game.packs.get("Jurumbleura.subclasses-55e");
    const spellPack = game.packs.get("Jurumbleura.spells-55e");

    if (!classPack || !subclassPack || !spellPack) return;

    // 1. Importa Magias se o compêndio estiver vazio
    if ((await spellPack.getIndex()).size === 0) {
        ui.notifications.info("Jurumbleura | Importando biblioteca de Magias 2024...");
        try {
            await spellPack.configure({ locked: false });
            
            const files = [
                "cantrips.json", "level-1.json", "level-2.json", "level-3.json",
                "level-4.json", "level-5.json", "level-6.json", "level-7.json",
                "level-8.json", "level-9.json"
            ];

            let allSpells = [];
            for (const file of files) {
                const res = await fetch(`modules/Jurumbleura/data/spells/${file}`);
                if (res.ok) {
                    const data = await res.json();
                    allSpells = allSpells.concat(data);
                }
            }

            await Item.createDocuments(allSpells, { pack: "Jurumbleura.spells-55e" });
            await spellPack.configure({ locked: true });
            ui.notifications.info("Jurumbleura | Magias importadas com sucesso!");
        } catch (e) {
            console.error("Jurumbleura | Erro ao carregar Magias:", e);
        }
    }

    // 2. Importa Classes e Subclasses vinculadas
    if ((await classPack.getIndex()).size === 0) {
        ui.notifications.info("Jurumbleura | Importando Classes e Subclasses integradas...");
        try {
            await classPack.configure({ locked: false });
            await subclassPack.configure({ locked: false });

            const res = await fetch("modules/Jurumbleura/data/classes-and-subclasses-2024.json");
            const data = await res.json();

            const subclasses = data.filter(i => i.type === "subclass");
            const classes = data.filter(i => i.type === "class");

            // Cria Subclasses primeiro e Classes depois
            await Item.createDocuments(subclasses, { pack: "Jurumbleura.subclasses-55e" });
            await Item.createDocuments(classes, { pack: "Jurumbleura.classes-55e" });

            await classPack.configure({ locked: true });
            await subclassPack.configure({ locked: true });

            ui.notifications.info("Jurumbleura | Classes e Subclasses registradas com sucesso!");
        } catch (e) {
            console.error("Jurumbleura | Erro ao carregar Classes/Subclasses:", e);
        }
    }
});