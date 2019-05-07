export const asType = (type, name) => [type, name].join('_').toUpperCase()
export const tagAsType = (type, names) => (
  names.reduce((tags, name) => {
    tags[name] = asType(type, name)
    return tags
  }, {})
)

export const api = tagAsType('api', [
  'loading', 'loaded', 'error', 'updateQuery',
])

export const system = tagAsType('system', [
])

export const init = '@@INIT'

export const MATCH_THRESHOLD = 1
export const SIMILAR_THRESHOLD = 20
