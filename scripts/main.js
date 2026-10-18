// Função auxiliar para higienizar os _ids do item e de seus advancements
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
    // 1. Confirmação de execução do Módulo
    console.log("%cJurumbreula | Hook 'ready' executado!", "color: #00ff00; font-weight: bold; font-size: 14px;");

    if (!game.user.isGM) {
        console.log("Jurumbreula | Usuário não é GM. Importação ignorada.");
        return;
    }

    const classPack = game.packs.get("Jurumbreula.classes-55e");
    const subclassPack = game.packs.get("Jurumbreula.subclasses-55e");
    const spellPack = game.packs.get("Jurumbreula.spells-55e");

    if (!classPack || !subclassPack || !spellPack) {
        ui.notifications.error("Jurumbreula | ERRO: Compêndios não encontrados! Verifique o nome da pasta e do ID do módulo.");
        console.error("Jurumbreula | Compêndios ausentes:", { classPack, subclassPack, spellPack });
        return;
    }

    // --- 1. IMPORTAÇÃO DAS MAGIAS ---
    try {
        const spellIndex = await spellPack.getIndex();
        console.log(`Jurumbreula | Magias encontradas no compêndio: ${spellIndex.size}`);

        if (spellIndex.size === 0) {
            ui.notifications.info("Jurumbreula | Iniciando importação de Magias 2024...");
            await spellPack.configure({ locked: false });

            const spellFiles = [
                "cantrips.json", "level-1.json", "level-2.json", "level-3.json",
                "level-4.json", "level-5.json", "level-6.json", "level-7.json",
                "level-8.json", "level-9.json"
            ];

            let allSpellsData = [];
            for (const file of spellFiles) {
                const response = await fetch(`modules/Jurumbreula/data/spells/${file}`);
                if (response.ok) {
                    const spells = await response.json();
                    allSpellsData = allSpellsData.concat(spells);
                } else {
                    console.warn(`Jurumbreula | Não foi possível encontrar modules/Jurumbreula/data/spells/${file}`);
                }
            }

            if (allSpellsData.length > 0) {
                const cleanSpells = allSpellsData.map(fixItemIds);
                await Item.createDocuments(cleanSpells, { pack: "Jurumbreula.spells-55e" });
                ui.notifications.info(`Jurumbreula | Sucesso! ${cleanSpells.length} magias importadas.`);
            } else {
                ui.notifications.warn("Jurumbreula | Nenhum dado de magia foi encontrado nos arquivos JSON.");
            }

            await spellPack.configure({ locked: true });
        }
    } catch (error) {
        console.error("Jurumbreula | Erro na importação de magias:", error);
    }

    // --- 2. IMPORTAÇÃO DE CLASSES E SUBCLASSES ---
    try {
        const classIndex = await classPack.getIndex();
        console.log(`Jurumbreula | Classes encontradas no compêndio: ${classIndex.size}`);

        if (classIndex.size === 0) {
            ui.notifications.info("Jurumbreula | Iniciando importação de Classes e Subclasses...");
            await classPack.configure({ locked: false });
            await subclassPack.configure({ locked: false });

            const response = await fetch("modules/Jurumbreula/data/classes-and-subclasses-2024.json");
            if (!response.ok) {
                throw new Error("Falha ao realizar fetch do arquivo classes-and-subclasses-2024.json");
            }

            const itemsData = await response.json();
            const rawSubclasses = itemsData.filter(item => item.type === "subclass").map(fixItemIds);
            const rawClasses = itemsData.filter(item => item.type === "class").map(fixItemIds);

            await Item.createDocuments(rawSubclasses, { pack: "Jurumbreula.subclasses-55e" });
            await Item.createDocuments(rawClasses, { pack: "Jurumbreula.classes-55e" });

            await classPack.configure({ locked: true });
            await subclassPack.configure({ locked: true });

            ui.notifications.info("Jurumbreula | Classes e Subclasses importadas com sucesso!");
        }
    } catch (error) {
        console.error("Jurumbreula | Erro na importação de classes/subclasses:", error);
    }
});