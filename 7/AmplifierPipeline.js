const { IntCode } = require('./IntCode');

class AmplifierPipeline {
  constructor({ memory, phases }) {
    this.phases = phases;
    this.amplifiers = phases.map(
      (phase) => new IntCode({ memory, initialInput: phase }),
    );
  }

  run() {
    const output = this.amplifiers.reduce(
      (result, amplifier) => amplifier.run(result),
      0,
    );
    return output;
  }
}

exports.AmplifierPipeline = AmplifierPipeline;
