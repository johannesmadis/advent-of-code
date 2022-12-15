const { AmplifierPipeline } = require('./AmplifierPipeline');

class LoopedAmplifierPipeline extends AmplifierPipeline {
  run() {
    const lastAmplifierIndex = this.amplifiers.length - 1;
    let i = 0;
    let ampOutput = 0;
    while (!this.amplifiers[lastAmplifierIndex].isTerminated) {
      const ampIndex = i % 5;
      const output = this.amplifiers[ampIndex].run(ampOutput);
      if (output !== null) {
        ampOutput = output;
      } else {
        break;
      }
      i += 1;
    }
    return ampOutput;
  }
}
exports.LoopedAmplifierPipeline = LoopedAmplifierPipeline;
