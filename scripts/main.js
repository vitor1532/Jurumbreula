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
    if (!game.user.isGM) return;

    const classPack = game.packs.get("Jurumbreula.classes-55e");
    const subclassPack = game.packs.get("Jurumbreula.subclasses-55e");

    if (!classPack || !subclassPack) return;

    const classIndex = await classPack.getIndex();
    if (classIndex.size === 0) {
        ui.notifications.info("Jurumbreula | Populando compêndios do módulo pela primeira vez...");

        try {
            const response = await fetch("modules/Jurumbreula/data/classes-and-subclasses-2024.json");
            const itemsData = await response.json();

            // Desbloqueia os compêndios para escrita
            await classPack.configure({ locked: false });
            await subclassPack.configure({ locked: false });

            // 1. Prepara e CRIA PRIMEIRO AS SUBCLASSES
            const rawSubclasses = itemsData.filter(item => item.type === "subclass").map(fixItemIds);
            const createdSubclasses = await Item.createDocuments(rawSubclasses, { pack: "Jurumbreula.subclasses-55e" });

            // Mapeia cada classe (classIdentifier) para um array de UUIDs das suas subclasses
            // Exemplo: { "guerreiro-2024": ["Compendium.Jurumbreula.subclasses-55e.Item...", ...] }
            const classToSubclassUuids = {};
            
            createdSubclasses.forEach(subcls => {
                const classId = subcls.system?.classIdentifier;
                if (classId) {
                    if (!classToSubclassUuids[classId]) {
                        classToSubclassUuids[classId] = [];
                    }
                    classToSubclassUuids[classId].push(subcls.uuid);
                }
            });

            // 2. Prepara as CLASSES e vincula APENAS as subclasses pertencentes a ela
            const rawClasses = itemsData.filter(item => item.type === "class").map(fixItemIds);

            const classes = rawClasses.map(cls => {
                const classIdentifier = cls.system?.identifier;
                // Obtém apenas os UUIDs das subclasses pertencentes a este identifier específico
                const matchingSubclassUuids = classToSubclassUuids[classIdentifier] || [];

                if (cls.system && Array.isArray(cls.system.advancement)) {
                    cls.system.advancement.forEach(adv => {
                        if (adv.type === "ItemChoice" && adv.configuration) {
                            // Atribui estritamente a lista de UUIDs correspondentes a esta classe
                            adv.configuration.pool = matchingSubclassUuids;
                        }
                    });
                }
                return cls;
            });

            // 3. Cria as CLASSES com os UUIDs perfeitamente filtrados e validados
            await Item.createDocuments(classes, { pack: "Jurumbreula.classes-55e" });

            // Bloqueia novamente os compêndios
            await classPack.configure({ locked: true });
            await subclassPack.configure({ locked: true });

            ui.notifications.info("Jurumbreula | Compêndios de Classes e Subclasses criados com sucesso!");
        } catch (error) {
            console.error("Jurumbreula | Erro ao carregar o arquivo JSON:", error);
        }
    }
});