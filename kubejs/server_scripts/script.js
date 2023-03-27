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
	event.remove({ output: "advancedperipherals:player_detector" })
	event.custom({
		"type": "immersiveengineering:arc_furnace",
		"additives": [
			{
				"tag": "forge:ingots/netherite"
			},
			{
				"tag": "forge:ingots/thallasium"
			},
			{
				"tag": "forge:ingots/constantan"
			},
		],
		conditions: [
			{
				"type": "forge:not",
				"value": {
					"type": "forge:tag_empty",
					"tag": "forge:ingots/netherite"
				}
			},
			{
				"type": "forge:not",
				"value": {
					"type": "forge:tag_empty",
					"tag": "forge:ingots/thallasium"
				}
			},
			{
				"type": "forge:not",
				"value": {
					"type": "forge:tag_empty",
					"tag": "forge:ingots/constantan"
				}
			}
		],
		"energy": 320000,
		"input": {
			"item": "advancedperipherals:environment_detector"
		},
		"results": [
			{
				"base_ingredient": {
					"item": "advancedperipherals:player_detector"
				},
				"count": 1,
			}
		],
		"secondaries": [
			{
				"chance": 0.75,
				"output": {
					"item": "advancedperipherals:player_detector"
				}
			}
		],
		"time": 6000
	})
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