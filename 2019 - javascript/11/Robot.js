const IntCode = require('./IntCode');

const DIR_UP = 0;
const DIR_RIGHT = 1;
const DIR_DOWN = 2;
const DIR_LEFT = 3;
const TURN_LEFT = 0;
const TURN_RIGHT = 1;

class Robot {
  constructor(memory, initialColor) {
    this.map = { 0: { 0: initialColor } }; // y and x
    this.painter = new IntCode({ memory, pauseAfterOutput: true });
    this.direction = DIR_UP;
    this.positionX = 0;
    this.positionY = 0;
    this.tileCounter = 1; // not 0 because tile for map is defined upwards
    this.totalOps = 0;
  }

  turn(turn) {
    if (turn === TURN_RIGHT) {
      this.direction = (this.direction + 1) % 4;
    } else if (turn === TURN_LEFT) {
      this.direction = this.direction === DIR_UP ? DIR_LEFT : this.direction - 1;
    }
    this.advance();
  }

  advance() {
    switch (this.direction) {
      case DIR_LEFT:
        this.positionX -= 1;
        break;
      case DIR_RIGHT:
        this.positionX += 1;
        break;
      case DIR_DOWN:
        this.positionY -= 1;
        break;
      case DIR_UP:
        this.positionY += 1;
        break;
      default:
        console.log('ERROR, unknown direction', this.direction);
    }
  }

  paint(color) {
    // record position,
    this.map[this.positionY] = this.map[this.positionY] || {};
    if (this.map[this.positionY][this.positionX] === undefined) {
      this.tileCounter += 1;
    }
    this.map[this.positionY][this.positionX] = color;
    this.totalOps += 1;
  }

  step(currentColor = 0) {
    let color;
    let turn;
    if (!this.painter.terminated) {
      const output = this.painter.run(currentColor);
      [color] = output;
    }
    if (!this.painter.terminated) {
      [turn] = this.painter.run();
    }

    if (!this.painter.terminated) {
      if (color !== undefined) this.paint(color);
      if (turn !== undefined) this.turn(turn);
    }
  }

  run() {
    while (!this.painter.terminated) {
      // get current position color
      let currentColor = 0;
      if (
        this.map[this.positionY]
        && this.map[this.positionY][this.positionX] !== undefined
      ) {
        currentColor = this.map[this.positionY][this.positionX];
      }
      this.step(currentColor);
    }
    return this.map;
  }
}

module.exports = Robot;
