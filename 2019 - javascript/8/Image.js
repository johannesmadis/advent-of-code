const imageInput = require('./Image_input');

const COLOR_BLACK = 0;
const COLOR_WHITE = 1;
const COLOR_TRANSPARENT = 2;

class Image {
  constructor({ width, height, data }) {
    this.width = width;
    this.height = height;
    this.data = data;
    this.layers = [];
    this.visibleLayer = [];
    this.fillLayers();
    this.getImage();
  }

  fillLayers() {
    const length = this.width * this.height;
    for (let i = 0; i < this.data.length; i += length) {
      const layerData = this.data.substr(i, length);
      const layerArr = [...layerData].map((char) => Number(char));

      let countBlack = 0;
      let countWhite = 0;
      let countTransparent = 0;

      layerArr.forEach((number) => {
        if (number === COLOR_BLACK) {
          countBlack += 1;
        } else if (number === COLOR_WHITE) {
          countWhite += 1;
        } else if (number === COLOR_TRANSPARENT) {
          countTransparent += 1;
        }
      });
      this.layers.push({
        countBlack,
        countWhite,
        countTransparent,
        data: layerArr,
      });
    }
  }

  getImage() {
    this.layers.reverse().forEach(({ data }) => {
      data.forEach((integer, index) => {
        if (integer === COLOR_BLACK || integer === COLOR_WHITE) {
          this.visibleLayer[index] = integer;
        }
      });
    });
  }

  getLayers() {
    return this.layers;
  }

  outputImage() {
    for (let i = 0; i < this.height; i += 1) {
      const index = i * this.width;
      const items = this.visibleLayer.slice(index, index + this.width);
      const str = items.map((item) => {
        if (item === COLOR_BLACK) {
          return ' ';
        }
        return 'O';
      });
      const lineStr = str.join('');
      console.log(lineStr);
    }
  }

  getCheckSum() {
    let leastDigitsLayer = { countBlack: Infinity };
    this.layers.forEach((layer) => {
      if (layer.countBlack < leastDigitsLayer.countBlack) {
        leastDigitsLayer = layer;
      }
    });
    return leastDigitsLayer.countWhite * leastDigitsLayer.countTransparent;
  }
}

const image = new Image({ height: 6, width: 25, data: imageInput.data });

console.log(image.getCheckSum());

image.outputImage();
