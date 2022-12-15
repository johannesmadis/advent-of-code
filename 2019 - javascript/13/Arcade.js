const IntCode = require('./IntCode');

/*
0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects. */

const TILE_EMPTY = 0;
const TILE_WALL = 1;
const TILE_BLOCK = 2;
const TILE_PADDLE = 3;
const TILE_BALL = 4;
const JOYSTICK_NEUTRAL = 0;
const JOYSTICK_LEFT = -1;
const JOYSTICK_RIGHT = 1;

class Arcade {
  constructor(memory) {
    this.program = new IntCode({
      memory,
      pauseAfterOutput: true,
    });
    this.map = [];
    this.score = 0;
    this.paddle = {};
  }

  run() {
    let ball;
    let paddle;
    let movement;
    while (!this.program.terminated) {
      const [x] = this.program.run(movement);
      movement = undefined;
      const [y] = this.program.run();
      const [id] = this.program.run();

      if (x < 0) {
        // display score
        this.score = id;
      } else {
        // get board
        this.map[y] = this.map[y] || [];
        this.map[y][x] = id;
        if (id === TILE_PADDLE) {
          paddle = { x, y };
        } else if (id === TILE_BALL) {
          ball = { x, y };
          // new ball, update movement
          if (ball && paddle) {
            if (ball.x > paddle.x) {
              movement = JOYSTICK_RIGHT;
            } else if (ball.x < paddle.x) {
              movement = JOYSTICK_LEFT;
            } else if (ball.x === paddle.x) {
              movement = JOYSTICK_NEUTRAL;
            }
          }
        }
      }
    }
  }

  draw() {
    this.map.forEach((row) => {
      let rowStr = '';
      row.forEach((block) => {
        let blockChar;
        switch (block) {
          case TILE_EMPTY:
            blockChar = '  ';
            break;
          case TILE_BALL:
            blockChar = '()';
            break;
          case TILE_WALL:
            blockChar = '##';
            break;
          case TILE_BLOCK:
            blockChar = '[]';
            break;
          case TILE_PADDLE:
            blockChar = '__';
            break;
          default:
            console.log('unknown tile', blockChar);
            blockChar = '??';
        }
        rowStr += blockChar;
      });
      console.log(rowStr);
    });
  }
}

module.exports = Arcade;
