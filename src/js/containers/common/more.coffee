$ = require 'jquery'

more = (next_page) ->
  $.ajax
    url: '/more'
    method: 'GET'
    data:
      'next_page': next_page
    success: (data) ->
      if data
        $('.main').append(data['data'])
        $('#next_page').val(data['next_page'])
        return
  return

$(window).scroll ->
  scrollTop = $(this).scrollTop()
  scrollHeight = $(document).height()
  windowHeight = $(this).height()
  if scrollTop + windowHeight is scrollHeight
    more(
      $('#next_page').val()
    )
  return

module.exports = more
