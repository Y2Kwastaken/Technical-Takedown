// priority: 0

settings.logAddedRecipes = true
settings.logRemovedRecipes = true
settings.logSkippedRecipes = false
settings.logErroringRecipes = true

console.info('Hello, World! (You will see this line every time server resources reload)')

onEvent('block.loot_tables', event => {
	event.addSimpleBlock('iceandfire:copper_ore', 'create:copper_ore')
	event.addSimpleBlock('iceandfire:silver_ore', 'immersiveengineering:ore_silver')
})

onEvent('recipes', event => {
	event.shapeless('occultism:datura_seeds', ['minecraft:dragon_breath', 'minecraft:wheat_seeds'])
})

onEvent('lootjs', event => {
	event
		.addBlockLootModifier('minecraft:tall_grass')
		.thenRemove('occultism:datura_seeds')

	event
		.addBlockLootModifier('minecraft:grass')
		.thenRemove('occultism:datura_seeds')
})

onEvent('player.logged_in', event => {

	if (event.player.stages.has('starting_items')) {
		return;
	}

	event.player.stages.add('starting_items');
	event.player.give('minecraft:stone_sword')
	event.player.give('minecraft:stone_pickaxe')
	event.player.give('minecraft:stone_axe')
	event.player.give('minecraft:stone_shovel')
	event.player.give('16x farmersdelight:roast_chicken')
})