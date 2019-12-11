const { initialMemory } = require('./7_input');
const { CombinationPipe } = require('./CombinationPipe');

const combinationPipe = new CombinationPipe({
  memory: initialMemory,
  base: [0, 1, 2, 3, 4],
});
const results = combinationPipe.run();
console.log(Math.max(...results));

const feedbackCombinationPipe = new CombinationPipe({
  memory: initialMemory,
  isLooped: true,
  base: [5, 6, 7, 8, 9],
});
const feedbackResults = feedbackCombinationPipe.run();
console.log(Math.max(...feedbackResults));
