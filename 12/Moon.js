class Moon {
  constructor(id, x, y, z) {
    this.id = id;
    this.x = x;
    this.y = y;
    this.z = z;
    this.vX = 0;
    this.vY = 0;
    this.vZ = 0;
  }

  applyGravity(vX, vY, vZ) {
    this.vX += vX;
    this.vY += vY;
    this.vZ += vZ;
  }

  updatePosition() {
    this.x += this.vX;
    this.y += this.vY;
    this.z += this.vZ;
  }

  getKineticEnergy() {
    return Math.abs(this.vX) + Math.abs(this.vY) + Math.abs(this.vZ);
  }

  getPotentialEnergy() {
    return Math.abs(this.x) + Math.abs(this.y) + Math.abs(this.z);
  }

  getTotalEnergy() {
    return this.getKineticEnergy() * this.getPotentialEnergy();
  }

  step() {
    this.updatePosition();
  }
}

module.exports = Moon;
