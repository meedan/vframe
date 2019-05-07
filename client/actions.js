import { get, post } from './util'
import * as types from './types'

export const api = (dispatch, method, tag, url, params, after) => {
  dispatch({ type: types.api.loading, tag })
  return method(url, params).then(data => {
    if (after) data = after(data)
    dispatch({ type: types.api.loaded, tag, data })
    return data
  }).catch(err => {
    dispatch({ type: types.api.error, tag, error })
  })
}

export const upload = (blob, threshold) => dispatch => {
  const params = new FormData()
  params.append('q', blob)
  params.append('threshold', threshold)
  api(dispatch, post, 'similar', '/api/v1/similar', params)
}

export const similar = (url, threshold) => dispatch => {
  const params = new FormData()
  params.append('url', url)
  params.append('threshold', threshold)
  api(dispatch, post, 'similar', '/api/v1/similar', params)
}

export const match = (url, threshold) => dispatch => {
  const params = new FormData()
  params.append('url', url)
  params.append('threshold', threshold)
  api(dispatch, post, 'similar', '/api/v1/match', params)
}

export const updateQuery = state => dispatch => {
  dispatch({ type: types.api.updateQuery, state })
}