/* Mobile check */

export const isiPhone = !!((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)))
export const isiPad = !!(navigator.userAgent.match(/iPad/i))
export const isAndroid = !!(navigator.userAgent.match(/Android/i))
export const isMobile = isiPhone || isiPad || isAndroid
export const isDesktop = !isMobile
export const isFirefox = typeof InstallTrigger !== 'undefined'

const htmlClassList = document.body.parentNode.classList
htmlClassList.add(isDesktop ? 'desktop' : 'mobile')
if (isFirefox) {
  htmlClassList.add('firefox')
}

/* AJAX */

export const get = (uri, data) => {
  let headers = {
    Accept: 'application/json, application/xml, text/play, text/html, *.*',
  }
  let opt = {
    method: 'GET',
    body: data,
    headers,
    // credentials: 'include',
  }
  // console.log(headers)
  // headers['X-CSRFToken'] = csrftoken
  return fetch(uri, opt).then(res => res.json())
}

export const post = (uri, data) => {
  let headers
  if (data instanceof FormData) {
    headers = {
      Accept: 'application/json, application/xml, text/play, text/html, *.*',
    }
  } else {
    headers = {
      Accept: 'application/json, application/xml, text/play, text/html, *.*',
      'Content-Type': 'application/json; charset=utf-8',
    }
    data = JSON.stringify(data)
  }
  let opt = {
    method: 'POST',
    body: data,
    headers,
    // credentials: 'include',
  }
  // console.log(headers)
  // headers['X-CSRFToken'] = csrftoken
  return fetch(uri, opt).then(res => res.json())
}
