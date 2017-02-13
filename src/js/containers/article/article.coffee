$ = require 'jquery'
ImageGallery = require '../common/image_gallery.coffee'


$(document).ready ->
  $('p:has(img)').addClass('img')
  iv = new ImageGallery '.article'
  iv.show('img')
  return
