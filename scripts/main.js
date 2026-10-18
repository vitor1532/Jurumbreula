// Função para higienizar IDs do Foundry VTT (garante 16 caracteres alfanuméricos)
function fixItemIds(item) {
    const cleanItem = JSON.parse(JSON.stringify(item));

    if (cleanItem._id && typeof cleanItem._id === 'string' && cleanItem._id.length !== 16) {
        delete cleanItem._id;
    }

    if (cleanItem.system && Array.isArray(cleanItem.system.advancement)) {
        cleanItem.system.advancement = cleanItem.system.advancement.map(adv => {
            if (adv._id && typeof adv._id === 'string' && adv._id.length !== 16) {
                adv._id = foundry.utils.randomID();
            }
            return adv;
        });
    }

    return cleanItem;
}

Hooks.once('ready', async () => {
    if (!game.user.isGM) return;

    const classPack = game.packs.get("Jurumbleura.classes-55e");
    const subclassPack = game.packs.get("Jurumbleura.subclasses-55e");
    const spellPack = game.packs.get("Jurumbleura.spells-55e");

    if (!classPack || !subclassPack || !spellPack) return;

    // --- 1. IMPORTAÇÃO DAS CLASSES E SUBCLASSES ---
    const classIndex = await classPack.getIndex();
    if (classIndex.size === 0) {
        ui.notifications.info("Jurumbleura | Populando compêndios de Classes e Subclasses...");

        try {
            const response = await fetch("modules/Jurumbleura/data/classes-and-subclasses-2024.json");
            const itemsData = await response.json();

            await classPack.configure({ locked: false });
            await subclassPack.configure({ locked: false });

            // Importa Subclasses
            const rawSubclasses = itemsData.filter(item => item.type === "subclass").map(fixItemIds);
            const createdSubclasses = await Item.createDocuments(rawSubclasses, { pack: "Jurumbleura.subclasses-55e" });

            // Mapeia os UUIDs das subclasses por classIdentifier
            const classToSubclassUuids = {};
            createdSubclasses.forEach(subcls => {
                const classId = subcls.system?.classIdentifier;
                if (classId) {
                    if (!classToSubclassUuids[classId]) classToSubclassUuids[classId] = [];
                    classToSubclassUuids[classId].push(subcls.uuid);
                }
            });

            // Importa Classes com pool de subclasses atualizado
            const rawClasses = itemsData.filter(item => item.type === "class").map(fixItemIds);
            const classes = rawClasses.map(cls => {
                const classIdentifier = cls.system?.identifier;
                const matchingSubclassUuids = classToSubclassUuids[classIdentifier] || [];

                if (cls.system && Array.isArray(cls.system.advancement)) {
                    cls.system.advancement.forEach(adv => {
                        if (adv.type === "ItemChoice" && adv.configuration) {
                            adv.configuration.pool = matchingSubclassUuids;
                        }
                    });
                }
                return cls;
            });

            await Item.createDocuments(classes, { pack: "Jurumbleura.classes-55e" });

            await classPack.configure({ locked: true });
            await subclassPack.configure({ locked: true });

            ui.notifications.info("Jurumbleura | Compêndios de Classes criados com sucesso!");
        } catch (error) {
            console.error("Jurumbleura | Erro ao carregar Classes/Subclasses:", error);
        }
    }

    // --- 2. IMPORTAÇÃO DAS MAGIAS (MULTIPLOS ARQUIVOS JSON) ---
    const spellIndex = await spellPack.getIndex();
    if (spellIndex.size === 0) {
        ui.notifications.info("Jurumbleura | Populando compêndio de Magias por Nível (PHB 2024)...");

        // Lista de todos os arquivos de magias
        const spellFiles = [
            "cantrips.json",
            "level-1.json",
            "level-2.json",
            "level-3.json",
            "level-4.json",
            "level-5.json",
            "level-6.json",
            "level-7.json",
            "level-8.json",
            "level-9.json"
        ];

        try {
            await spellPack.configure({ locked: false });

            let allSpellsData = [];

            // Lê cada arquivo individualmente e agrupa no array principal
            for (const file of spellFiles) {
                const response = await fetch(`modules/Jurumbleura/data/spells/${file}`);
                if (response.ok) {
                    const spells = await response.json();
                    allSpellsData = allSpellsData.concat(spells);
                } else {
                    console.warn(`Jurumbleura | Não foi possível carregar modules/Jurumbleura/data/spells/${file}`);
                }
            }

            const cleanSpells = allSpellsData.map(fixItemIds);
            await Item.createDocuments(cleanSpells, { pack: "Jurumbleura.spells-55e" });

            await spellPack.configure({ locked: true });

            ui.notifications.info(`Jurumbleura | Compêndio com ${cleanSpells.length} Magias criado com sucesso!`);
        } catch (error) {
            console.error("Jurumbleura | Erro ao carregar arquivos de Magias:", error);
        }
    }
});