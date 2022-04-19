#https://code.earthengine.google.com/8310e548a78a83b800b8f2f383c05175#


/*
Copyright (c) 2018 Gennadii Donchyts. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
*/

exports.doc = "Animates images stretched (DOS-corrected) over a given polygon"

var utils = require('users/gena/packages:utils')
var assets = require('users/gena/packages:assets')  
var animation = require('users/gena/packages:animation')

Map.setOptions('HYBRID')

var images = assets.getImages(Map.getCenter(), { 
  missions: ['S2'/*, 'L8'*//*, 'L7'*/], 
  resample: 'bicubic', 
  filter: ee.Filter.date('2022-02-24', '2022-07-01')
})

// images = assets.getMostlyCleanImages(images, Map.getBounds(true))

images = images.sort('system:time_start')

function stretch(image) {
  // var bands = ['swir', 'nir', 'green']
  var bands = ['red', 'green', 'blue']
  var image2 = utils.stretchImage(image.select(bands), {
    percentiles: [0, 99],
    bounds: Map.getBounds(true),
    scale: Map.getScale() * 5
  })
  
  var bands = ['swir', 'nir', 'green']
  // var bands = ['red', 'green', 'blue']
  var image3 = utils.stretchImage(image.select(bands), {
    percentiles: [0, 99],
    bounds: Map.getBounds(true),
    scale: Map.getScale() * 5
  })

  image2 = image2.add(image3.multiply(ee.Image.constant([0.2, 0.1, 0.1]))).multiply(0.8).set({ label: image.date().format('YYYY-MM-dd hh:mm') })
  
  return image2
}

print(images.size())

images = images.map(stretch)

animation.animate(images, {
  vis: { min: 0, max: 1, gamma: 0.9 },
  label: 'label',
  masFrames: 100
})


