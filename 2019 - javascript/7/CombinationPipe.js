const G = require('generatorics');
const { AmplifierPipeline } = require('./AmplifierPipeline');
const { LoopedAmplifierPipeline } = require('./LoopedAmplifierPipeline');

class CombinationPipe {
  constructor({ memory, base, isLooped = false }) {
    this.base = base;
    this.memory = memory;
    this.combinations = [];
    this.isLooped = isLooped;
    this.makeCombinations();
  }

  makeCombinations() {
    const generator = G.permutation(this.base);
    let value;
    let done;
    do {
      ({ value, done } = generator.next());
      if (value) this.combinations.push([...value]);
    } while (!done);
  }

  run() {
    return this.combinations.map((combination) => {
      const Pipeline = this.isLooped
        ? LoopedAmplifierPipeline
        : AmplifierPipeline;
      const amp = new Pipeline({
        memory: this.memory,
        phases: combination,
      });
      return amp.run();
    });
  }
}

exports.CombinationPipe = CombinationPipe;
