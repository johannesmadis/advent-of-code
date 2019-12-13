const { input } = require('./input');
const Arcade = require('./Arcade');

// calculate inputs based on map data

const hackedInput = [...input];
hackedInput[0] = 2;

const arcade2 = new Arcade(hackedInput);
arcade2.run();
arcade2.draw();
console.log('arcade', arcade2.score);
