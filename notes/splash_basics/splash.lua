function main(splash, args)
    --splash:set_user_agent("test")
    --[[headers = {
      ['User-Agent'] = 'test'
    }
    splash:set_custom_headers(headers)
    --]]

    splash:on_request(function(request)
        request.set_header('User-Agent', 'test')
    end)

    url = args.url
    assert(splash:go(url))
    assert(splash:wait(1))

    input_box = assert(splash:select('#search_form_input_homepage'))
    input_box.focus()
    input_box:send_text("my user agent")
    assert(splash:wait(0.5))

    --[[btn = splash:select("#search_button_homepage")
    btn:mouse_click()
    assert(splash:wait(5))
    --]]

    input_box:send_keys("<Enter>")
    assert(splash:wait(5))
    splash:set_viewport_full()

    return {
      html = splash:html(),
      image = splash:png()
    }
  end
