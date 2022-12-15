class Vector2 {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.magnitude = Math.sqrt(x * x + y * y);
    this.normalised = {
      magnitude: this.magnitude,
      x: x / this.magnitude,
      y: y / this.magnitude,
    };
    const angle = Math.atan2(x, -y); // not y,x to get 0 up and clockwise
    const rotatedAngle = angle;
    this.angle = rotatedAngle < 0 ? rotatedAngle + 2 * Math.PI : rotatedAngle;
  }
}

module.exports = Vector2;
