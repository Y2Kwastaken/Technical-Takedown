// priority: 0

settings.logAddedRecipes = true
settings.logRemovedRecipes = true
settings.logSkippedRecipes = false
settings.logErroringRecipes = true

console.info('Hello, World! (You will see this line every time server resources reload)')

onEvent('block.loot_tables', event => {
	event.addSimpleBlock('iceandfire:silver_ore', 'immersiveengineering:ore_silver')
	event.addSimpleBlock('iceandfire:copper_ore', 'immersiveengineering:ore_copper')
})

