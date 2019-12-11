const { asteroidMap } = require('./10_input');
const Vector2 = require('./Vector2');

const input = `.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##`;

const ASTEROID = '#';
const SPACE = '.';

class Station {
  constructor(map) {
    this.input = map;
    const { asteroidMap, asteroidArray } = this.parse();
    this.map = asteroidMap;
    this.asteroidArray = asteroidArray;
    this.height = this.map.length;
    this.width = this.map[0].length;
  }

  parse() {
    const rows = this.input.split(/\r?\n/g);
    const asteroidArray = [];
    const asteroidMap = rows.map((row, rowIndex) => {
      const rowArray = row.split('');
      return rowArray.map((space, spaceIndex) => {
        const isAsteroid = space === ASTEROID;
        if (isAsteroid) {
          asteroidArray.push({ y: rowIndex, x: spaceIndex });
        }
        return isAsteroid;
      });
    });
    return { asteroidArray, asteroidMap };
  }

  collide(x, y) {
    const collisions = {};

    // record vectors, unitise each (but remember length)
    this.asteroidArray.forEach((asteroidCoords) => {
      const deltaX = asteroidCoords.x - x;
      const deltaY = asteroidCoords.y - y;

      if (!(deltaY === 0 && deltaX === 0)) {
        // make vectors
        const vector = new Vector2(deltaX, deltaY);
        if (
          (collisions[vector.angle]
            && collisions[vector.angle].magnitude > vector.magnitude)
          || !collisions[vector.angle]
        ) {
          collisions[vector.angle] = vector;
        }
      }
    });
    return collisions;
  }

  findRayCollisions() {
    const collisions = this.asteroidArray.map((asteroidCoords) => {
      const collisionVectors = this.collide(asteroidCoords.x, asteroidCoords.y);

      const collisionCount = Object.values(collisionVectors).length;

      return { ...asteroidCoords, count: collisionCount };
    });
    return collisions;
  }

  findAsteroid(x, y, index) {
    const collisions = this.collide(x, y);
    const collisionVectors = Object.values(collisions);

    collisionVectors.sort((vectorA, vectorB) => vectorA.angle - vectorB.angle);

    const vector = collisionVectors[index];
    const originalX = vector.x + x;
    const originalY = vector.y + y;
    const originalAsteroid = this.asteroidArray.find(
      (asteroid) => asteroid.x === originalX && asteroid.y === originalY,
    );

    collisionVectors.map((vector, vectorI) => console.log(vectorI, vector.x, vector.y));
    console.log('original', originalAsteroid);

    return {
      ...collisionVectors[index],
      resultX: collisionVectors[index].x + x,
      resultY: collisionVectors[index].y + y,
    };
  }

  findAsteroid2(x, y, index) {
    const rounds = []; // map all to rounds, later sort
    const allCollisions = this.collideAll(x, y);

    allCollisions.forEach((quarter) => {
      const vectorArray = Object.values(quarter);
      vectorArray.forEach((vectorsForAngle) => {
        vectorsForAngle.forEach((vector, vectorIndex) => {
          rounds[vectorIndex] = rounds[vectorIndex] || [];
          rounds[vectorIndex].push(vector);
        });
      });
    });

    let i = 0;
    let roundIndex = 0;
    let currentVector;

    while (i <= index && !currentVector) {
      const round = rounds[roundIndex];

      if (round.length + i >= index) {
        // sort round by angles.
        const sortedRound = round.sort((vectorA, vectorB) => {
          if (vectorA.quarter === vectorB.quarter) {
            return vectorB.angle - vectorA.angle;
          }
          return vectorA.quarter - vectorB.quarter;
        });

        const sortedRoundIndex = index - i;
        currentVector = sortedRound[sortedRoundIndex];
        break;
      } else {
        i += round.length;
        roundIndex += 1;
      }
    }
  }
}

const station = new Station(asteroidMap);
const locations = station.findRayCollisions();

const counts = locations.map(({ count }) => count);
const maxCount = Math.max(...counts);

const bestLocation = locations.find(({ count }) => count === maxCount);

const bettingTarget = station.findAsteroid(bestLocation.x, bestLocation.y, 199);
console.log(bestLocation);
console.log(bettingTarget);
